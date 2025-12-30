from flask import request, jsonify
from datetime import datetime
from database.db import Database

# for CRUD endpoint
from models.models import TaskCreate, TaskUpdate, TaskResponse

# for chat endpoint
from google.genai import types
from agent.tools_definitions import client, config
from agent.tools import get_tasks as get_user_tasks, create_task as create_task_for_user, update_task as update_task_for_user, get_task_details

def task_to_dict(task_row):
    """Convert database row to dictionary"""
    if not task_row:
        return None
    
    result = dict(task_row)
    
    # Convert datetime strings if needed
    datetime_fields = ['deadline', 'creation_date', 'updated_date', 'deleted_at']
    for field in datetime_fields:
        if field in result and result[field]:
            if isinstance(result[field], str):
                try:
                    result[field] = datetime.fromisoformat(str(result[field]).replace('Z', '+00:00'))
                except:
                    # Try different format
                    result[field] = datetime.strptime(str(result[field]), '%Y-%m-%d %H:%M:%S')
    
    return result

def register_tasks_routes(app):
    """Register task routes directly on app"""

    @app.route('/api/chat', methods=['POST'])
    def chat():
        try:
            data = request.json
            user_prompt = data.get("user_prompt")
            # Receive history as a list of dicts from the client
            history = data.get("history", [])

            if not data or "user_prompt" not in data:
                return jsonify({"error": "Missing user_prompt"}), 400

            # Convert dictionary history back into Gemini 'Content' objects
            history = [types.Content(**msg) for msg in history]
            
            # Add the new user message
            history.append(types.Content(role="user", parts=[types.Part(text=user_prompt)]))

            # --- THE AGENT LOOP ---
            # max turns
            turns = 1
            while turns <= 5:
                turns += 1

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=history,
                    config=config
                )

                # Add model's reasoning/response to history
                model_content = response.candidates[0].content
                history.append(model_content)

                # Check for function calls in the parts
                function_call = None
                for part in model_content.parts:
                    if part.function_call:
                        function_call = part.function_call
                        break

                if function_call:
                    tool_name = function_call.name
                    tool_args = dict(function_call.args)
                    
                    # Call the function (and get result)
                    observation = None
                    match tool_name:
                        case "get_tasks":
                            observation = get_user_tasks(**tool_args)
                        case "create_task":
                            observation = create_task_for_user(**tool_args)
                        case "update_task":
                            observation = update_task_for_user(**tool_args)
                        case "get_task_details":
                            observation = get_task_details(**tool_args)

                    print(f"=================== called tool: {tool_name}")
                    
                    history.append(types.Content(
                        role="tool",
                        parts=[types.Part(
                            function_response=types.FunctionResponse(
                                name=tool_name,
                                response={"output": observation}
                            )
                        )]
                    ))

                else:
                    history.append(response.candidates[0].content)
                    break

            # --- PREPARE RESPONSE ---
            # Convert history objects back to JSON-serializable dicts
            serializable_history = [content.model_dump(exclude_none=True) for content in history]
            
            return jsonify({
                "response": response.text,
                "history": serializable_history
            })
        except Exception as e:
            print(f"Error: {e} ")
            return jsonify({"error": str(e)}), 500

    @app.route('/api/tasks', methods=['GET'])
    def get_tasks():
        """Get all tasks"""
        try:
            # Get query params
            status = request.args.get('status')
            priority = request.args.get('priority')
            category = request.args.get('category')
            
            # Build query
            conditions = ["deleted_at IS NULL"]
            params = []
            
            if status:
                conditions.append("status = %s")
                params.append(status)
            if priority:
                conditions.append("priority = %s")
                params.append(priority)
            if category:
                conditions.append("category = %s")
                params.append(category)
            
            where_clause = " AND ".join(conditions)
            query = f"SELECT * FROM tasks WHERE {where_clause} ORDER BY creation_date DESC"
            
            # Execute
            tasks = Database.execute_query(query, tuple(params), fetch_all=True)
            
            # Convert and validate
            task_list = []
            for task in tasks:
                task_dict = task_to_dict(task)
                if task_dict:
                    task_list.append(TaskResponse(**task_dict).model_dump()) # pydantic feature
            
            return jsonify({"tasks": task_list})
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/tasks/<int:task_id>', methods=['GET'])
    def get_task(task_id):
        """Get single task by ID"""
        try:
            query = "SELECT * FROM tasks WHERE task_id = %s AND deleted_at IS NULL"
            task = Database.execute_query(query, (task_id,), fetch_one=True)
            
            if not task:
                return jsonify({"error": "Task not found"}), 404
            
            task_dict = task_to_dict(task)
            return jsonify({"task": TaskResponse(**task_dict).model_dump()}) # pydantic feature
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/tasks', methods=['POST'])
    def create_task():
        """Create new task"""
        try:
            # Validate request
            task_data = TaskCreate(**request.get_json()) # flask feature
            
            # Prepare SQL
            query = """
                INSERT INTO tasks (title, description, deadline, category, priority, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (
                task_data.title,
                task_data.description,
                task_data.deadline,
                task_data.category,
                task_data.priority,
                task_data.status
            )
            
            # Execute
            task_id = Database.execute_query(query, params, lastrowid=True)
            
            # Return created task
            get_query = "SELECT * FROM tasks WHERE task_id = %s"
            created_task = Database.execute_query(get_query, (task_id,), fetch_one=True)
            task_dict = task_to_dict(created_task)
            
            return jsonify({
                "message": "Task created successfully",
                "task": TaskResponse(**task_dict).model_dump()
            }), 201
            
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    
    @app.route('/api/tasks/<int:task_id>', methods=['PUT'])
    def update_task(task_id):
        """Update existing task"""
        try:
            # Check if task exists
            check_query = "SELECT * FROM tasks WHERE task_id = %s AND deleted_at IS NULL"
            existing = Database.execute_query(check_query, (task_id,), fetch_one=True)
            
            if not existing:
                return jsonify({"error": "Task not found"}), 404
            
            # Validate update data
            update_data = TaskUpdate(**request.get_json())
            
            # Build dynamic UPDATE query
            update_fields = []
            params = []
            
            if update_data.title is not None:
                update_fields.append("title = %s")
                params.append(update_data.title)
            if update_data.description is not None:
                update_fields.append("description = %s")
                params.append(update_data.description)
            if update_data.deadline is not None:
                update_fields.append("deadline = %s")
                params.append(update_data.deadline)
            if update_data.category is not None:
                update_fields.append("category = %s")
                params.append(update_data.category)
            if update_data.priority is not None:
                update_fields.append("priority = %s")
                params.append(update_data.priority)
            if update_data.status is not None:
                update_fields.append("status = %s")
                params.append(update_data.status)
            
            # Add updated_date and task_id
            update_fields.append("updated_date = NOW()")
            params.append(task_id)
            
            # Execute update
            query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE task_id = %s"
            Database.execute_query(query, tuple(params))
            
            # Return updated task
            get_query = "SELECT * FROM tasks WHERE task_id = %s"
            updated_task = Database.execute_query(get_query, (task_id,), fetch_one=True)
            task_dict = task_to_dict(updated_task)
            
            return jsonify({
                "message": "Task updated successfully",
                "task": TaskResponse(**task_dict).model_dump()
            })
            
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    
    @app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        """Soft delete a task"""
        try:
            # Check if task exists
            check_query = "SELECT * FROM tasks WHERE task_id = %s AND deleted_at IS NULL"
            existing = Database.execute_query(check_query, (task_id,), fetch_one=True)
            
            if not existing:
                return jsonify({"error": "Task not found"}), 404
            
            # Soft delete
            query = "UPDATE tasks SET deleted_at = NOW() WHERE task_id = %s"
            Database.execute_query(query, (task_id,))
            
            return jsonify({
                "success": True,
                "message": "Task deleted successfully"
            })
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
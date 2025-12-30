from google import genai
from google.genai import types
from dotenv import load_dotenv
from datetime import date


import os
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Define tools using the SDK types
task_tools = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_tasks",
            description="Search tasks using filters for status, priority, category and deadline. you can use this as a lookup tool to find a task_id when you only have a task title or name.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "status": types.Schema(type="STRING", enum=["todo", "in progress", "canceled", "completed"]),
                    "priority": types.Schema(type="STRING", enum=["low", "medium", "high"]),
                    "category": types.Schema(type="STRING", description="e,g: 'work', 'study', 'health'..."),
                    "deadline": types.Schema(type="STRING", description="Format: YYYY-MM-DD")
                }
            )
        ),
        types.FunctionDeclaration(
            name="create_task",
            description="Creates a new task. Requires a title. Priority and Category should be lowercase (e.g., 'high', 'work').",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "title": types.Schema(type="STRING"),
                    "description": types.Schema(type="STRING"),
                    "priority": types.Schema(type="STRING", enum=["low", "medium", "high"]),
                    "category": types.Schema(type="STRING", description="e,g: 'work', 'study', 'health'..."),
                    "deadline": types.Schema(type="STRING", description="Format: YYYY-MM-DD")
                },
                required=["title"]
            )
        ),
        types.FunctionDeclaration(
            name="update_task",
            description="Modifies an existing task's fields (status, priority, etc.). Requires a valid task_id obtained from get_tasks.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "task_id": types.Schema(type="INTEGER"),
                    "status": types.Schema(type="STRING", enum=["todo", "in progress", "canceled", "completed"]),
                    "priority": types.Schema(type="STRING", enum=["low", "medium", "high"]),
                    "category": types.Schema(type="STRING", description="e,g: 'work', 'study', 'health'..."),
                    "deadline": types.Schema(type="STRING", description="Format: YYYY-MM-DD")
                },
                required=["task_id"]
            )
        ),
        types.FunctionDeclaration(
            name="get_task_details",
            description="Retrieves full info for a specific task and all its sub-tasks. Use this when the user asks for 'details' or 'subtasks'. Requires task_id.",
            parameters=types.Schema(
                type="OBJECT",
                properties={"task_id": types.Schema(type="INTEGER")},
                required=["task_id"]
            )
        )
    ]
)

config = types.GenerateContentConfig(
    tools=[task_tools],
    system_instruction=f"""You are a Task Manager Agent. Today's date: {date.today()}.
                        1. **ID Lookup**: If a user refers to a task by title (e.g., "Update 'Learn React'"), you MUST first call `get_tasks` to find the correct `task_id`. Do not guess IDs.
                        2. **Action Workflow**: Always describe your plan to the user first. Only execute `create_task` or `update_task` if the user confirms or gives a direct command to proceed.
                        3. **Data Integrity**: Ensure status values are valid (todo, in progress, completed) as defined in the database schema.
                        4. if the user asks for a task details or its subtasks, show them in a user friendly message (do not include task_id or sub_task_id)
                        """
)
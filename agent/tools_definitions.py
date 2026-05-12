from google import genai
from google.genai import types
from dotenv import load_dotenv
from datetime import date
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

task_tools = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_tasks",
            description="List/search tasks with optional filters. Use this as a lookup to find a task_id when you only have a title.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "status": types.Schema(type="STRING", enum=["todo", "in progress", "canceled", "completed"]),
                    "priority": types.Schema(type="STRING", enum=["low", "medium", "high"]),
                    "category": types.Schema(type="STRING"),
                    "deadline": types.Schema(type="STRING", description="Format: YYYY-MM-DD"),
                }
            )
        ),
        types.FunctionDeclaration(
            name="get_task_details",
            description="Get full details of a task including all its sub-tasks. Requires task_id.",
            parameters=types.Schema(
                type="OBJECT",
                properties={"task_id": types.Schema(type="INTEGER")},
                required=["task_id"]
            )
        ),
        types.FunctionDeclaration(
            name="create_task",
            description="Create a new task. Only title is required.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "title": types.Schema(type="STRING"),
                    "description": types.Schema(type="STRING"),
                    "priority": types.Schema(type="STRING", enum=["low", "medium", "high"]),
                    "status": types.Schema(type="STRING", enum=["todo", "in progress", "canceled", "completed"]),
                    "category": types.Schema(type="STRING"),
                    "deadline": types.Schema(type="STRING", description="Format: YYYY-MM-DDTHH:MM:SS"),
                },
                required=["title"]
            )
        ),
        types.FunctionDeclaration(
            name="update_task",
            description="Update fields of an existing task. Requires task_id. All other fields are optional.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "task_id": types.Schema(type="INTEGER"),
                    "title": types.Schema(type="STRING"),
                    "description": types.Schema(type="STRING"),
                    "priority": types.Schema(type="STRING", enum=["low", "medium", "high"]),
                    "status": types.Schema(type="STRING", enum=["todo", "in progress", "canceled", "completed"]),
                    "category": types.Schema(type="STRING"),
                    "deadline": types.Schema(type="STRING", description="Format: YYYY-MM-DDTHH:MM:SS"),
                },
                required=["task_id"]
            )
        ),
        types.FunctionDeclaration(
            name="delete_task",
            description="Soft-delete a task by task_id.",
            parameters=types.Schema(
                type="OBJECT",
                properties={"task_id": types.Schema(type="INTEGER")},
                required=["task_id"]
            )
        ),
        types.FunctionDeclaration(
            name="create_subtask",
            description="Add a sub-task to an existing task. Requires task_id and title.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "task_id": types.Schema(type="INTEGER"),
                    "title": types.Schema(type="STRING"),
                    "description": types.Schema(type="STRING"),
                    "deadline": types.Schema(type="STRING", description="Format: YYYY-MM-DDTHH:MM:SS"),
                },
                required=["task_id", "title"]
            )
        ),
        types.FunctionDeclaration(
            name="update_subtask",
            description="Update a sub-task. Requires task_id and sub_task_id. Use is_done=true to mark it complete.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "task_id": types.Schema(type="INTEGER"),
                    "sub_task_id": types.Schema(type="INTEGER"),
                    "title": types.Schema(type="STRING"),
                    "description": types.Schema(type="STRING"),
                    "deadline": types.Schema(type="STRING", description="Format: YYYY-MM-DDTHH:MM:SS"),
                    "is_done": types.Schema(type="BOOLEAN"),
                },
                required=["task_id", "sub_task_id"]
            )
        ),
        types.FunctionDeclaration(
            name="delete_subtask",
            description="Soft-delete a sub-task. Requires task_id and sub_task_id.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "task_id": types.Schema(type="INTEGER"),
                    "sub_task_id": types.Schema(type="INTEGER"),
                },
                required=["task_id", "sub_task_id"]
            )
        ),
    ]
)

config = types.GenerateContentConfig(
    tools=[task_tools],
    system_instruction=f"""You are a Task Manager Agent. Today's date: {date.today()}.
1. **ID Lookup**: If the user refers to a task or sub-task by name, call `get_tasks` or `get_task_details` first to resolve the correct id. Never guess ids.
2. **Confirmation**: Before executing `create_task`, `delete_task`, or `delete_subtask`, confirm with the user unless they gave a direct command.
3. **Valid values**: status must be one of: todo, in progress, canceled, completed. priority: low, medium, high.
"""
)

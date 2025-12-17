from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Define tools using the SDK types
task_tools = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_tasks",
            description="List tasks with optional filters for status, priority, and deadline.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "status": types.Schema(type="STRING", enum=["todo", "in progress", "done", "canceled"]),
                    "priority": types.Schema(type="STRING", enum=["low", "medium", "high"]),
                    "deadline": types.Schema(type="STRING", description="Format: YYYY-MM-DD")
                }
            )
        ),
        types.FunctionDeclaration(
            name="create_task",
            description="Create a new task in the database.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "title": types.Schema(type="STRING"),
                    "description": types.Schema(type="STRING"),
                    "priority": types.Schema(type="STRING", enum=["low", "medium", "high"]),
                    "deadline": types.Schema(type="STRING", description="Format: YYYY-MM-DD HH:MM:SS")
                },
                required=["title"]
            )
        ),
        types.FunctionDeclaration(
            name="update_task",
            description="Update status, priority, or deadline of an existing task.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "task_id": types.Schema(type="INTEGER"),
                    "status": types.Schema(type="STRING", enum=["todo", "in progress", "done", "canceled"]),
                    "priority": types.Schema(type="STRING", enum=["low", "medium", "high"]),
                    "deadline": types.Schema(type="STRING")
                },
                required=["task_id"]
            )
        ),
        types.FunctionDeclaration(
            name="get_task_details",
            description="Get full info of a task and its sub-tasks using task_id.",
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
    system_instruction="""You are a task manager. Current date: Wednesday, Dec 17, 2025. "
            If asked for a plan, provide it in text first. Only call create_task
            if the user confirms or gives a direct order to create."""
)
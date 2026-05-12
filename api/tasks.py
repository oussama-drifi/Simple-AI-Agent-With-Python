from flask import request, jsonify
from google.genai import types
from agent.tools_definitions import client, config
from agent.tools import (
    get_tasks, get_task_details,
    create_task, update_task, delete_task,
    create_subtask, update_subtask, delete_subtask,
)

TOOL_MAP = {
    "get_tasks": get_tasks,
    "get_task_details": get_task_details,
    "create_task": create_task,
    "update_task": update_task,
    "delete_task": delete_task,
    "create_subtask": create_subtask,
    "update_subtask": update_subtask,
    "delete_subtask": delete_subtask,
}

def register_tasks_routes(app):

    @app.route('/api/chat', methods=['POST'])
    def chat():
        try:
            data = request.json
            if not data or "user_prompt" not in data:
                return jsonify({"error": "Missing user_prompt"}), 400

            user_prompt = data["user_prompt"]
            history = [types.Content(**msg) for msg in data.get("history", [])]
            history.append(types.Content(role="user", parts=[types.Part(text=user_prompt)]))

            # Agent loop — max 5 turns
            for _ in range(5):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=history,
                    config=config
                )

                model_content = response.candidates[0].content
                history.append(model_content)

                function_call = next((p.function_call for p in model_content.parts if p.function_call), None)

                if not function_call:
                    break

                tool_name = function_call.name
                observation = TOOL_MAP[tool_name](**dict(function_call.args))
                print(f"[agent] called {tool_name} → {observation}")

                history.append(types.Content(
                    role="tool",
                    parts=[types.Part(function_response=types.FunctionResponse(
                        name=tool_name,
                        response={"output": observation}
                    ))]
                ))

            return jsonify({
                "response": response.text,
                "history": [c.model_dump(exclude_none=True) for c in history]
            })

        except Exception as e:
            print(f"[error] {e}")
            return jsonify({"error": str(e)}), 500
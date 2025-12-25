# from google.genai import types
# from agent.tools_definitions import client, config
# from agent.tools import get_tasks, update_task, create_task, get_task_details


# history = []

# while True:
#     user_prompt = input("you: ")
#     if user_prompt in ["break", "stop", "cancel"]:
#         break

#     history.append(types.Content(
#         role="user",
#         parts=[types.Part(text=str(user_prompt))]
#     ))

#     turns = 1
#     while turns <= 3: # max turns 3
#         turns += 1

#         print(f"=== iteration {turns + 1} of loop")

#         response = client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=history,
#             config=config
#         )

#         # Add model's reasoning/response to history
#         model_content = response.candidates[0].content
#         history.append(model_content)

#         # Check for function calls in the parts
#         function_call = None
#         for part in model_content.parts:
#             if part.function_call:
#                 function_call = part.function_call
#                 break

#         if function_call:

#             tool_name = function_call.name
#             tool_args = dict(function_call.args)
            
#             # Call the function (and get result)
#             observation = None
#             match tool_name:
#                 case "get_tasks":
#                     observation = get_tasks(**tool_args)
#                 case "create_task":
#                     observation = create_task(**tool_args)
#                 case "update_task":
#                     observation = update_task(**tool_args)
#                 case "get_task_details":
#                     observation = get_task_details(**tool_args)

#             print(f"=================== called tool: {tool_name}")
            
#             history.append(types.Content(
#                 role="tool",
#                 parts=[types.Part(
#                     function_response=types.FunctionResponse(
#                         name=tool_name,
#                         response={"output": observation}
#                     )
#                 )]
#             ))

#         else:
#             print("no tool call...")
#             print(response.text)
#             break

# print("done")




# test api endpoint

import requests

url = "http://127.0.0.1:5000/api/message"
history = []

while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit', 'stop']: break

    payload = {
        "user_prompt": user_input,
        "history": history
    }
    

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        print(f"Agent: {data['response']}")
        history = data['history'] # Update history with the server's new version
    else:
        print(f"Error: {response.text}")


print("process completed")
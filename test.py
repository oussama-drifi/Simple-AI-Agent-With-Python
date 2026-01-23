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
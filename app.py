from flask import Flask
from flask_cors import CORS
from api.tasks import register_tasks_routes
import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    CORS(app)  # for browser
    register_tasks_routes(app)
    return app

load_dotenv()
PORT = int(os.getenv("PORT", 5000))

print(f"server is up and running on port {PORT}")
app = create_app()

is_debug_mode = os.getenv("DEBUG_MODE") == "1"

if __name__ == '__main__':
    app.run(debug=is_debug_mode, port=PORT)
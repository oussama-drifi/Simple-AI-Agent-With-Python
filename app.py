from flask import Flask
from flask_cors import CORS
from api.tasks import register_tasks_routes
import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    CORS(app)  # for React
    register_tasks_routes(app)
    return app

PORT = os.getenv('PORT')

print(f"server is up and running on port {PORT}")
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=PORT)
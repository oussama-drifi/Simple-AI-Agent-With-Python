from flask import Flask
from flask_cors import CORS
from api.tasks import register_tasks_routes

def create_app():
    app = Flask(__name__)
    CORS(app)  # for React
    register_tasks_routes(app)
    return app


print("server is up and running")
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
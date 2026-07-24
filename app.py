from flask import Flask
from flask_cors import CORS
from api.tasks import register_tasks_routes
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, origins=app.config["CORS_ORIGIN"])  # for our FrontEnd only
    register_tasks_routes(app)
    return app

PORT = Config.PORT
app = create_app()

print(f"Server is up and running on port {PORT}")

if __name__ == '__main__':
    app.run(debug=Config.DEBUG_MODE, port=PORT)
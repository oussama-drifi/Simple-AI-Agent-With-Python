import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG_MODE = os.getenv('DEBUG_MODE') == '1'

    # Gemini
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

    # CORS (for React)
    CORS_ORIGIN = os.getenv('CORS_ORIGIN')

    # External CRUD service
    CRUD_SERVICE_BASE_URL = os.getenv('CRUD_SERVICE_BASE_URL', 'http://localhost:3000')

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # Gemini
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # CORS (for React)
    CORS_ORIGINS = ['http://localhost:3000']
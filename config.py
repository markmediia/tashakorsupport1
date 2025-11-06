"""
فایل پیکربندی برای چت بات برند تشکر
"""

import os
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

class Config:
    """کلاس پیکربندی اصلی"""
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    PORT = int(os.getenv('PORT', 5000))
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Chatbot Settings
    CHATBOT_MODEL = os.getenv('CHATBOT_MODEL', 'gpt-4o-mini')
    CHATBOT_TEMPERATURE = float(os.getenv('CHATBOT_TEMPERATURE', '0.7'))
    CHATBOT_MAX_TOKENS = int(os.getenv('CHATBOT_MAX_TOKENS', '500'))
    CHATBOT_MAX_HISTORY = int(os.getenv('CHATBOT_MAX_HISTORY', '10'))
    
    @staticmethod
    def validate():
        """اعتبارسنجی تنظیمات"""
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY باید تنظیم شود")


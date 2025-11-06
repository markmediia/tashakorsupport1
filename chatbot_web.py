"""
چت بات وب برند تشکر با استفاده از Flask و OpenAI API
"""

import os
import uuid
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from chatbot import TashakorChatBot
from functools import wraps
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')

# فعال‌سازی CORS برای دسترسی از دامنه‌های مختلف
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize chatbot (lazy initialization)
bot = None

def get_bot():
    """Lazy initialization of chatbot"""
    global bot
    if bot is None:
        try:
            bot = TashakorChatBot()
        except Exception as e:
            print(f"خطا در راه‌اندازی چت بات: {e}")
            return None
    return bot

def require_bot(f):
    """دکوراتور برای بررسی وجود bot"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_bot = get_bot()
        if current_bot is None:
            return jsonify({'error': 'چت بات در دسترس نیست. لطفا API key را تنظیم کنید.'}), 503
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """صفحه اصلی چت بات"""
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
@require_bot
def chat():
    """API برای دریافت پیام و ارسال پاسخ"""
    data = request.json
    
    if not data:
        return jsonify({'error': 'داده‌های نامعتبر'}), 400
    
    user_message = data.get('message', '').strip()
    session_id = data.get('session_id', None)
    
    if not user_message:
        return jsonify({'error': 'پیام خالی است'}), 400
    
    # ایجاد session_id جدید اگر وجود نداشته باشد
    if not session_id:
        session_id = str(uuid.uuid4())
    
    try:
        current_bot = get_bot()
        if current_bot is None:
            return jsonify({'error': 'چت بات در دسترس نیست'}), 503
            
        response = current_bot.get_response(user_message, session_id)
        
        return jsonify({
            'response': response,
            'bot_name': current_bot.name,
            'session_id': session_id
        })
    except Exception as e:
        return jsonify({
            'error': f'خطا در پردازش پیام: {str(e)}'
        }), 500

@app.route('/clear', methods=['POST'])
@require_bot
def clear_chat():
    """پاک کردن سابقه مکالمه"""
    data = request.json or {}
    session_id = data.get('session_id', 'default')
    
    current_bot = get_bot()
    if current_bot:
        current_bot.clear_conversation(session_id)
    
    return jsonify({
        'message': 'سابقه مکالمه پاک شد',
        'session_id': session_id
    })

@app.route('/health', methods=['GET'])
def health():
    """بررسی وضعیت سرویس"""
    current_bot = get_bot()
    return jsonify({
        'status': 'healthy' if current_bot else 'unhealthy',
        'bot_available': current_bot is not None
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    current_bot = get_bot()
    if current_bot:
        print(f"🚀 چت بات برند تشکر در حال اجرا است...")
        print(f"📡 پورت: {port}")
        print(f"🌐 آدرس: http://localhost:{port}")
    else:
        print("⚠️  هشدار: چت بات به دلیل عدم وجود API key راه‌اندازی نشد.")
        print("لطفا متغیر محیطی OPENAI_API_KEY را تنظیم کنید.")
    
    app.run(host='0.0.0.0', port=port, debug=debug)


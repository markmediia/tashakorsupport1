"""
چت بات وب برند تشکر با استفاده از Flask و OpenAI API
"""

import os
import uuid
import json as json_lib
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, send_file, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from chatbot import TashakorChatBot
from data_storage import CustomerDataStorage
from customer_manager import CustomerNumberManager
from functools import wraps
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی (فقط در محیط محلی، در Render از Environment Variables استفاده می‌شود)
# در Render، Environment Variables اولویت دارند
if os.getenv('RENDER') or os.getenv('DYNO'):  # Render یا Heroku
    # در production، از Environment Variables استفاده می‌کنیم
    pass
else:
    # در محیط محلی، از فایل .env استفاده می‌کنیم
    load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')

# تنظیمات آپلود فایل
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'ico', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# ایجاد پوشه uploads در صورت عدم وجود
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'logos'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'icons'), exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    """بررسی مجاز بودن پسوند فایل"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# فعال‌سازی CORS برای دسترسی از دامنه‌های مختلف
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize chatbot (lazy initialization)
bot = None

# Initialize data storage
data_storage = CustomerDataStorage()

# Initialize customer number manager
customer_manager = CustomerNumberManager()

def get_bot():
    """Lazy initialization of chatbot"""
    global bot
    if bot is None:
        try:
            # بررسی وجود API key - فقط از OPENAI_API_KEY استفاده می‌کنیم
            api_key = os.getenv('OPENAI_API_KEY')
            
            # بررسی تمام متغیرهای محیطی برای دیباگ
            all_env_vars = {k: v[:20] + '...' if len(v) > 20 else v for k, v in os.environ.items() if 'API' in k or 'KEY' in k}
            print(f"🔍 Environment variables containing 'API' or 'KEY': {all_env_vars}")
            
            if not api_key:
                print("❌ OPENAI_API_KEY environment variable not found")
                print(f"   Available env vars with 'OPENAI': {[k for k in os.environ.keys() if 'OPENAI' in k]}")
                return None
            
            # بررسی فرمت API key
            if not api_key.startswith('sk-'):
                print(f"❌ Invalid API key format. Key starts with: {api_key[:20]}...")
                print(f"   Key length: {len(api_key)}")
                print(f"   First 30 chars: {api_key[:30]}")
                print("   ⚠️  لطفا در Render، Environment Variable 'OPENAI_API_KEY' را بررسی کنید")
                return None
            
            bot = TashakorChatBot()
            print("✅ چت بات با موفقیت راه‌اندازی شد")
        except ValueError as e:
            print(f"❌ خطا در راه‌اندازی چت بات (ValueError): {e}")
            return None
        except Exception as e:
            print(f"❌ خطا در راه‌اندازی چت بات: {type(e).__name__}: {e}")
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

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """سرو کردن فایل‌های آپلود شده"""
    # filename می‌تواند شامل subdirectory باشد (مثلاً logos/file.png)
    directory = app.config['UPLOAD_FOLDER']
    return send_from_directory(directory, filename)

@app.route('/upload-logo', methods=['POST'])
def upload_logo():
    """آپلود لوگو"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'فایلی انتخاب نشده است'}), 400
        
        file = request.files['file']
        file_type = request.form.get('type', 'logo')  # logo یا icon
        
        if file.filename == '':
            return jsonify({'error': 'فایلی انتخاب نشده است'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'فرمت فایل مجاز نیست. فرمت‌های مجاز: PNG, JPG, JPEG, GIF, SVG, ICO, WEBP'}), 400
        
        # بررسی اندازه فایل
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({'error': f'حجم فایل بیش از حد مجاز است. حداکثر: {MAX_FILE_SIZE // 1024 // 1024}MB'}), 400
        
        # نام فایل امن
        filename = secure_filename(file.filename)
        # اضافه کردن timestamp برای جلوگیری از تداخل
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        
        # ذخیره فایل
        if file_type == 'icon':
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'icons', filename)
        else:
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'logos', filename)
        
        file.save(save_path)
        
        # حذف فایل‌های قدیمی (اختیاری)
        # می‌توانید فقط آخرین لوگو/آیکون را نگه دارید
        
        return jsonify({
            'success': True,
            'message': 'فایل با موفقیت آپلود شد',
            'filename': filename,
            'url': f'/uploads/{file_type}s/{filename}',
            'type': file_type
        })
        
    except Exception as e:
        return jsonify({
            'error': f'خطا در آپلود فایل: {str(e)}',
            'success': False
        }), 500

@app.route('/get-logo', methods=['GET'])
def get_logo():
    """دریافت لوگو/آیکون فعلی"""
    try:
        logo_file = None
        icon_file = None
        
        # پیدا کردن آخرین لوگو
        logos_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'logos')
        if os.path.exists(logos_dir):
            logos = [f for f in os.listdir(logos_dir) if os.path.isfile(os.path.join(logos_dir, f))]
            if logos:
                logos.sort(reverse=True)  # جدیدترین اول
                logo_file = f'/uploads/logos/{logos[0]}'
        
        # پیدا کردن آخرین آیکون
        icons_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'icons')
        if os.path.exists(icons_dir):
            icons = [f for f in os.listdir(icons_dir) if os.path.isfile(os.path.join(icons_dir, f))]
            if icons:
                icons.sort(reverse=True)  # جدیدترین اول
                icon_file = f'/uploads/icons/{icons[0]}'
        
        return jsonify({
            'success': True,
            'logo': logo_file,
            'icon': icon_file
        })
        
    except Exception as e:
        return jsonify({
            'error': f'خطا: {str(e)}',
            'success': False
        }), 500

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

@app.route('/save-customer', methods=['POST'])
def save_customer():
    """ذخیره اطلاعات مشتری"""
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'داده‌های نامعتبر'}), 400
        
        session_id = data.get('session_id', '')
        
        # دریافت یا ایجاد شماره مشتری
        customer_number = customer_manager.get_or_create_customer_number(session_id)
        
        # استخراج اطلاعات از درخواست
        customer_data = {
            'customer_number': customer_number,
            'name': data.get('name', ''),
            'phone': data.get('phone', ''),
            'email': data.get('email', ''),
            'address': data.get('address', ''),
            'product': data.get('product', ''),
            'quantity': data.get('quantity', ''),
            'price': data.get('price', ''),
            'status': data.get('status', 'در انتظار'),
            'notes': data.get('notes', ''),
            'session_id': session_id
        }
        
        # ذخیره اطلاعات
        success = data_storage.save_customer_data(customer_data)
        
        if success:
            return jsonify({
                'message': 'اطلاعات با موفقیت ذخیره شد',
                'success': True,
                'customer_number': customer_number
            })
        else:
            return jsonify({
                'error': 'خطا در ذخیره اطلاعات',
                'success': False
            }), 500
            
    except Exception as e:
        return jsonify({
            'error': f'خطا: {str(e)}',
            'success': False
        }), 500

@app.route('/get-customer-number', methods=['POST'])
def get_customer_number():
    """دریافت شماره مشتری برای session_id"""
    try:
        data = request.json
        session_id = data.get('session_id', '')
        
        if not session_id:
            return jsonify({'error': 'session_id الزامی است'}), 400
        
        # دریافت یا ایجاد شماره مشتری
        customer_number = customer_manager.get_or_create_customer_number(session_id)
        
        return jsonify({
            'success': True,
            'customer_number': customer_number,
            'session_id': session_id
        })
        
    except Exception as e:
        return jsonify({
            'error': f'خطا: {str(e)}',
            'success': False
        }), 500

@app.route('/extract-info', methods=['POST'])
def extract_customer_info():
    """استخراج اطلاعات مشتری از مکالمه با استفاده از ChatGPT"""
    try:
        current_bot = get_bot()
        if current_bot is None:
            return jsonify({'error': 'چت بات در دسترس نیست'}), 503
        
        data = request.json
        conversation_history = data.get('conversation', [])
        
        if not conversation_history:
            return jsonify({'error': 'مکالمه خالی است'}), 400
        
        # ساخت prompt برای استخراج اطلاعات
        extraction_prompt = """از مکالمه زیر، اطلاعات مشتری را استخراج کن و به صورت JSON برگردان.
        اگر اطلاعاتی موجود نبود، مقدار null بگذار.
        
        فرمت JSON:
        {
            "name": "نام و نام خانوادگی",
            "phone": "شماره تماس",
            "email": "ایمیل",
            "address": "آدرس کامل",
            "product": "محصول مورد نظر",
            "quantity": "تعداد",
            "price": "قیمت",
            "notes": "یادداشت‌های اضافی"
        }
        
        فقط JSON را برگردان، بدون توضیح اضافی."""
        
        # اضافه کردن مکالمه به prompt
        conversation_text = "\n".join([f"{msg.get('role', 'user')}: {msg.get('content', '')}" 
                                      for msg in conversation_history[-10:]])
        
        full_prompt = f"{extraction_prompt}\n\nمکالمه:\n{conversation_text}"
        
        # فراخوانی ChatGPT برای استخراج
        response = current_bot.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "شما یک سیستم استخراج اطلاعات هستید. فقط JSON برگردانید."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )
        
        extracted_data = json_lib.loads(response.choices[0].message.content.strip())
        
        return jsonify({
            'success': True,
            'data': extracted_data
        })
        
    except Exception as e:
        return jsonify({
            'error': f'خطا در استخراج اطلاعات: {str(e)}',
            'success': False
        }), 500

@app.route('/download-excel', methods=['GET'])
def download_excel():
    """دانلود فایل Excel اطلاعات مشتریان"""
    try:
        excel_file = data_storage.excel_file
        if not os.path.exists(excel_file):
            return jsonify({'error': 'فایل یافت نشد'}), 404
        
        return send_file(
            excel_file,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'customers_data_{datetime.now().strftime("%Y%m%d")}.xlsx'
        )
    except Exception as e:
        return jsonify({'error': f'خطا: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health():
    """بررسی وضعیت سرویس"""
    current_bot = get_bot()
    api_key_exists = os.getenv('OPENAI_API_KEY') is not None
    api_key_preview = None
    if api_key_exists:
        key = os.getenv('OPENAI_API_KEY', '')
        api_key_preview = f"{key[:10]}...{key[-10:]}" if len(key) > 20 else "***"
    
    return jsonify({
        'status': 'healthy' if current_bot else 'unhealthy',
        'bot_available': current_bot is not None,
        'api_key_exists': api_key_exists,
        'api_key_preview': api_key_preview,
        'api_key_format_valid': api_key_exists and os.getenv('OPENAI_API_KEY', '').startswith('sk-'),
        'environment': 'render' if os.getenv('RENDER') else 'local'
    })

@app.route('/debug', methods=['GET'])
def debug():
    """Endpoint برای دیباگ (فقط در development)"""
    api_key = os.getenv('OPENAI_API_KEY')
    api_key_exists = api_key is not None
    
    debug_info = {
        'api_key_exists': api_key_exists,
        'api_key_length': len(api_key) if api_key else 0,
        'api_key_starts_with_sk': api_key.startswith('sk-') if api_key else False,
        'api_key_preview': f"{api_key[:15]}...{api_key[-10:]}" if api_key and len(api_key) > 25 else "***",
        'render_env': os.getenv('RENDER'),
        'flask_env': os.getenv('FLASK_ENV'),
        'port': os.getenv('PORT'),
    }
    
    # تلاش برای ایجاد bot و گرفتن خطا
    try:
        test_bot = TashakorChatBot()
        debug_info['bot_creation'] = 'success'
        debug_info['bot_name'] = test_bot.name
    except Exception as e:
        debug_info['bot_creation'] = 'failed'
        debug_info['bot_error'] = str(e)
        debug_info['bot_error_type'] = type(e).__name__
    
    return jsonify(debug_info)

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


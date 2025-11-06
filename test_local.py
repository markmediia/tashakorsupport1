"""
اسکریپت تست برای بررسی نصب و راه‌اندازی محلی
"""

import sys
import os

def check_python_version():
    """بررسی نسخه Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ مورد نیاز است")
        print(f"   نسخه فعلی: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """بررسی وابستگی‌ها"""
    required = ['flask', 'openai', 'flask_cors', 'dotenv']
    missing = []
    
    for package in required:
        try:
            if package == 'flask_cors':
                __import__('flask_cors')
            elif package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"✅ {package} نصب شده")
        except ImportError:
            print(f"❌ {package} نصب نشده")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  برای نصب وابستگی‌های گمشده اجرا کنید:")
        print(f"   pip install {' '.join(missing)}")
        return False
    return True

def check_env_file():
    """بررسی فایل .env"""
    if not os.path.exists('.env'):
        print("❌ فایل .env یافت نشد")
        print("   فایل .env.example را کپی کرده و API key را وارد کنید")
        return False
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your-openai-api-key-here':
        print("❌ OPENAI_API_KEY در فایل .env تنظیم نشده")
        return False
    
    print("✅ فایل .env یافت شد و API key تنظیم شده")
    return True

def test_chatbot_import():
    """تست import کردن chatbot"""
    try:
        from chatbot import TashakorChatBot
        print("✅ کلاس TashakorChatBot قابل import است")
        return True
    except Exception as e:
        print(f"❌ خطا در import: {e}")
        return False

def test_chatbot_init():
    """تست ایجاد instance از chatbot"""
    try:
        from chatbot import TashakorChatBot
        bot = TashakorChatBot()
        print("✅ چت‌بات با موفقیت ایجاد شد")
        return True
    except Exception as e:
        print(f"❌ خطا در ایجاد چت‌بات: {e}")
        return False

def main():
    print("=" * 50)
    print("بررسی نصب و راه‌اندازی چت‌بات برند تشکر")
    print("=" * 50)
    print()
    
    checks = [
        ("نسخه Python", check_python_version),
        ("وابستگی‌ها", check_dependencies),
        ("فایل .env", check_env_file),
        ("Import کلاس", test_chatbot_import),
        ("ایجاد چت‌بات", test_chatbot_init),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n[{name}]")
        result = check_func()
        results.append(result)
    
    print("\n" + "=" * 50)
    if all(results):
        print("✅ همه چیز آماده است! می‌توانید سرور را اجرا کنید:")
        print("   python chatbot_web.py")
    else:
        print("❌ برخی مشکلات وجود دارد. لطفا آنها را برطرف کنید.")
    print("=" * 50)

if __name__ == "__main__":
    main()


@echo off
chcp 65001 >nul
echo ========================================
echo راه‌اندازی چت‌بات برند تشکر
echo ========================================
echo.

REM بررسی وجود Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python نصب نشده است!
    echo لطفا Python 3.11+ را از python.org نصب کنید
    pause
    exit /b 1
)

echo ✅ Python یافت شد
echo.

REM بررسی وجود فایل .env
if not exist .env (
    echo ⚠️  فایل .env یافت نشد
    echo در حال کپی از .env.example...
    copy .env.example .env >nul
    echo ✅ فایل .env ایجاد شد
    echo ⚠️  لطفا فایل .env را باز کرده و API key را وارد کنید
    echo.
    pause
    exit /b 1
)

echo ✅ فایل .env یافت شد
echo.

REM نصب وابستگی‌ها
echo در حال نصب وابستگی‌ها...
python -m pip install -q -r requirements.txt
if errorlevel 1 (
    echo ❌ خطا در نصب وابستگی‌ها
    pause
    exit /b 1
)

echo ✅ وابستگی‌ها نصب شدند
echo.

REM اجرای سرور
echo ========================================
echo 🚀 در حال راه‌اندازی سرور...
echo ========================================
echo.
echo آدرس: http://localhost:5000
echo برای توقف سرور، Ctrl+C را فشار دهید
echo.

python chatbot_web.py

pause


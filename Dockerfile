FROM python:3.11-slim

WORKDIR /app

# نصب وابستگی‌ها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# کپی فایل‌های پروژه
COPY . .

# ایجاد پوشه templates اگر وجود نداشته باشد
RUN mkdir -p templates

# Expose port
EXPOSE 5000

# اجرای برنامه
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "chatbot_web:app"]


# راهنمای کامل استقرار چت‌بات روی دامنه 🌐

## روش 1: استقرار روی Render (پیشنهادی - رایگان و آسان) ⭐

### مراحل:

1. **آماده‌سازی پروژه در GitHub**
   ```bash
   # اگر Git نصب دارید:
   cd chatbot_project
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. **ایجاد حساب در Render**
   - به [render.com](https://render.com) بروید
   - با GitHub حساب خود وارد شوید
   - روی "New +" کلیک کنید
   - "Web Service" را انتخاب کنید

3. **اتصال Repository**
   - "Connect GitHub" را انتخاب کنید
   - Repository خود را انتخاب کنید
   - Branch را "main" انتخاب کنید

4. **تنظیمات Build & Deploy**
   - **Name**: `tashakor-chatbot` (یا هر نامی که می‌خواهید)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT chatbot_web:app`

5. **تنظیم Environment Variables**
   در بخش "Environment Variables" این متغیرها را اضافه کنید:
   ```
   OPENAI_API_KEY = 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
   SECRET_KEY = یک-رشته-تصادفی-و-امن-برای-production
   FLASK_ENV = production
   PORT = 10000
   ```

6. **استقرار**
   - روی "Create Web Service" کلیک کنید
   - Render به صورت خودکار پروژه را build و deploy می‌کند
   - بعد از چند دقیقه، آدرس شما آماده است: `https://tashakor-chatbot.onrender.com`

7. **اتصال دامنه شخصی (اختیاری)**
   - در تنظیمات سرویس، به بخش "Custom Domains" بروید
   - دامنه خود را اضافه کنید (مثلاً: `chatbot.yourdomain.com`)
   - DNS records را طبق راهنمای Render تنظیم کنید

---

## روش 2: استقرار روی Railway (سریع و آسان) 🚂

### مراحل:

1. **آماده‌سازی در GitHub** (همانند روش 1)

2. **ایجاد حساب در Railway**
   - به [railway.app](https://railway.app) بروید
   - با GitHub وارد شوید

3. **ایجاد پروژه جدید**
   - "New Project" را کلیک کنید
   - "Deploy from GitHub repo" را انتخاب کنید
   - Repository خود را انتخاب کنید

4. **تنظیم Environment Variables**
   در بخش "Variables" این متغیرها را اضافه کنید:
   ```
   OPENAI_API_KEY = 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
   SECRET_KEY = یک-رشته-تصادفی-و-امن
   FLASK_ENV = production
   ```

5. **اتصال دامنه**
   - در تنظیمات پروژه، "Settings" → "Networking"
   - "Generate Domain" را کلیک کنید یا دامنه خود را اضافه کنید

---

## روش 3: استقرار روی VPS (کنترل کامل) 🖥️

### پیش‌نیازها:
- یک سرور VPS (مثلاً از DigitalOcean، Linode، یا Hetzner)
- دسترسی SSH به سرور
- دامنه (اختیاری)

### مراحل:

1. **اتصال به سرور**
   ```bash
   ssh root@your-server-ip
   ```

2. **نصب Python و وابستگی‌ها**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3-pip python3-venv nginx git
   
   # CentOS/RHEL
   sudo yum install python3-pip nginx git
   ```

3. **کلون کردن پروژه**
   ```bash
   cd /var/www
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git chatbot
   cd chatbot
   ```

4. **ایجاد Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

5. **ایجاد فایل .env**
   ```bash
   nano .env
   ```
   محتوا:
   ```
   OPENAI_API_KEY=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
   SECRET_KEY=یک-رشته-تصادفی-و-امن
   FLASK_ENV=production
   PORT=5000
   ```

6. **ایجاد Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/chatbot.service
   ```
   محتوا:
   ```ini
   [Unit]
   Description=Tashakor Chatbot
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/var/www/chatbot
   Environment="PATH=/var/www/chatbot/venv/bin"
   ExecStart=/var/www/chatbot/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:5000 chatbot_web:app

   [Install]
   WantedBy=multi-user.target
   ```

7. **اجرای Service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start chatbot
   sudo systemctl enable chatbot
   ```

8. **تنظیم Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/chatbot
   ```
   محتوا:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com www.your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

9. **فعال‌سازی سایت**
   ```bash
   sudo ln -s /etc/nginx/sites-available/chatbot /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

10. **تنظیم SSL با Let's Encrypt (HTTPS)**
    ```bash
    sudo apt install certbot python3-certbot-nginx
    sudo certbot --nginx -d your-domain.com -d www.your-domain.com
    ```

---

## روش 4: استقرار با Docker 🐳

### در سرور VPS:

1. **نصب Docker**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```

2. **کلون پروژه**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
   cd chatbot_project
   ```

3. **ایجاد .env** (همانند قبل)

4. **اجرای با Docker Compose**
   ```bash
   docker-compose up -d
   ```

5. **تنظیم Nginx** (همانند روش 3)

---

## تست محلی قبل از استقرار

قبل از استقرار روی دامنه، مطمئن شوید که در سیستم محلی کار می‌کند:

```bash
cd chatbot_project

# نصب وابستگی‌ها
pip install -r requirements.txt

# اجرای سرور
python chatbot_web.py
```

اگر خطا داد، بررسی کنید:
- Python 3.11+ نصب است؟
- همه کتابخانه‌ها نصب شده‌اند؟
- فایل `.env` وجود دارد و API key درست است؟

---

## نکات مهم امنیتی 🔒

1. **هرگز API key را در Git commit نکنید**
   - فایل `.env` در `.gitignore` است
   - فقط در Environment Variables سرویس قرار دهید

2. **استفاده از HTTPS**
   - در production حتماً از HTTPS استفاده کنید
   - Let's Encrypt رایگان است

3. **تغییر SECRET_KEY**
   - در production حتماً `SECRET_KEY` را تغییر دهید
   - از یک رشته تصادفی و طولانی استفاده کنید

4. **محدود کردن دسترسی**
   - در صورت نیاز، IP های مجاز را محدود کنید
   - Rate limiting اضافه کنید

---

## عیب‌یابی مشکلات رایج

### مشکل: سرور اجرا نمی‌شود
- بررسی کنید که همه Environment Variables تنظیم شده‌اند
- لاگ‌ها را بررسی کنید: `docker logs` یا `journalctl -u chatbot`

### مشکل: 502 Bad Gateway
- بررسی کنید که Gunicorn در حال اجرا است
- Port را بررسی کنید

### مشکل: API کار نمی‌کند
- API key را بررسی کنید
- از داشتن اعتبار کافی در حساب OpenAI اطمینان حاصل کنید

---

## هزینه‌ها 💰

- **Render**: رایگان (با محدودیت) یا $7/ماه برای بدون محدودیت
- **Railway**: $5 اعتبار رایگان، سپس pay-as-you-go
- **VPS**: از $5/ماه (DigitalOcean, Linode)
- **OpenAI API**: بر اساس استفاده (gpt-4o-mini ارزان است)

---

**موفق باشید! 🚀**


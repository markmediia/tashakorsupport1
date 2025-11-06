# راهنمای تنظیم Environment Variables در Render 🔧

## مشکل: خطای 401 - Invalid API Key

اگر خطای `Incorrect API key provided` می‌بینید، یعنی Environment Variable در Render به درستی تنظیم نشده است.

## راه حل: تنظیم Environment Variables در Render

### مراحل:

1. **وارد داشبورد Render شوید**
   - به [dashboard.render.com](https://dashboard.render.com) بروید
   - سرویس خود را انتخاب کنید

2. **بخش Environment Variables را پیدا کنید**
   - در منوی سمت چپ، روی سرویس خود کلیک کنید
   - در منوی بالا، "Environment" را انتخاب کنید
   - یا در تنظیمات سرویس، بخش "Environment Variables" را پیدا کنید

3. **اضافه کردن متغیرها**

   روی "Add Environment Variable" کلیک کنید و این متغیرها را اضافه کنید:

   #### متغیر 1: OPENAI_API_KEY
   - **Key**: `OPENAI_API_KEY`
   - **Value**: `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`
   - **Important**: کل API key را کپی کنید (شامل `sk-proj-` در ابتدا)

   #### متغیر 2: SECRET_KEY
   - **Key**: `SECRET_KEY`
   - **Value**: یک رشته تصادفی و طولانی (مثلاً: `tashakor-secret-key-2024-random-string-12345`)

   #### متغیر 3: FLASK_ENV
   - **Key**: `FLASK_ENV`
   - **Value**: `production`

4. **ذخیره و Redeploy**
   - بعد از اضافه کردن همه متغیرها، "Save Changes" را کلیک کنید
   - Render به صورت خودکار redeploy می‌کند
   - یا می‌توانید دستی "Manual Deploy" → "Deploy latest commit" را کلیک کنید

## بررسی صحت تنظیمات

### روش 1: بررسی در Logs
1. در داشبورد Render، به بخش "Logs" بروید
2. اگر API key درست باشد، خطایی نمی‌بینید
3. اگر خطا دیدید، بررسی کنید که:
   - نام متغیر دقیقاً `OPENAI_API_KEY` باشد (با حروف بزرگ)
   - مقدار API key کامل باشد
   - هیچ فاصله اضافی در ابتدا یا انتها نباشد

### روش 2: تست Health Endpoint
بعد از deploy، به آدرس زیر بروید:
```
https://your-app.onrender.com/health
```

اگر `bot_available: true` باشد، یعنی API key درست است.

## مشکلات رایج

### مشکل 1: "Incorrect API key provided"
**علت**: API key در Environment Variables تنظیم نشده یا اشتباه است
**راه حل**: 
- بررسی کنید که متغیر `OPENAI_API_KEY` وجود دارد
- مطمئن شوید که کل API key را کپی کرده‌اید
- بعد از تغییر، حتماً redeploy کنید

### مشکل 2: API key با "render-t" شروع می‌شود
**علت**: Render از یک مقدار پیش‌فرض استفاده می‌کند
**راه حل**: 
- Environment Variable `OPENAI_API_KEY` را حذف و دوباره اضافه کنید
- مطمئن شوید که مقدار درست را وارد کرده‌اید

### مشکل 3: بعد از تغییر، هنوز خطا می‌دهد
**راه حل**:
1. در Render، "Manual Deploy" → "Clear build cache & deploy" را انجام دهید
2. یا Environment Variable را حذف کرده و دوباره اضافه کنید
3. مطمئن شوید که بعد از تغییر، redeploy انجام شده است

## نکات مهم

✅ **هرگز API key را در کد قرار ندهید**
✅ **فقط در Environment Variables قرار دهید**
✅ **بعد از تغییر Environment Variables، حتماً redeploy کنید**
✅ **API key باید با `sk-` یا `sk-proj-` شروع شود**

## تست محلی

برای تست در سیستم محلی، فایل `.env` را بررسی کنید:
```env
OPENAI_API_KEY=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
```

---

**اگر هنوز مشکل دارید، لاگ‌های Render را بررسی کنید و خطای دقیق را ببینید.**


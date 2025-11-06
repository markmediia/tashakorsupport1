# راهنمای تنظیم Google Sheets (اختیاری)

## مراحل تنظیم:

### 1. ایجاد Google Cloud Project

1. به [Google Cloud Console](https://console.cloud.google.com/) بروید
2. یک پروژه جدید ایجاد کنید
3. "APIs & Services" → "Library" را باز کنید
4. "Google Sheets API" و "Google Drive API" را فعال کنید

### 2. ایجاد Service Account

1. "APIs & Services" → "Credentials" را باز کنید
2. "Create Credentials" → "Service Account" را انتخاب کنید
3. نام و توضیحات را وارد کنید
4. "Create and Continue" را کلیک کنید
5. Role را "Editor" انتخاب کنید
6. "Done" را کلیک کنید

### 3. دانلود Credentials

1. روی Service Account ایجاد شده کلیک کنید
2. به تب "Keys" بروید
3. "Add Key" → "Create new key" → "JSON" را انتخاب کنید
4. فایل JSON دانلود می‌شود
5. این فایل را به نام `credentials.json` در پوشه پروژه قرار دهید

### 4. ایجاد Google Sheet

1. یک Google Sheet جدید ایجاد کنید
2. از URL، Sheet ID را کپی کنید:
   ```
   https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit
   ```
3. Sheet ID را در Environment Variable قرار دهید:
   ```
   GOOGLE_SHEET_ID=your-sheet-id-here
   ```

### 5. اشتراک‌گذاری Sheet

1. Sheet را باز کنید
2. "Share" را کلیک کنید
3. ایمیل Service Account را (از فایل credentials.json) اضافه کنید
4. دسترسی "Editor" بدهید

### 6. تنظیم Environment Variables در Render

در Render، این متغیرها را اضافه کنید:
- `GOOGLE_SHEET_ID`: ID شیت شما
- `GOOGLE_CREDENTIALS_FILE`: `credentials.json` (یا مسیر فایل)

**نکته**: در Render، باید محتوای فایل `credentials.json` را به صورت Environment Variable قرار دهید و در کد آن را بسازید.

---

**اگر فقط Excel می‌خواهید، نیازی به تنظیم Google Sheets نیست!**


# راهنمای استفاده از سیستم ذخیره اطلاعات مشتریان 📊

## قابلیت‌های اضافه شده:

✅ **ذخیره در Excel**: اطلاعات مشتریان به صورت خودکار در فایل Excel ذخیره می‌شود
✅ **ذخیره در Google Sheets**: (اختیاری) می‌توانید به Google Sheets متصل شوید
✅ **استخراج خودکار اطلاعات**: ChatGPT می‌تواند اطلاعات را از مکالمه استخراج کند
✅ **دانلود فایل Excel**: می‌توانید فایل Excel را دانلود کنید

## API Endpoints:

### 1. POST `/save-customer`
ذخیره اطلاعات مشتری

**Request:**
```json
{
  "name": "علی احمدی",
  "phone": "09123456789",
  "email": "ali@example.com",
  "address": "تهران، خیابان ولیعصر",
  "product": "محصول شماره 1",
  "quantity": "2",
  "price": "500000",
  "status": "در انتظار",
  "notes": "یادداشت اضافی",
  "session_id": "session-123"
}
```

**Response:**
```json
{
  "message": "اطلاعات با موفقیت ذخیره شد",
  "success": true,
  "customer_number": "CUST-0001"
}
```

### 2. POST `/get-customer-number`
دریافت شماره مشتری برای session_id

**Request:**
```json
{
  "session_id": "session-123"
}
```

**Response:**
```json
{
  "success": true,
  "customer_number": "CUST-0001",
  "session_id": "session-123"
}
```

### 2. POST `/extract-info`
استخراج اطلاعات از مکالمه با ChatGPT

**Request:**
```json
{
  "conversation": [
    {"role": "user", "content": "سلام، من علی احمدی هستم"},
    {"role": "assistant", "content": "سلام آقای احمدی"},
    {"role": "user", "content": "می‌خوام محصول شماره 1 رو بخرم"},
    {"role": "assistant", "content": "بله، حتماً"}
  ]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "name": "علی احمدی",
    "phone": null,
    "email": null,
    "address": null,
    "product": "محصول شماره 1",
    "quantity": null,
    "price": null,
    "notes": null
  }
}
```

### 3. GET `/download-excel`
دانلود فایل Excel اطلاعات مشتریان

**Response:** فایل Excel دانلود می‌شود

## نحوه استفاده در Frontend:

### مثال JavaScript:

```javascript
// ذخیره اطلاعات مشتری
async function saveCustomer(customerData) {
  const response = await fetch('/save-customer', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: customerData.name,
      phone: customerData.phone,
      email: customerData.email,
      address: customerData.address,
      product: customerData.product,
      quantity: customerData.quantity,
      price: customerData.price,
      session_id: sessionId
    })
  });
  
  const result = await response.json();
  if (result.success) {
    alert('اطلاعات با موفقیت ذخیره شد!');
  }
}

// استخراج اطلاعات از مکالمه
async function extractInfoFromConversation(conversation) {
  const response = await fetch('/extract-info', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      conversation: conversation
    })
  });
  
  const result = await response.json();
  return result.data;
}
```

## فایل Excel:

فایل Excel به نام `customers_data.xlsx` در پوشه پروژه ایجاد می‌شود و شامل این ستون‌هاست:

- **شماره مشتری** (مثلاً: CUST-0001) - شماره اختصاصی هر مشتری
- تاریخ و زمان
- نام و نام خانوادگی
- شماره تماس
- ایمیل
- آدرس
- محصول مورد نظر
- تعداد
- قیمت
- وضعیت
- یادداشت
- Session ID

**نکته**: هر مشتری یک شماره منحصر به فرد دارد که بر اساس session_id تولید می‌شود.

## تنظیم Google Sheets (اختیاری):

برای استفاده از Google Sheets، فایل `GOOGLE_SHEETS_SETUP.md` را مطالعه کنید.

## نکات مهم:

1. **در Render**: فایل Excel در سیستم فایل Render ذخیره می‌شود
2. **پشتیبان‌گیری**: بهتر است به صورت دوره‌ای فایل Excel را دانلود کنید
3. **امنیت**: endpoint `/download-excel` را در production محافظت کنید
4. **Google Sheets**: برای ذخیره دائمی و دسترسی آسان‌تر، از Google Sheets استفاده کنید

## مثال استفاده کامل:

```javascript
// بعد از اینکه مشتری اطلاعات را داد
const customerInfo = await extractInfoFromConversation(conversationHistory);

// ذخیره اطلاعات
await saveCustomer({
  ...customerInfo,
  session_id: sessionId,
  status: 'در انتظار'
});
```

---

**موفق باشید! 🚀**


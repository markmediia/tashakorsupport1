"""
چت بات پشتیبان و فروشنده برند تشکر با استفاده از OpenAI API
"""

import os
import json
from datetime import datetime
from openai import OpenAI
from typing import List, Dict, Optional

class TashakorChatBot:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Tashakor brand chatbot
        
        Args:
            api_key: OpenAI API key. If None, will read from environment variable OPENAI_API_KEY
        """
        self.name = "پشتیبان برند تشکر"
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        # بررسی صحت API key (شروع با sk-)
        if not self.api_key.startswith('sk-'):
            raise ValueError(f"Invalid API key format. API key should start with 'sk-'. Current key starts with: {self.api_key[:10]}...")
        
        self.client = OpenAI(api_key=self.api_key)
        
        # کانتکس برند تشکر
        self.brand_context = """
        شما یک پشتیبان و فروشنده حرفه‌ای برای برند "تشکر" هستید. برند تشکر یک برند معتبر و محبوب در زمینه [لطفا زمینه کسب و کار را مشخص کنید] است.
        
        وظایف شما:
        1. پاسخ به سوالات مشتریان درباره محصولات و خدمات برند تشکر
        2. راهنمایی مشتریان در انتخاب محصول مناسب
        3. ارائه اطلاعات درباره قیمت‌ها، تخفیف‌ها و پیشنهادات ویژه
        4. حل مشکلات و پاسخ به شکایات مشتریان
        5. ثبت سفارشات و راهنمایی برای خرید
        
        ویژگی‌های برند تشکر:
        - کیفیت بالا
        - خدمات مشتری عالی
        - قیمت‌های رقابتی
        - تحویل سریع
        
        همیشه مودب، صبور و مفید باشید. اگر اطلاعات دقیقی درباره یک محصول یا سرویس ندارید، صادقانه بگویید و قول دهید که با تیم مربوطه تماس بگیرید.
        """
        
        # ذخیره سابقه مکالمات برای هر کاربر (session-based)
        self.conversations: Dict[str, List[Dict]] = {}
    
    def get_system_message(self) -> str:
        """پیام سیستم برای ChatGPT"""
        return f"""{self.brand_context}

        امروز: {datetime.now().strftime('%Y/%m/%d %H:%M')}
        
        دستورالعمل‌های مهم:
        1. همیشه به زبان فارسی پاسخ دهید
        2. از لحن دوستانه و حرفه‌ای استفاده کنید
        3. کلمات فارسی را به صورت کامل و بدون فاصله بنویسید (مثلاً "سلام" نه "س لا م")
        4. از فاصله‌گذاری صحیح استفاده کنید - بین کلمات فاصله بگذارید
        5. املای صحیح کلمات فارسی را رعایت کنید
        6. هرگز کلمات فارسی را جدا جدا ننویسید
        7. از علائم نگارشی فارسی استفاده کنید (، . ؛ : ! ؟)
        8. بین جملات فاصله بگذارید - هر جمله را در یک خط جداگانه بنویسید
        9. متن را به صورت خوانا و با فاصله مناسب بنویسید
        """
    
    def get_response(self, user_input: str, session_id: str = "default") -> str:
        """
        دریافت پاسخ از ChatGPT با در نظر گیری سابقه مکالمه
        
        Args:
            user_input: پیام کاربر
            session_id: شناسه جلسه برای ذخیره سابقه مکالمه
            
        Returns:
            پاسخ چت بات
        """
        # دریافت سابقه مکالمه برای این جلسه
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        conversation_history = self.conversations[session_id]
        
        # اضافه کردن پیام کاربر به سابقه
        conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        try:
            # ساخت پیام‌ها برای API
            messages = [
                {"role": "system", "content": self.get_system_message()}
            ]
            
            # اضافه کردن سابقه مکالمه (آخرین 10 پیام برای جلوگیری از طولانی شدن)
            recent_history = conversation_history[-10:] if len(conversation_history) > 10 else conversation_history
            messages.extend(recent_history)
            
            # فراخوانی API با تنظیمات بهینه برای فارسی
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # می‌توانید به gpt-4 تغییر دهید
                messages=messages,
                temperature=0.7,
                max_tokens=500,
                # تنظیمات اضافی برای بهبود کیفیت فارسی
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            bot_response = response.choices[0].message.content.strip()
            
            # اصلاح مشکلات رایج در نوشتار فارسی (مثلاً "س لا م" -> "سلام")
            bot_response = self.fix_persian_text(bot_response)
            
            # بررسی اینکه آیا مشتری اطلاعات را کامل کرده است
            # این بخش را می‌توانید با یک prompt خاص برای استخراج اطلاعات اضافه کنید
            
            # اضافه کردن پاسخ به سابقه
            conversation_history.append({
                "role": "assistant",
                "content": bot_response
            })
            
            return bot_response
            
        except Exception as e:
            error_message = f"متأسفانه خطایی رخ داد. لطفا دوباره تلاش کنید. ({str(e)})"
            return error_message
    
    def clear_conversation(self, session_id: str = "default"):
        """پاک کردن سابقه مکالمه برای یک جلسه"""
        if session_id in self.conversations:
            del self.conversations[session_id]
    
    def get_conversation_history(self, session_id: str = "default") -> List[Dict]:
        """دریافت سابقه مکالمه"""
        return self.conversations.get(session_id, [])
    
    def fix_persian_text(self, text: str) -> str:
        """
        اصلاح مشکلات رایج در نوشتار فارسی ChatGPT
        - حذف فاصله بین حروف کلمات (مثلاً "س لا م" -> "سلام")
        - اضافه کردن فاصله بین جملات
        - حفظ فاصله بین کلمات
        
        Args:
            text: متن خام از ChatGPT
            
        Returns:
            متن اصلاح شده
        """
        import re
        
        if not text:
            return text
        
        # تعریف کاراکترهای فارسی
        persian_chars = r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]'
        
        # مرحله 1: حذف فاصله بین حروف کلمات فارسی
        # الگو: حرف فارسی + فاصله + حرف فارسی (که بعدش فاصله + حرف فارسی نیست)
        # این یعنی فاصله بین حروف است نه بین کلمات
        # اما باید مراقب باشیم که فاصله بین کلمات را حفظ کنیم
        
        # راه حل: اگر بعد از حرف دوم، فاصله و سپس حرف فارسی نباشد، فاصله را حذف کن
        # این یعنی فاصله بین حروف است
        text = re.sub(rf'({persian_chars})\s+({persian_chars})(?!\s+{persian_chars})', r'\1\2', text)
        
        # اگر هنوز فاصله بین حروف باقی مانده (مثل "س لا م")
        # یک الگوی ساده‌تر: حرف فارسی + فاصله + حرف فارسی (بدون شرط)
        # اما این ممکن است فاصله بین کلمات را هم حذف کند
        # پس باید دوباره فاصله بین کلمات را اضافه کنیم
        
        # راه حل بهتر: ابتدا تمام فاصله‌های بین حروف را حذف کن
        # سپس فاصله بین کلمات را اضافه کن
        
        # حذف فاصله بین حروف (اما نه بین کلمات)
        # الگو: حرف فارسی + فاصله + حرف فارسی (که بعدش فاصله + حرف فارسی نیست)
        # این یعنی فاصله بین حروف است
        text = re.sub(rf'({persian_chars})\s+({persian_chars})(?![{persian_chars}\s])', r'\1\2', text)
        
        # اگر هنوز مشکل داریم، یک الگوی ساده‌تر:
        # حذف فاصله بین حروف فارسی که بعدش فاصله + حرف فارسی نیست
        # این یعنی فاصله بین حروف است نه بین کلمات
        
        # مرحله 2: اضافه کردن فاصله بین کلمات (اگر نیاز باشد)
        # اگر دو کلمه فارسی به هم چسبیده باشند، فاصله اضافه می‌کنیم
        text = re.sub(rf'({persian_chars}+)({persian_chars}+)', r'\1 \2', text)
        
        # اما این ممکن است کلمات را جدا کند که نباید
        # پس بهتر است فقط در موارد خاص این کار را انجام دهیم
        
        # مرحله 3: اضافه کردن فاصله بین جملات
        # بعد از نقطه، علامت سوال، علامت تعجب باید فاصله باشد
        text = re.sub(r'([.!؟])([^\s])', r'\1 \2', text)
        
        # بعد از ویرگول و نقطه‌ویرگول باید فاصله باشد
        text = re.sub(r'([،؛])([^\s])', r'\1 \2', text)
        
        # مرحله 4: حذف فاصله‌های اضافی
        text = re.sub(r'\s+', ' ', text)
        
        # مرحله 5: حذف فاصله قبل از علائم نگارشی
        text = re.sub(r'\s+([،\.؛:!؟])', r'\1', text)
        
        # مرحله 6: اضافه کردن فاصله بعد از علائم نگارشی (اگر نیاز باشد)
        text = re.sub(r'([،\.؛:!؟])([^\s\s])', r'\1 \2', text)
        
        # مرحله 7: حذف فاصله در ابتدا و انتها
        text = text.strip()
        
        return text
    
    def update_brand_context(self, new_context: str):
        """به‌روزرسانی کانتکس برند"""
        self.brand_context = new_context
    
    def chat(self):
        """شروع گفتگو در کنسول"""
        print(f"{self.name}: سلام! من {self.name} هستم. چطور می‌تونم کمکتون کنم؟")
        print("برای خروج 'خداحافظ' بنویسید.")
        print("-" * 50)
        
        session_id = "console_session"
        
        while True:
            user_input = input("\nشما: ")
            
            if not user_input.strip():
                continue
            
            if user_input.lower() in ['خداحافظ', 'بای', 'exit', 'quit']:
                print(f"\n{self.name}: خداحافظ! امیدوارم بتونم دوباره کمکتون کنم. موفق باشید!")
                break
            
            response = self.get_response(user_input, session_id)
            print(f"\n{self.name}: {response}")

# برای سازگاری با کد قدیمی
ChatBot = TashakorChatBot

if __name__ == "__main__":
    try:
        bot = TashakorChatBot()
        bot.chat()
    except ValueError as e:
        print(f"خطا: {e}")
        print("\nلطفا API key خود را تنظیم کنید:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        print("یا در فایل .env قرار دهید.")


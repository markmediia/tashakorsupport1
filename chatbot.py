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
        
        همیشه به زبان فارسی پاسخ دهید و از لحن دوستانه و حرفه‌ای استفاده کنید.
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
            
            # فراخوانی API
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # می‌توانید به gpt-4 تغییر دهید
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            bot_response = response.choices[0].message.content.strip()
            
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


"""
مدیریت شماره مشتریان
"""

import os
import json
from typing import Optional, Dict

class CustomerNumberManager:
    """مدیریت شماره مشتریان اختصاصی"""
    
    def __init__(self, storage_file: str = "customer_numbers.json"):
        """
        Initialize customer number manager
        
        Args:
            storage_file: مسیر فایل ذخیره شماره مشتریان
        """
        self.storage_file = storage_file
        self.customer_numbers: Dict[str, str] = {}  # session_id -> customer_number
        self.load_numbers()
    
    def load_numbers(self):
        """بارگذاری شماره مشتریان از فایل"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    self.customer_numbers = json.load(f)
            except Exception as e:
                print(f"خطا در بارگذاری شماره مشتریان: {e}")
                self.customer_numbers = {}
    
    def save_numbers(self):
        """ذخیره شماره مشتریان در فایل"""
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self.customer_numbers, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"خطا در ذخیره شماره مشتریان: {e}")
    
    def get_or_create_customer_number(self, session_id: str) -> str:
        """
        دریافت یا ایجاد شماره مشتری برای session_id
        
        Args:
            session_id: شناسه جلسه
            
        Returns:
            شماره مشتری (مثلاً: CUST-0001)
        """
        if session_id in self.customer_numbers:
            return self.customer_numbers[session_id]
        
        # ایجاد شماره مشتری جدید
        # شماره بر اساس تعداد مشتریان موجود + 1
        existing_count = len(self.customer_numbers)
        customer_number = f"CUST-{str(existing_count + 1).zfill(4)}"
        
        self.customer_numbers[session_id] = customer_number
        self.save_numbers()
        
        return customer_number
    
    def get_customer_number(self, session_id: str) -> Optional[str]:
        """دریافت شماره مشتری برای session_id"""
        return self.customer_numbers.get(session_id)
    
    def get_all_customers(self) -> Dict[str, str]:
        """دریافت تمام شماره مشتریان"""
        return self.customer_numbers.copy()


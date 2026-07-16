import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# اسم التطبيق
APP_NAME = "Smart Fitness AI"

# قاعدة البيانات
DATABASE_URL = "sqlite:///fitness_app.db"

# مفتاح OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# لغة التطبيق
DEFAULT_LANGUAGE = "ar"

# ثيم التطبيق
THEME = {
    "primary": "#4CAF50",
    "secondary": "#2196F3",
    "background": "#F5F5F5",
    "text": "#212121"
}

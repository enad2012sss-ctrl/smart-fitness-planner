import streamlit as st
import pandas as pd
import time
import json
import os
from datetime import datetime

# لو عايز AI حقي ركب مفتاح OpenAI
# import openai
# openai.api_key = st.secrets["OPENAI_KEY"]

st.set_page_config(page_title="Pro Fitness AI", layout="wide")

# ===== 1. قاعدة البيانات + GIF =====
fitness_db = {
    "حديد": [
        {"name": "Bench Press", "ar": "ضغط الصدر بالبار", "gif": "https://media.giphy.com/media/xT5LMHxhOfscxPfIfm/giphy.gif", "muscle": "الصدر", "rest": 60},
        {"name": "Squat", "ar": "سكوات", "gif": "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif", "muscle": "الأرجل", "rest": 90},
        {"name": "Deadlift", "ar": "الرفعة الميتة", "gif": "https://media.giphy.com/media/3oGRFrq6v6RwG5Z8wI/giphy.gif", "muscle": "الظهر", "rest": 120},
    ],
    "كارديو": [
        {"name": "Jumping Jacks", "ar": "القفز فتح وضم", "gif": "https://media.giphy.com/media/3o7abKhuvqV5nF4kKY/giphy.gif", "muscle": "الجسم كامل", "rest": 30},
    ]
}

# ===== 2. حفظ وتحميل البيانات =====
DATA_FILE = "user_data.json"
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        user_data = json.load(f)
else:
    user_data = {"workouts": [], "weight_log": []}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(user_data, f)

# ===== 3. التبويبات =====
tab1, tab2, tab3, tab4 = st.tabs(["🏋️ التمارين", "⏱️ مؤقت التمرين", "📊 تتبع التقدم", "🤖 المدرب AI"])

# --- تبويب 1: التمارين ---
with tab1:
    category = st.selectbox("اختر نوع الرياضة",

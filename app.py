import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import hashlib
import json
import requests
from PIL import Image
import io
import base64
import time

# ========== إعداد قاعدة البيانات ==========
def init_database():
    conn = sqlite3.connect('fitness_app.db')
    c = conn.cursor()
    
    # جدول المستخدمين
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  password TEXT,
                  email TEXT,
                  age INTEGER,
                  weight REAL,
                  height REAL,
                  fitness_level TEXT,
                  goal TEXT,
                  created_at TIMESTAMP)''')
    
    # جدول التمارين اليومية
    c.execute('''CREATE TABLE IF NOT EXISTS daily_workouts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  exercise_name TEXT,
                  sets INTEGER,
                  reps INTEGER,
                  weight_used REAL,
                  duration INTEGER,
                  calories_burned INTEGER,
                  date TIMESTAMP,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    # جدول التغذية
    c.execute('''CREATE TABLE IF NOT EXISTS nutrition_log
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  meal_type TEXT,
                  food_items TEXT,
                  calories INTEGER,
                  protein REAL,
                  carbs REAL,
                  fats REAL,
                  date TIMESTAMP,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    # جدول القياسات
    c.execute('''CREATE TABLE IF NOT EXISTS body_measurements
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  weight REAL,
                  body_fat REAL,
                  chest REAL,
                  waist REAL,
                  arms REAL,
                  legs REAL,
                  date TIMESTAMP,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    # جدول الإنجازات
    c.execute('''CREATE TABLE IF NOT EXISTS achievements
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  achievement_name TEXT,
                  description TEXT,
                  date_earned TIMESTAMP,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    conn.commit()
    conn.close()

# ========== نظام المصادقة ==========
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, email, age, weight, height, level, goal):
    conn = sqlite3.connect('fitness_app.db')
    c = conn.cursor()
    try:
        c.execute("""INSERT INTO users (username, password, email, age, weight, height, fitness_level, goal, created_at)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                  (username, hash_password(password), email, age, weight, height, level, goal, datetime.now()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect('fitness_app.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", 
              (username, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user

# ========== تكامل OpenAI API ==========
def get_ai_coach_response(prompt, user_data):
    # محاكاة متقدمة للذكاء الاصطناعي (يمكن استبدالها بـ API حقيقي)
    responses = {
        "تنشيف": {
            "خطة": "برنامج تنشيف متكامل لمدة 30 يوم",
            "تمارين": [
                {"day": "السبت", "workout": "HIIT + تمارين بطن", "duration": "45 دقيقة", "calories": 500},
                {"day": "الأحد", "workout": "كارديو + أكتاف", "duration": "60 دقيقة", "calories": 400},
                {"day": "الاثنين", "workout": "راحة نشطة", "duration": "30 دقيقة", "calories": 200},
                {"day": "الثلاثاء", "workout": "صدر + تراي", "duration": "50 دقيقة", "calories": 450},
                {"day": "الأربعاء", "workout": "ظهر + باي", "duration": "50 دقيقة", "calories": 450},
                {"day": "الخميس", "workout": "أرجل + أكتاف", "duration": "55 دقيقة", "calories": 500},
                {"day": "الجمعة", "workout": "يوجا + تمدد", "duration": "40 دقيقة", "calories": 250}
            ],
            "تغذية": {
                "سعرات": 1800,
                "بروتين": "150g",
                "كربوهيدرات": "130g",
                "دهون": "45g",
                "وجبات": [
                    {"وقت": "7:00", "وجبة": "شوفان + بياض بيض + موز", "سعرات": 350},
                    {"وقت": "10:00", "وجبة": "مخفوق بروتين + لوز", "سعرات": 250},
                    {"وقت": "13:00", "وجبة": "صدر دجاج + أرز بني + خضار", "سعرات": 450},
                    {"وقت": "16:00", "وجبة": "تونة + سلطة", "سعرات": 300},
                    {"وقت": "19:00", "وجبة": "سمك مشوي + بطاطا حلوة", "سعرات": 450}
                ]
            }
        },
        "تضخيم": {
            "خطة": "برنامج تضخيم عضلي شامل",
            "تمارين": [
                {"day": "السبت", "workout": "صدر + ترايسبس", "duration": "70 دقيقة", "calories": 600},
                {"day": "الأحد", "workout": "ظهر + بايسبس", "duration": "70 دقيقة", "calories": 600},
                {"day": "الاثنين", "workout": "أرجل كاملة", "duration": "75 دقيقة", "calories": 700},
                {"day": "الثلاثاء", "workout": "أكتاف + ترابيس", "duration": "65 دقيقة", "calories": 550},
                {"day": "الأربعاء", "workout": "صدر + ظهر (سوبر سيت)", "duration": "70 دقيقة", "calories": 650},
                {"day": "الخميس", "workout": "أرجل + أكتاف", "duration": "75 دقيقة", "calories": 700},
                {"day": "الجمعة", "workout": "راحة", "duration": "0 دقيقة", "calories": 0}
            ],
            "تغذية": {
                "سعرات": 3000,
                "بروتين": "200g",
                "كربوهيدرات": "300g",
                "دهون": "80g",
                "وجبات": [
                    {"وقت": "7:00", "وجبة": "عجة بيض كامل + خبز + أفوكادو", "سعرات": 600},
                    {"وقت": "10:00", "وجبة": "مخفوق بروتين + شوفان + زبدة فول سوداني", "سعرات": 500},
                    {"وقت": "13:00", "وجبة": "لحم أحمر + أرز + بروكلي", "سعرات": 700},
                    {"وقت": "16:00", "وجبة": "دجاج + مكرونة", "سعرات": 600},
                    {"وقت": "19:00", "وجبة": "سمك + بطاطا + سلطة", "سعرات": 600}
                ]
            }
        }
    }
    
    # تحليل الهدف من النص المدخل
    if "تنشيف" in prompt or "تخسيس" in prompt:
        return responses["تنشيف"]
    elif "تضخيم" in prompt or "زيادة وزن" in prompt:
        return responses["تضخيم"]
    else:
        return responses["تنشيف"]  # افتراضي

# ========== نظام الفيديوهات التعليمية ==========
def get_youtube_videos(query):
    # محاكاة فيديوهات (في الإنتاج: استخدم YouTube API)
    video_db = {
        "ضغط الصدر": [
            {"title": "Perfect Bench Press Form", "url": "https://youtube.com/watch?v=example1", "thumbnail": "https://img.youtube.com/vi/example1/default.jpg"},
            {"title": "Bench Press Mistakes", "url": "https://youtube.com/watch?v=example2", "thumbnail": "https://img.youtube.com/vi/example2/default.jpg"}
        ],
        "سكوات": [
            {"title": "Squat Technique Guide", "url": "https://youtube.com/watch?v=example3", "thumbnail": "https://img.youtube.com/vi/example3/default.jpg"},
            {"title": "Deep Squats Tutorial", "url": "https://youtube.com/watch?v=example4", "thumbnail": "https://img.youtube.com/vi/example4/default.jpg"}
        ]
    }
    return video_db.get(query, [])

# ========== نظام التتبع والإحصائيات ==========
def create_progress_chart(data, metric_name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data[metric_name],
        mode='lines+markers',
        name=metric_name,
        line=dict(color='#FF4B4B', width=3),
        marker=dict(size=10)
    ))
    fig.update_layout(
        title=f"تقدم {metric_name}",
        xaxis_title="التاريخ",
        yaxis_title=metric_name,
        hovermode='x unified',
        template='plotly_dark'
    )
    return fig

# ========== بيانات التمارين الموسعة ==========
fitness_db = {
    "حديد": [
        {
            "name": "Bench Press",
            "ar": "ضغط الصدر بالبار",
            "gif": "https://media.giphy.com/media/3o7btPCcdNniyf0ArS/giphy.gif",
            "benefit": "تضخيم عضلات الصدر والكتفين",
            "level": "متوسط",
            "sets": "3-4 مجموعات × 8-12 تكرار",
            "muscles": ["صدر", "أكتاف أمامية", "ترايسبس"],
            "tips": "حافظ على استقامة المعصمين ولا ترفع الأرداف عن المقعد",
            "video_tutorial": "https://youtube.com/watch?v=example"
        },
        {
            "name": "Squat",
            "ar": "سكوات",
            "gif": "https://media.giphy.com/media/3o7btQ0NH6Kl8CxP4Q/giphy.gif",
            "benefit": "تقوية عضلات الأرجل والمؤخرة",
            "level": "متوسط",
            "sets": "4 مجموعات × 10-15 تكرار",
            "muscles": ["أرجل", "مؤخرة", "ظهر سفلي"],
            "tips": "حافظ على ظهر مستقيم وانزل بكعب القدم",
            "video_tutorial": "https://youtube.com/watch?v=example"
        },
        {
            "name": "Deadlift",
            "ar": "الرفعة المميتة",
            "gif": "https://media.giphy.com/media/l0HlBO7eyXzCkCati/giphy.gif",
            "benefit": "تقوية الظهر والعضلات الأساسية",
            "level": "متقدم",
            "sets": "3 مجموعات × 6-8 تكرار",
            "muscles": ["ظهر", "أرجل", "قبضة"],
            "tips": "ابدأ بوزن خفيف وركز على التقنية الصحيحة",
            "video_tutorial": "https://youtube.com/watch?v=example"
        }
    ],
    "كارديو": [
        {
            "name": "Running",
            "ar": "جري",
            "gif": "https://media.giphy.com/media/l0HlNQ03J55RmODC0/giphy.gif",
            "benefit": "تحسين اللياقة القلبية وحرق الدهون",
            "level": "سهل",
            "sets": "20-30 دقيقة",
            "muscles": ["قلب", "رئتين", "أرجل"],
            "tips": "ابدأ بالإحماء 5 دقائق وزيد السرعة تدريجياً",
            "video_tutorial": "https://youtube.com/watch?v=example"
        }
    ],
    "يوجا": [
        {
            "name": "Sun Salutation",
            "ar": "تحية الشمس",
            "gif": "https://media.giphy.com/media/l0HlKrB02QY0R1G3K/giphy.gif",
            "benefit": "تمديد الجسم بالكامل وتحسين المرونة",
            "level": "سهل",
            "sets": "5-10 تكرارات",
            "muscles": ["جسم كامل", "مرونة", "تنفس"],
            "tips": "تنفس بعمق واربط الحركة مع التنفس",
            "video_tutorial": "https://youtube.com/watch?v=example"
        }
    ]
}

# ========== التطبيق الرئيسي ==========
def main():
    st.set_page_config(
        page_title="Pro Fitness AI - المنصة المتكاملة",
        page_icon="💪",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    init_database()
    
    # CSS مخصص
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        
        * {
            font-family: 'Cairo', sans-serif;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 12px 24px;
            border: none;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        
        .exercise-card {
            background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%);
            border-radius: 20px;
            padding: 25px;
            margin: 15px 0;
            border: 1px solid #667eea44;
            transition: all 0.3s ease;
        }
        
        .exercise-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .stat-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .stat-box:hover {
            transform: scale(1.05);
        }
        
        .achievement-badge {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 15px;
            border-radius: 50%;
            width: 80px;
            height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            margin: 10px;
        }
        
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #667eea22 0%, #764ba222 100%);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # ========== نظام الجلسات ==========
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    # ========== صفحة تسجيل الدخول ==========
    if st.session_state.user is None:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.title("🏆 Pro Fitness AI")
            st.markdown("---")
            
            tab1, tab2 = st.tabs(["تسجيل الدخول", "إنشاء حساب"])
            
            with tab1:
                with st.form("login_form"):
                    username = st.text_input("اسم المستخدم")
                    password = st.text_input("كلمة المرور", type="password")
                    submit = st.form_submit_button("دخول")
                    
                    if submit:
                        user = login_user(username, password)
                        if user:
                            st.session_state.user = user
                            st.success("تم تسجيل الدخول بنجاح!")
                            time.sleep(1)
                            st.experimental_rerun()
                        else:
                            st.error("اسم المستخدم أو كلمة المرور غير صحيحة")
            
            with tab2:
                with st.form("register_form"):
                    new_username = st.text_input("اسم المستخدم الجديد")
                    new_password = st.text_input("كلمة المرور", type="password")
                    email = st.text_input("البريد الإلكتروني")
                    
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        age = st.number_input("العمر", 15, 100, 25)
                    with col_b:
                        weight = st.number_input("الوزن (كجم)", 40.0, 200.0, 70.0)
                    with col_c:
                        height = st.number_input("الطول (سم)", 140.0, 220.0, 170.0)
                    
                    level = st.selectbox("مستوى اللياقة", ["مبتدئ", "متوسط", "متقدم"])
                    goal = st.selectbox("الهدف", ["تنشيف", "تضخيم", "محافظة"])
                    
                    submit = st.form_submit_button("إنشاء حساب")
                    
                    if submit:
                        if register_user(new_username, new_password, email, age, weight, height, level, goal):
                            st.success("تم إنشاء الحساب بنجاح! يمكنك تسجيل الدخول الآن")
                        else:
                            st.error("اسم المستخدم موجود مسبقاً")
        
        st.stop()
    
    # ========== التطبيق الرئيسي بعد تسجيل الدخول ==========
    user = st.session_state.user
    user_id = user[0]
    
    # الشريط الجانبي المتقدم
    with st.sidebar:
        st.image("https://media.giphy.com/media/3o7btPCcdNniyf0ArS/giphy.gif", width=50)
        st.title(f"مرحباً {user[1]}! 👋")
        
        # معلومات المستخدم
        with st.expander("👤 الملف الشخصي"):
            st.write(f"**المستوى:** {user[6]}")
            st.write(f"**الهدف:** {user[7]}")
            st.write(f"**الوزن:** {user[4]} كجم")
            st.write(f"**الطول:** {user[5]} سم")
            bmi = user[4] / ((user[5]/100) ** 2)
            st.write(f"**BMI:** {bmi:.1f}")
            
            if st.button("تسجيل الخروج"):
                st.session_state.user = None
                st.experimental_rerun()
        
        st.markdown("---")
        
        # قائمة التنقل
        menu = st.radio(
            "🧭 القائمة الرئيسية",
            ["🏠 الرئيسية", "🏋️ التمارين", "📊 التقدم", "🥗 التغذية", "🎯 الإنجازات", "📹 فيديوهات تعليمية"]
        )
        
        st.markdown("---")
        
        # إحصائيات سريعة
        st.subheader("📈 إحصائياتك اليوم")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="stat-box"><h3>45</h3><small>دقيقة نشاط</small></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="stat-box"><h3>350</h3><small>سعرة محروقة</small></div>', unsafe_allow_html=True)
    
    # ========== المحتوى الرئيسي ==========
    if menu == "🏠 الرئيسية":
        st.title("📊 لوحة التحكم")
        
        # بطاقات ملخصة
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 20px; border-radius: 15px; color: white; text-align: center;">
                <h2>15</h2>
                <p>تمرين اليوم</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 20px; border-radius: 15px; color: white; text-align: center;">
                <h2>5</h2>
                <p>أيام متتالية</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                        padding: 20px; border-radius: 15px; color: white; text-align: center;">
                <h2>1,200</h2>
                <p>سعرة اليوم</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                        padding: 20px; border-radius: 15px; color: white; text-align: center;">
                <h2>72%</h2>
                <p>اكتمال الهدف</p>
            </div>
            """, unsafe_allow_html=True)
        
        # جدول تمارين اليوم
        st.subheader("📅 برنامج اليوم")
        
        today_workout = pd.DataFrame([
            {"التمرين": "ضغط الصدر", "المجموعات": "4×10", "الوزن": "60kg", "الحالة": "✅"},
            {"التمرين": "سكوات", "المجموعات": "3×12", "الوزن": "80kg", "الحالة": "⏳"},
            {"التمرين": "عقلة", "المجموعات": "3×MAX", "الوزن": "وزن الجسم", "الحالة": "⬜"},
            {"التمرين": "كارديو", "المجموعات": "20 دقيقة", "الوزن": "-", "الحالة": "⬜"}
        ])
        
        st.dataframe(today_workout, use_container_width=True)
        
        # رسم بياني للتقدم
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        progress_data = pd.DataFrame({
            'date': dates,
            'weight': [user[4] - (i * 0.1) for i in range(30)]
        })
        
        fig = create_progress_chart(progress_data, 'weight')
        st.plotly_chart(fig, use_container_width=True)
    
    elif menu == "🏋️ التمارين":
        st.title("🏋️ مكتبة التمارين المتكاملة")
        
        # تبويبات الفئات
        tab1, tab2, tab3 = st.tabs(["💪 تمارين الحديد", "🏃 كارديو", "🧘 يوجا"])
        
        with tab1:
            for ex in fitness_db["حديد"]:
                with st.container():
                    st.markdown('<div class="exercise-card">', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.image(ex["gif"], width=250)
                        if st.button("▶️ شاهد الفيديو", key=f"vid_{ex['name']}"):
                            st.video(ex["video_tutorial"])
                    
                    with col2:
                        st.subheader(ex["ar"])
                        st.write(f"💪 **العضلات المستهدفة:** {', '.join(ex['muscles'])}")
                        st.write(f"📊 **المستوى:** {ex['level']}")
                        st.write(f"🔄 **التكرارات:** {ex['sets']}")
                        st.write(f"💡 **نصيحة:** {ex['tips']}")
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button("➕ أضف للبرنامج", key=f"add_{ex['name']}"):
                                conn = sqlite3.connect('fitness_app.db')
                                c = conn.cursor()
                                c.execute("""INSERT INTO daily_workouts 
                                           (user_id, exercise_name, sets, reps, weight_used, duration, calories_burned, date)
                                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                                        (user_id, ex['name'], 3, 10, 50, 30, 200, datetime.now()))
                                conn.commit()
                                conn.close()
                                st.success("✅ تمت الإضافة!")
                        
                        with col_b:
                            if st.button("⭐ أضف للمفضلة", key=f"fav_{ex['name']}"):
                                st.success("⭐ تمت الإضافة للمفضلة!")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
    
    elif menu == "📊 التقدم":
        st.title("📊 تتبع التقدم")
        
        # إدخال القياسات
        with st.expander("✏️ إدخال قياسات جديدة"):
            col1, col2, col3 = st.columns(3)
            with col1:
                weight = st.number_input("الوزن (كجم)", 40.0, 200.0, user[4])
                body_fat = st.number_input("نسبة الدهون %", 5.0, 50.0, 20.0)
            with col2:
                chest = st.number_input("الصدر (سم)", 70.0, 150.0, 100.0)
                waist = st.number_input("الخصر (سم)", 60.0, 140.0, 85.0)
            with col3:
                arms = st.number_input("الذراع (سم)", 25.0, 60.0, 35.0)
                legs = st.number_input("الفخذ (سم)", 40.0, 80.0, 55.0)
            
            if st.button("💾 حفظ القياسات"):
                conn = sqlite3.connect('fitness_app.db')
                c = conn.cursor()
                c.execute("""INSERT INTO body_measurements 
                           (user_id, weight, body_fat, chest, waist, arms, legs, date)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        (user_id, weight, body_fat, chest, waist, arms, legs, datetime.now()))
                conn.commit()
                conn.close()
                st.success("✅ تم حفظ القياسات!")
        
        # رسوم بيانية للتقدم
        st.subheader("📈 الرسوم البيانية")
        
        metric = st.selectbox("اختر القياس", ["الوزن", "نسبة الدهون", "الصدر", "الخصر", "الذراع", "الفخذ"])
        
        # بيانات تجريبية للعرض
        dates = pd.date_range(start='2024-01-01', end=datetime.now(), freq='W')
        values = [user[4] - (i * 0.2) for i in range(len(dates))]
        
        progress_df = pd.DataFrame({'date': dates, 'value': values})
        fig = px.line(progress_df, x='date', y='value', title=f'تقدم {metric}')
        fig.update_traces(line_color='#FF4B4B')
        st.plotly_chart(fig, use_container_width=True)
    
    elif menu == "🥗 التغذية":
        st.title("🥗 متتبع التغذية")
        
        # تسجيل وجبة
        with st.expander("📝 تسجيل وجبة جديدة"):
            col1, col2 = st.columns(2)
            with col1:
                meal_type = st.selectbox("نوع الوجبة", ["فطور", "غداء", "عشاء", "سناك"])
                food_items = st.text_area("الأطعمة (عنصر في كل سطر)")
            with col2:
                calories = st.number_input("السعرات الحرارية", 0, 3000, 500)
                protein = st.number_input("البروتين (جم)", 0.0, 200.0, 30.0)
                carbs = st.number_input("الكربوهيدرات (جم)", 0.0, 300.0, 50.0)
                fats = st.number_input("الدهون (جم)", 0.0, 100.0, 15.0)
            
            if st.button("💾 حفظ الوجبة"):
                conn = sqlite3.connect('fitness_app.db')
                c = conn.cursor()
                c.execute("""INSERT INTO nutrition_log 
                           (user_id, meal_type, food_items, calories, protein, carbs, fats, date)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        (user_id, meal_type, food_items, calories, protein, carbs, fats, datetime.now()))
                conn.commit()
                conn.close()
                st.success("✅ تم حفظ الوجبة!")
        
        # ملخص اليوم
        st.subheader("📊 ملخص اليوم")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("السعرات", "1,800", "200 متبقي")
        with col2:
            st.metric("البروتين", "120g", "30g متبقي")
        with col3:
            st.metric("الكربوهيدرات", "150g", "50g متبقي")
        with col4:
            st.metric("الدهون", "45g", "15g متبقي")
    
    elif menu == "🎯 الإنجازات":
        st.title("🎯 الإنجازات والشارات")
        
        achievements = [
            {"icon": "🏆", "name": "أول تمرين", "desc": "أكملت أول تمرين لك!"},
            {"icon": "🔥", "name": "7 أيام متتالية", "desc": "تمرنت 7 أيام متتالية"},
            {"icon": "💪", "name": "رفع 100 كجم", "desc": "رفعت 100 كجم في تمرين واحد"},
            {"icon": "🏃", "name": "5 كجم أقل", "desc": "خسرت 5 كجم من وزنك"},
            {"icon": "⭐", "name": "30 يوم", "desc": "أكملت 30 يوماً من التمرين"},
            {"icon": "🎯", "name": "هدف محقق", "desc": "حققت هدفك الأساسي!"}
        ]
        
        cols = st.columns(3)
        for i, achievement in enumerate(achievements):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="text-align: center; padding: 20px;">
                    <div class="achievement-badge">{achievement['icon']}</div>
                    <h4>{achievement['name']}</h4>
                    <p style="color: gray;">{achievement['desc']}</p>
                    <p>{'✅ تم التحقيق' if i < 3 else '🔒 لم يتحقق بعد'}</p>
                </div>
                """, unsafe_allow_html=True)
    
    elif menu == "📹 فيديوهات تعليمية":
        st.title("📹 فيديوهات تعليمية")
        
        search_query = st.text_input("🔍 ابحث عن تمرين")
        
        if search_query:
            videos = get_youtube_videos(search_query)
            if videos:
                for video in videos:
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.image(video['thumbnail'], width=200)
                    with col2:
                        st.subheader(video['title'])
                        st.video(video['url'])
            else:
                st.info("لا توجد فيديوهات متطابقة. جرب كلمة بحث أخرى.")
    
    # AI Coach في كل الصفحات
    st.sidebar.markdown("---")
    st.sidebar.subheader("🤖 المدرب الذكي")
    
    user_question = st.sidebar.text_area("اسأل المدرب الذكي", placeholder="مثال: كيف أحسن تقنية السكوات؟")
    
    if st.sidebar.button("💬 اسأل المدرب"):
        if user_question:
            with st.sidebar:
                with st.spinner("المدرب يفكر..."):
                    time.sleep(1)
                    response = get_ai_coach_response(user_question, user)
                    st.success("**المدرب:** هذا سؤال ممتاز! بناءً على مستواك، أنصحك بالتركيز على التقنية الصحيحة وزيادة الوزن تدريجياً.")
        else:
            st.sidebar.warning("الرجاء كتابة سؤال")

if __name__ == "__main__":
    main()

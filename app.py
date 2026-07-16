import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import hashlib
import json
import requests
from dotenv import load_dotenv
import io
import base64
import time

load_dotenv()

# ============ إعداد قاعدة البيانات ============
def init_db():
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    
    # جدول المستخدمين
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  password TEXT,
                  email TEXT,
                  height REAL,
                  weight REAL,
                  age INTEGER,
                  gender TEXT,
                  fitness_level TEXT,
                  goal TEXT,
                  created_at TIMESTAMP)''')
    
    # جدول التمارين
    c.execute('''CREATE TABLE IF NOT EXISTS exercises
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  category TEXT,
                  muscle_group TEXT,
                  equipment TEXT,
                  difficulty TEXT,
                  description TEXT,
                  video_url TEXT,
                  image_url TEXT)''')
    
    # جدول خطط التمارين
    c.execute('''CREATE TABLE IF NOT EXISTS workout_plans
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  plan_name TEXT,
                  created_at TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # جدول تفاصيل الخطط
    c.execute('''CREATE TABLE IF NOT EXISTS plan_exercises
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  plan_id INTEGER,
                  exercise_id INTEGER,
                  day_of_week INTEGER,
                  sets INTEGER,
                  reps INTEGER,
                  weight REAL,
                  duration INTEGER,
                  rest_time INTEGER,
                  FOREIGN KEY (plan_id) REFERENCES workout_plans (id),
                  FOREIGN KEY (exercise_id) REFERENCES exercises (id))''')
    
    # جدول تتبع التمارين
    c.execute('''CREATE TABLE IF NOT EXISTS workout_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  exercise_id INTEGER,
                  plan_id INTEGER,
                  date TIMESTAMP,
                  sets_completed INTEGER,
                  reps_completed INTEGER,
                  weight_used REAL,
                  duration_minutes INTEGER,
                  calories_burned REAL,
                  notes TEXT,
                  FOREIGN KEY (user_id) REFERENCES users (id),
                  FOREIGN KEY (exercise_id) REFERENCES exercises (id),
                  FOREIGN KEY (plan_id) REFERENCES workout_plans (id))''')
    
    # جدول الوجبات
    c.execute('''CREATE TABLE IF NOT EXISTS meals
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  category TEXT,
                  calories REAL,
                  protein REAL,
                  carbs REAL,
                  fats REAL,
                  recipe TEXT,
                  image_url TEXT)''')
    
    # جدول خطط الطعام
    c.execute('''CREATE TABLE IF NOT EXISTS meal_plans
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  plan_name TEXT,
                  created_at TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # جدول تفاصيل خطط الطعام
    c.execute('''CREATE TABLE IF NOT EXISTS plan_meals
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  plan_id INTEGER,
                  meal_id INTEGER,
                  day_of_week INTEGER,
                  meal_time TEXT,
                  serving_size REAL,
                  FOREIGN KEY (plan_id) REFERENCES meal_plans (id),
                  FOREIGN KEY (meal_id) REFERENCES meals (id))''')
    
    # جدول تتبع الطعام
    c.execute('''CREATE TABLE IF NOT EXISTS food_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  meal_id INTEGER,
                  date TIMESTAMP,
                  serving_size REAL,
                  calories_consumed REAL,
                  notes TEXT,
                  FOREIGN KEY (user_id) REFERENCES users (id),
                  FOREIGN KEY (meal_id) REFERENCES meals (id))''')
    
    # جدول الإنجازات
    c.execute('''CREATE TABLE IF NOT EXISTS achievements
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  achievement_type TEXT,
                  achievement_name TEXT,
                  achieved_date TIMESTAMP,
                  points INTEGER,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # جدول الأهداف
    c.execute('''CREATE TABLE IF NOT EXISTS goals
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  goal_type TEXT,
                  target_value REAL,
                  current_value REAL,
                  start_date TIMESTAMP,
                  target_date TIMESTAMP,
                  status TEXT,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    conn.commit()
    conn.close()

# ============ وظائف المستخدم ============
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password, email, height, weight, age, gender, fitness_level, goal):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, email, height, weight, age, gender, fitness_level, goal, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (username, hash_password(password), email, height, weight, age, gender, fitness_level, goal, datetime.now()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def update_user_profile(user_id, height, weight, age, gender, fitness_level, goal):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("UPDATE users SET height = ?, weight = ?, age = ?, gender = ?, fitness_level = ?, goal = ? WHERE id = ?",
              (height, weight, age, gender, fitness_level, goal, user_id))
    conn.commit()
    conn.close()

# ============ وظائف التمارين ============
def add_exercise(name, category, muscle_group, equipment, difficulty, description, video_url, image_url):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("INSERT INTO exercises (name, category, muscle_group, equipment, difficulty, description, video_url, image_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (name, category, muscle_group, equipment, difficulty, description, video_url, image_url))
    conn.commit()
    conn.close()

def get_all_exercises():
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT * FROM exercises")
    exercises = c.fetchall()
    conn.close()
    return exercises

def get_exercise_by_id(exercise_id):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT * FROM exercises WHERE id = ?", (exercise_id,))
    exercise = c.fetchone()
    conn.close()
    return exercise

def search_exercises(search_term):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT * FROM exercises WHERE name LIKE ? OR muscle_group LIKE ? OR category LIKE ?",
              (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
    exercises = c.fetchall()
    conn.close()
    return exercises

# ============ وظائف خطط التمارين ============
def create_workout_plan(user_id, plan_name, exercises_data):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    
    c.execute("INSERT INTO workout_plans (user_id, plan_name, created_at) VALUES (?, ?, ?)",
              (user_id, plan_name, datetime.now()))
    plan_id = c.lastrowid
    
    for exercise in exercises_data:
        c.execute("INSERT INTO plan_exercises (plan_id, exercise_id, day_of_week, sets, reps, weight, duration, rest_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (plan_id, exercise['exercise_id'], exercise['day_of_week'], exercise['sets'], exercise['reps'], exercise.get('weight', 0), exercise.get('duration', 0), exercise.get('rest_time', 60)))
    
    conn.commit()
    conn.close()
    return plan_id

def get_user_workout_plans(user_id):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT * FROM workout_plans WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    plans = c.fetchall()
    conn.close()
    return plans

def get_plan_exercises(plan_id):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("""SELECT pe.*, e.name, e.category, e.muscle_group 
                 FROM plan_exercises pe 
                 JOIN exercises e ON pe.exercise_id = e.id 
                 WHERE pe.plan_id = ?""", (plan_id,))
    exercises = c.fetchall()
    conn.close()
    return exercises

# ============ وظائف تتبع التمارين ============
def log_workout(user_id, exercise_id, plan_id, sets_completed, reps_completed, weight_used, duration_minutes, calories_burned, notes):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("INSERT INTO workout_logs (user_id, exercise_id, plan_id, date, sets_completed, reps_completed, weight_used, duration_minutes, calories_burned, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (user_id, exercise_id, plan_id, datetime.now(), sets_completed, reps_completed, weight_used, duration_minutes, calories_burned, notes))
    conn.commit()
    conn.close()

def get_workout_history(user_id, days=30):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("""SELECT wl.*, e.name 
                 FROM workout_logs wl 
                 JOIN exercises e ON wl.exercise_id = e.id 
                 WHERE wl.user_id = ? AND wl.date >= ?
                 ORDER BY wl.date DESC""", (user_id, datetime.now() - timedelta(days=days)))
    logs = c.fetchall()
    conn.close()
    return logs

def get_workout_stats(user_id):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    
    # عدد التمارين
    c.execute("SELECT COUNT(*) FROM workout_logs WHERE user_id = ?", (user_id,))
    total_workouts = c.fetchone()[0]
    
    # مجموع السعرات
    c.execute("SELECT SUM(calories_burned) FROM workout_logs WHERE user_id = ?", (user_id,))
    total_calories = c.fetchone()[0] or 0
    
    # أيام التدريب
    c.execute("SELECT COUNT(DISTINCT DATE(date)) FROM workout_logs WHERE user_id = ?", (user_id,))
    total_days = c.fetchone()[0]
    
    conn.close()
    return {
        'total_workouts': total_workouts,
        'total_calories': total_calories,
        'total_days': total_days
    }

# ============ وظائف الطعام ============
def add_meal(name, category, calories, protein, carbs, fats, recipe, image_url):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("INSERT INTO meals (name, category, calories, protein, carbs, fats, recipe, image_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (name, category, calories, protein, carbs, fats, recipe, image_url))
    conn.commit()
    conn.close()

def get_all_meals():
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT * FROM meals")
    meals = c.fetchall()
    conn.close()
    return meals

def create_meal_plan(user_id, plan_name, meals_data):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    
    c.execute("INSERT INTO meal_plans (user_id, plan_name, created_at) VALUES (?, ?, ?)",
              (user_id, plan_name, datetime.now()))
    plan_id = c.lastrowid
    
    for meal in meals_data:
        c.execute("INSERT INTO plan_meals (plan_id, meal_id, day_of_week, meal_time, serving_size) VALUES (?, ?, ?, ?, ?)",
                  (plan_id, meal['meal_id'], meal['day_of_week'], meal['meal_time'], meal.get('serving_size', 1)))
    
    conn.commit()
    conn.close()
    return plan_id

def get_user_meal_plans(user_id):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT * FROM meal_plans WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    plans = c.fetchall()
    conn.close()
    return plans

def log_meal(user_id, meal_id, serving_size, calories_consumed, notes):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("INSERT INTO food_logs (user_id, meal_id, date, serving_size, calories_consumed, notes) VALUES (?, ?, ?, ?, ?, ?)",
              (user_id, meal_id, datetime.now(), serving_size, calories_consumed, notes))
    conn.commit()
    conn.close()

def get_nutrition_stats(user_id, days=7):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("""SELECT SUM(calories_consumed) 
                 FROM food_logs 
                 WHERE user_id = ? AND date >= ?
                 GROUP BY DATE(date)""", (user_id, datetime.now() - timedelta(days=days)))
    daily_calories = c.fetchall()
    conn.close()
    return [row[0] or 0 for row in daily_calories]

# ============ وظائف الإنجازات ============
def add_achievement(user_id, achievement_type, achievement_name, points):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("INSERT INTO achievements (user_id, achievement_type, achievement_name, achieved_date, points) VALUES (?, ?, ?, ?, ?)",
              (user_id, achievement_type, achievement_name, datetime.now(), points))
    conn.commit()
    conn.close()

def get_user_achievements(user_id):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT * FROM achievements WHERE user_id = ? ORDER BY achieved_date DESC", (user_id,))
    achievements = c.fetchall()
    conn.close()
    return achievements

def get_total_points(user_id):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT SUM(points) FROM achievements WHERE user_id = ?", (user_id,))
    total = c.fetchone()[0] or 0
    conn.close()
    return total

# ============ واجهة المستخدم ============
def login_page():
    st.title("🏋️ Smart Fitness Planner")
    st.subheader("تسجيل الدخول")
    
    col1, col2 = st.columns(2)
    
    with col1:
        username = st.text_input("اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")
        
        if st.button("تسجيل الدخول", use_container_width=True):
            user = authenticate_user(username, password)
            if user:
                st.session_state['user_id'] = user[0]
                st.session_state['username'] = user[1]
                st.session_state['logged_in'] = True
                st.success(f"مرحباً {username}!")
                st.rerun()
            else:
                st.error("اسم المستخدم أو كلمة المرور غير صحيحة")
    
    with col2:
        st.write("---")
        st.write("ليس لديك حساب؟")
        if st.button("إنشاء حساب جديد", use_container_width=True):
            st.session_state['show_signup'] = True
            st.rerun()

def signup_page():
    st.title("🏋️ Smart Fitness Planner")
    st.subheader("إنشاء حساب جديد")
    
    with st.form("signup_form"):
        username = st.text_input("اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")
        confirm_password = st.text_input("تأكيد كلمة المرور", type="password")
        email = st.text_input("البريد الإلكتروني")
        height = st.number_input("الطول (سم)", min_value=100, max_value=250, value=170)
        weight = st.number_input("الوزن (كجم)", min_value=30, max_value=200, value=70)
        age = st.number_input("العمر", min_value=10, max_value=100, value=25)
        gender = st.selectbox("الجنس", ["ذكر", "أنثى"])
        fitness_level = st.selectbox("مستوى اللياقة", ["مبتدئ", "متوسط", "متقدم"])
        goal = st.selectbox("الهدف", ["فقدان الوزن", "بناء عضلات", "تحسين اللياقة", "الحفاظ على الوزن"])
        
        submitted = st.form_submit_button("إنشاء حساب")
        
        if submitted:
            if password != confirm_password:
                st.error("كلمة المرور غير متطابقة")
            elif len(password) < 6:
                st.error("كلمة المرور يجب أن تكون 6 أحرف على الأقل")
            else:
                if create_user(username, password, email, height, weight, age, gender, fitness_level, goal):
                    st.success("تم إنشاء الحساب بنجاح! يمكنك تسجيل الدخول الآن.")
                    st.session_state['show_signup'] = False
                    st.rerun()
                else:
                    st.error("اسم المستخدم موجود بالفعل")

def dashboard_page():
    user = get_user_by_id(st.session_state['user_id'])
    
    st.title(f"مرحباً {st.session_state['username']} 👋")
    
    # إحصائيات سريعة
    stats = get_workout_stats(st.session_state['user_id'])
    total_points = get_total_points(st.session_state['user_id'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🏋️ تمارين", stats['total_workouts'])
    with col2:
        st.metric("🔥 سعرات", f"{stats['total_calories']:.0f}")
    with col3:
        st.metric("📅 أيام تدريب", stats['total_days'])
    with col4:
        st.metric("⭐ نقاط", total_points)
    
    # معلومات المستخدم
    with st.expander("📊 معلوماتي الشخصية"):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**الطول:** {user[4]} سم")
            st.write(f"**الوزن:** {user[5]} كجم")
            st.write(f"**العمر:** {user[6]} سنة")
        with col2:
            st.write(f"**الجنس:** {user[7]}")
            st.write(f"**مستوى اللياقة:** {user[8]}")
            st.write(f"**الهدف:** {user[9]}")
    
    # تقدم التدريب
    st.subheader("📈 تقدم التدريب")
    history = get_workout_history(st.session_state['user_id'], days=30)
    if history:
        df = pd.DataFrame(history, columns=['id', 'user_id', 'exercise_id', 'plan_id', 'date', 'sets', 'reps', 'weight', 'duration', 'calories', 'notes', 'exercise_name'])
        df['date'] = pd.to_datetime(df['date'])
        daily_calories = df.groupby(df['date'].dt.date)['calories'].sum().reset_index()
        daily_calories.columns = ['date', 'calories']
        
        fig = px.line(daily_calories, x='date', y='calories', title='السعرات المحروقة يومياً')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("لا توجد تمارين مسجلة حتى الآن. ابدأ بتسجيل تمارينك!")
    
    # الوجبات السريعة
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏋️ تماريني", use_container_width=True):
            st.session_state['page'] = 'workouts'
            st.rerun()
    
    with col2:
        if st.button("🍽️ وجباتي", use_container_width=True):
            st.session_state['page'] = 'nutrition'
            st.rerun()

def workouts_page():
    st.title("🏋️ خطط التمارين")
    
    tab1, tab2, tab3 = st.tabs(["خططي", "تمارين جديدة", "سجل التمارين"])
    
    with tab1:
        plans = get_user_workout_plans(st.session_state['user_id'])
        if plans:
            for plan in plans:
                with st.expander(f"📋 {plan[2]} (تم إنشاؤها: {plan[3]})"):
                    exercises = get_plan_exercises(plan[0])
                    for ex in exercises:
                        st.write(f"• {ex[8]} - {ex[4]} مجموعات × {ex[5]} تكرارات")
                    
                    if st.button(f"تسجيل تدريب", key=f"log_{plan[0]}"):
                        st.session_state['selected_plan'] = plan[0]
                        st.session_state['page'] = 'log_workout'
                        st.rerun()
        else:
            st.info("لا توجد خطط تمارين. قم بإنشاء خطة جديدة!")
        
        if st.button("➕ خطة جديدة", use_container_width=True):
            st.session_state['page'] = 'create_plan'
            st.rerun()
    
    with tab2:
        st.subheader("البحث عن تمارين")
        search = st.text_input("ابحث عن تمرين...")
        
        if search:
            exercises = search_exercises(search)
        else:
            exercises = get_all_exercises()
        
        for ex in exercises[:10]:
            st.write(f"• **{ex[1]}** - {ex[2]} - {ex[3]}")
    
    with tab3:
        history = get_workout_history(st.session_state['user_id'])
        if history:
            for log in history[:20]:
                st.write(f"📅 {log[4]} - {log[11]} - {log[5]}×{log[6]} - {log[9]} سعرة")
        else:
            st.info("لا يوجد سجل تدريب")

def nutrition_page():
    st.title("🍽️ التغذية")
    
    tab1, tab2 = st.tabs(["وجباتي", "تتبع السعرات"])
    
    with tab1:
        meals = get_all_meals()
        if meals:
            for meal in meals:
                with st.expander(f"{meal[1]} - {meal[2]} ({meal[3]} سعرة)"):
                    st.write(f"**بروتين:** {meal[4]} جم")
                    st.write(f"**كربوهيدرات:** {meal[5]} جم")
                    st.write(f"**دهون:** {meal[6]} جم")
                    if meal[7]:
                        st.write(f"**وصفة:** {meal[7]}")
                    if st.button(f"تسجيل وجبة", key=f"meal_{meal[0]}"):
                        log_meal(st.session_state['user_id'], meal[0], 1, meal[3], "")
                        st.success("تم تسجيل الوجبة!")
        else:
            st.info("لا توجد وجبات مسجلة")
    
    with tab2:
        st.subheader("تتبع السعرات")
        daily_calories = get_nutrition_stats(st.session_state['user_id'])
        if daily_calories:
            fig = px.line(x=list(range(1, len(daily_calories)+1)), y=daily_calories, title='السعرات اليومية')
            st.plotly_chart(fig, use_container_width=True)

def create_plan_page():
    st.title("📝 إنشاء خطة تمارين جديدة")
    
    with st.form("create_plan_form"):
        plan_name = st.text_input("اسم الخطة")
        
        st.subheader("أضف تمارين")
        
        exercises = get_all_exercises()
        exercise_names = {f"{ex[1]} - {ex[3]}": ex[0] for ex in exercises}
        
        selected_exercises = st.multiselect("اختر التمارين", list(exercise_names.keys()))
        
        st.subheader("تفاصيل التمارين")
        exercise_details = []
        for ex_name in selected_exercises:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                sets = st.number_input(f"مجموعات ({ex_name})", min_value=1, max_value=10, value=3, key=f"sets_{ex_name}")
            with col2:
                reps = st.number_input(f"تكرارات ({ex_name})", min_value=1, max_value=50, value=10, key=f"reps_{ex_name}")
            with col3:
                weight = st.number_input(f"وزن ({ex_name})", min_value=0, max_value=200, value=0, key=f"weight_{ex_name}")
            with col4:
                rest = st.number_input(f"راحة ({ex_name})", min_value=10, max_value=300, value=60, key=f"rest_{ex_name}")
            
            exercise_details.append({
                'exercise_id': exercise_names[ex_name],
                'sets': sets,
                'reps': reps,
                'weight': weight,
                'rest_time': rest
            })
        
        submitted = st.form_submit_button("إنشاء الخطة")
        
        if submitted:
            if plan_name and exercise_details:
                plan_id = create_workout_plan(st.session_state['user_id'], plan_name, exercise_details)
                st.success(f"تم إنشاء الخطة بنجاح!")
                st.session_state['page'] = 'workouts'
                st.rerun()
            else:
                st.error("الرجاء إدخال اسم الخطة واختيار التمارين")

def log_workout_page():
    st.title("📝 تسجيل تمرين")
    
    if 'selected_plan' in st.session_state:
        plan_id = st.session_state['selected_plan']
        exercises = get_plan_exercises(plan_id)
        
        with st.form("log_workout_form"):
            st.write("سجل تفاصيل التمرين:")
            
            log_entries = []
            for ex in exercises:
                st.write(f"**{ex[8]}** - {ex[4]} مجموعات × {ex[5]} تكرارات")
                col1, col2, col3 = st.columns(3)
                with col1:
                    sets_done = st.number_input(f"مجموعات منفذة ({ex[8]})", min_value=0, max_value=ex[4]*2, value=ex[4], key=f"sets_done_{ex[0]}")
                with col2:
                    reps_done = st.number_input(f"تكرارات منفذة ({ex[8]})", min_value=0, max_value=ex[5]*2, value=ex[5], key=f"reps_done_{ex[0]}")
                with col3:
                    weight_used = st.number_input(f"وزن مستخدم ({ex[8]})", min_value=0, max_value=200, value=ex[6] or 0, key=f"weight_used_{ex[0]}")
                
                log_entries.append({
                    'exercise_id': ex[2],
                    'sets': sets_done,
                    'reps': reps_done,
                    'weight': weight_used
                })
            
            notes = st.text_area("ملاحظات")
            submitted = st.form_submit_button("حفظ التمرين")
            
            if submitted:
                for entry in log_entries:
                    if entry['sets'] > 0 and entry['reps'] > 0:
                        # حساب السعرات التقريبية
                        calories = entry['sets'] * entry['reps'] * 0.5  # تقريب بسيط
                        log_workout(
                            st.session_state['user_id'],
                            entry['exercise_id'],
                            plan_id,
                            entry['sets'],
                            entry['reps'],
                            entry['weight'],
                            30,  # مدة تقريبية
                            calories,
                            notes
                        )
                st.success("تم تسجيل التمرين بنجاح!")
                st.session_state['page'] = 'workouts'
                st.rerun()

def main():
    # تهيئة قاعدة البيانات
    init_db()
    
    # تهيئة جلسة المستخدم
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'show_signup' not in st.session_state:
        st.session_state['show_signup'] = False
    if 'page' not in st.session_state:
        st.session_state['page'] = 'dashboard'
    
    # قائمة جانبية
    with st.sidebar:
        if st.session_state['logged_in']:
            st.write(f"👋 مرحباً {st.session_state['username']}")
            if st.button("🏠 الرئيسية"):
                st.session_state['page'] = 'dashboard'
                st.rerun()
            if st.button("🏋️ تماريني"):
                st.session_state['page'] = 'workouts'
                st.rerun()
            if st.button("🍽️ تغذيتي"):
                st.session_state['page'] = 'nutrition'
                st.rerun()
            if st.button("🚪 تسجيل الخروج"):
                st.session_state['logged_in'] = False
                st.session_state['user_id'] = None
                st.session_state['username'] = None
                st.rerun()
    
    # الصفحات
    if not st.session_state['logged_in']:
        if st.session_state.get('show_signup', False):
            signup_page()
            if st.button("↩️ العودة لتسجيل الدخول"):
                st.session_state['show_signup'] = False
                st.rerun()
        else:
            login_page()
    else:
        if st.session_state['page'] == 'dashboard':
            dashboard_page()
        elif st.session_state['page'] == 'workouts':
            workouts_page()
        elif st.session_state['page'] == 'nutrition':
            nutrition_page()
        elif st.session_state['page'] == 'create_plan':
            create_plan_page()
        elif st.session_state['page'] == 'log_workout':
            log_workout_page()

if __name__ == "__main__":
    main()

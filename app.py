import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import hashlib
import json
import random

st.set_page_config(page_title="🏋️ Smart Fitness", page_icon="💪", layout="wide")

def init_db():
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        email TEXT,
        height REAL,
        weight REAL,
        age INTEGER,
        gender TEXT,
        fitness_level TEXT,
        goal TEXT,
        created_at TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        muscle_group TEXT,
        equipment TEXT,
        difficulty TEXT,
        description TEXT,
        gif_url TEXT,
        default_sets INTEGER,
        default_reps INTEGER,
        rest_time INTEGER
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS workout_plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        plan_name TEXT,
        created_at TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS plan_exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plan_id INTEGER,
        exercise_id INTEGER,
        day_of_week INTEGER,
        sets INTEGER,
        reps INTEGER,
        rest_time INTEGER,
        FOREIGN KEY (plan_id) REFERENCES workout_plans(id),
        FOREIGN KEY (exercise_id) REFERENCES exercises(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS workout_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        exercise_id INTEGER,
        plan_id INTEGER,
        date TIMESTAMP,
        sets_completed INTEGER,
        reps_completed INTEGER,
        calories_burned REAL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (exercise_id) REFERENCES exercises(id)
    )''')

    c.execute("SELECT COUNT(*) FROM exercises")
    if c.fetchone()[0] == 0:
        exercises = [
            ("جري سريع (Sprint)", "جري", "أرجل", "وزن جسم", "متقدم", "جري بأقصى سرعة لمسافة قصيرة لتطوير السرعة والقوة.", "https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif", 5, 4, 90),
            ("جري تحمل", "جري", "أرجل", "وزن جسم", "مبتدئ", "جري بسرعة ثابتة لمسافات طويلة (3-5 كم) لتحسين اللياقة القلبية.", "https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif", 1, 1, 60),
            ("جري فترات (Interval)", "جري", "أرجل", "وزن جسم", "متقدم", "تبديل بين الجري السريع والبطيء (1 دقيقة سريع + 2 دقيقة بطيء).", "https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif", 8, 1, 60),
            ("جري مرتفعات", "جري", "أرجل", "وزن جسم", "متقدم", "جري على منحدرات أو تلال لتقوية الأرجل وزيادة التحمل.", "https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif", 6, 1, 90),
            ("ضغط الصدر بالبار", "حديد", "صدر", "بار", "مبتدئ", "استلقِ على مقعد وادفع البار لأعلى لتقوية الصدر والكتفين.", "https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif", 4, 10, 90),
            ("سحب أمامي (Lat Pulldown)", "حديد", "ظهر", "جهاز", "مبتدئ", "اسحب البار للأسفل حتى يلامس صدرك لتقوية الظهر.", "https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif", 4, 12, 90),
            ("قرفصاء بالبار", "حديد", "أرجل", "بار", "متوسط", "ضع البار على كتفيك وانزل للأسفل للحصول على تمرين شامل للأرجل.", "https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif", 4, 10, 120),
            ("تجديل البايسبس", "حديد", "ذراع", "بار", "مبتدئ", "امسك البار واثنِ ذراعيك لأعلى لتقوية العضلة الأمامية للذراع.", "https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif", 4, 12, 60),
            ("ضغط (Push-up)", "وزن جسم", "صدر", "وزن جسم", "مبتدئ", "استلقِ على بطنك وادفع جسمك لأعلى باستخدام ذراعيك.", "https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif", 3, 15, 60),
            ("سحب (Pull-up)", "وزن جسم", "ظهر", "وزن جسم", "متوسط", "علق على البار واسحب جسمك للأعلى حتى يلامس الذقن البار.", "https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif", 3, 8, 90),
            ("قرفصاء (Squat)", "وزن جسم", "أرجل", "وزن جسم", "مبتدئ", "انزل للأسفل كأنك تجلس على كرسي ثم ارفع لتقوية الأرجل والأرداف.", "https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif", 3, 20, 60),
            ("تمرين البطن (Crunch)", "وزن جسم", "بطن", "وزن جسم", "مبتدئ", "استلقِ على ظهرك وارفع كتفيك عن الأرض لتقوية عضلات البطن.", "https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif", 3, 20, 30),
            ("البلانك (Plank)", "وزن جسم", "بطن", "وزن جسم", "مبتدئ", "اثبت في وضعية الضغط مع تثبيت الجسم مستقيمًا لتقوية الجذع.", "https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif", 3, 30, 45),
            ("بيربي (Burpee)", "فتنس", "كامل الجسم", "وزن جسم", "متوسط", "اجلس ثم اقفز للخلف لوضعية الضغط، ثم اقفز للأمام وقفز لأعلى.", "https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif", 3, 10, 90),
            ("متسلق الجبال", "فتنس", "كامل الجسم", "وزن جسم", "متوسط", "في وضعية الضغط، اسحب ركبتيك تجاه صدرك بالتناوب بسرعة.", "https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif", 3, 20, 30),
            ("قفزة القرفصاء", "فتنس", "أرجل", "وزن جسم", "متوسط", "قرفصاء ثم قفز لأعلى بأقصى قوة لتمرين انفجاري للأرجل.", "https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif", 3, 15, 60),
            ("نط الحبل", "فتنس", "كامل الجسم", "حبل", "مبتدئ", "اقفز فوق الحبل مع دورانه لحرق السعرات وتحسين التنسيق.", "https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif", 3, 60, 30),
        ]

        c.executemany('''INSERT INTO exercises 
                         (name, category, muscle_group, equipment, difficulty, 
                          description, gif_url, default_sets, default_reps, rest_time) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', exercises)
        conn.commit()

    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password, email, height, weight, age, gender, fitness_level, goal):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    try:
        c.execute('''INSERT INTO users 
                     (username, password, email, height, weight, age, gender, fitness_level, goal, created_at) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (username, hash_password(password), email, height, weight, age, gender, fitness_level, goal, datetime.now()))
        conn.commit()
        return True
    except:
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

def get_user(user_id):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def get_all_exercises():
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT * FROM exercises")
    ex = c.fetchall()
    conn.close()
    return ex

def get_exercises_by_category(category):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    if category == "الكل":
        c.execute("SELECT * FROM exercises")
    else:
        c.execute("SELECT * FROM exercises WHERE category = ?", (category,))
    ex = c.fetchall()
    conn.close()
    return ex

def get_workout_stats(user_id):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM workout_logs WHERE user_id = ?", (user_id,))
    total = c.fetchone()[0]
    c.execute("SELECT SUM(calories_burned) FROM workout_logs WHERE user_id = ?", (user_id,))
    calories = c.fetchone()[0] or 0
    conn.close()
    return total, calories

def log_workout(user_id, exercise_id, sets, reps, calories):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute('''INSERT INTO workout_logs 
                 (user_id, exercise_id, date, sets_completed, reps_completed, calories_burned) 
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (user_id, exercise_id, datetime.now(), sets, reps, calories))
    conn.commit()
    conn.close()

def create_plan(user_id, plan_name, selected_exercises):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("INSERT INTO workout_plans (user_id, plan_name, created_at) VALUES (?, ?, ?)",
              (user_id, plan_name, datetime.now()))
    plan_id = c.lastrowid
    for i, ex_id in enumerate(selected_exercises):
        ex = get_exercise_by_id(ex_id)
        day = (i % 3) + 1
        c.execute('''INSERT INTO plan_exercises 
                     (plan_id, exercise_id, day_of_week, sets, reps, rest_time) 
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (plan_id, ex_id, day, ex[7] or 3, ex[8] or 10, ex[9] or 60))
    conn.commit()
    conn.close()
    return plan_id

def get_exercise_by_id(ex_id):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT * FROM exercises WHERE id = ?", (ex_id,))
    ex = c.fetchone()
    conn.close()
    return ex

def get_user_plans(user_id):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT * FROM workout_plans WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    plans = c.fetchall()
    conn.close()
    return plans

def get_plan_exercises(plan_id):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute('''SELECT pe.*, e.name, e.gif_url, e.description 
                 FROM plan_exercises pe 
                 JOIN exercises e ON pe.exercise_id = e.id 
                 WHERE pe.plan_id = ?''', (plan_id,))
    ex = c.fetchall()
    conn.close()
    return ex

def get_workout_history(user_id):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute('''SELECT wl.*, e.name 
                 FROM workout_logs wl 
                 JOIN exercises e ON wl.exercise_id = e.id 
                 WHERE wl.user_id = ? 
                 ORDER BY wl.date DESC''', (user_id,))
    logs = c.fetchall()
    conn.close()
    return logs

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
                st.error("بيانات غير صحيحة")
    with col2:
        st.write("---")
        if st.button("إنشاء حساب جديد", use_container_width=True):
            st.session_state['show_signup'] = True
            st.rerun()

def signup_page():
    st.title("🏋️ Smart Fitness Planner")
    st.subheader("إنشاء حساب جديد")
    with st.form("signup"):
        username = st.text_input("اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")
        confirm = st.text_input("تأكيد كلمة المرور", type="password")
        email = st.text_input("البريد الإلكتروني")
        height = st.number_input("الطول (سم)", 100, 250, 170)
        weight = st.number_input("الوزن (كجم)", 30, 200, 70)
        age = st.number_input("العمر", 10, 100, 25)
        gender = st.selectbox("الجنس", ["ذكر", "أنثى"])
        level = st.selectbox("مستوى اللياقة", ["مبتدئ", "متوسط", "متقدم"])
        goal = st.selectbox("الهدف", ["فقدان الوزن", "بناء عضلات", "تحسين اللياقة", "الحفاظ على الوزن"])
        if st.form_submit_button("إنشاء حساب"):
            if password != confirm:
                st.error("كلمة المرور غير متطابقة")
            elif len(password) < 6:
                st.error("كلمة المرور يجب أن تكون 6 أحرف على الأقل")
            else:
                if create_user(username, password, email, height, weight, age, gender, level, goal):
                    st.success("تم إنشاء الحساب بنجاح!")
                    st.session_state['show_signup'] = False
                    st.rerun()
                else:
                    st.error("اسم المستخدم موجود بالفعل")

def dashboard_page():
    user = get_user(st.session_state['user_id'])
    total_workouts, total_calories = get_workout_stats(st.session_state['user_id'])
    st.title(f"👋 مرحباً {st.session_state['username']}")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🏋️ إجمالي التمارين", total_workouts)
    with col2:
        st.metric("🔥 السعرات المحروقة", f"{total_calories:.0f}")
    with col3:
        history = get_workout_history(st.session_state['user_id'])
        days = len(set([log[4].split()[0] for log in history])) if history else 0
        st.metric("📅 أيام التدريب", days)
    st.divider()
    st.subheader("📚 مكتبة التمارين")
    categories = ["الكل", "جري", "حديد", "وزن جسم", "فتنس"]
    selected_cat = st.selectbox("اختر التصنيف", categories)
    exercises = get_exercises_by_category(selected_cat)
    for ex in exercises[:6]:
        with st.container():
            c1, c2 = st.columns([1, 3])
            with c1:
                st.image(ex[6], width=120)
            with c2:
                st.subheader(ex[1])
                st.write(f"**التصنيف:** {ex[2]} | **المجموعة:** {ex[3]} | **المستوى:** {ex[5]}")
                st.write(f"**الجولات:** {ex[7]} | **التكرارات:** {ex[8]} | **الراحة:** {ex[9]} ثانية")
                st.write(f"**الشرح:** {ex[6]}")
            st.divider()

def exercises_page():
    st.title("📚 مكتبة التمارين")
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("التصنيف", ["الكل", "جري", "حديد", "وزن جسم", "فتنس"])
    with col2:
        level = st.selectbox("المستوى", ["الكل", "مبتدئ", "متوسط", "متقدم"])
    exercises = get_all_exercises()
    filtered = []
    for ex in exercises:
        if (category == "الكل" or ex[2] == category) and (level == "الكل" or ex[5] == level):
            filtered.append(ex)
    for ex in filtered:
        with st.container():
            c1, c2 = st.columns([1, 3])
            with c1:
                st.image(ex[6], width=150)
            with c2:
                st.subheader(ex[1])
                st.write(f"**التصنيف:** {ex[2]} | **المجموعة العضلية:** {ex[3]} | **المستوى:** {ex[5]}")
                st.write(f"**الجولات:** {ex[7]} | **التكرارات:** {ex[8]} | **الراحة:** {ex[9]} ثانية")
                st.write(f"**الشرح:** {ex[6]}")
            st.divider()

def plans_page():
    st.title("📋 خطط التمارين")
    user_plans = get_user_plans(st.session_state['user_id'])
    if not user_plans:
        st.info("ليس لديك خطط تمارين حالياً")
    else:
        for plan in user_plans:
            with st.expander(f"📌 {plan[2]} - {plan[3]}"):
                exercises = get_plan_exercises(plan[0])
                for ex in exercises:
                    st.write(f"• {ex[8]} - {ex[4]} مجموعات × {ex[5]} تكرارات")
                    if ex[9]:
                        st.image(ex[9], width=100)
    if st.button("➕ إنشاء خطة جديدة", use_container_width=True):
        st.session_state['page'] = 'create_plan'
        st.rerun()

def create_plan_page():
    st.title("📝 إنشاء خطة جديدة")
    with st.form("new_plan"):
        plan_name = st.text_input("اسم الخطة")
        exercises = get_all_exercises()
        exercise_dict = {f"{ex[1]} - {ex[2]}": ex[0] for ex in exercises}
        selected = st.multiselect("اختر التمارين", list(exercise_dict.keys()))
        if st.form_submit_button("إنشاء الخطة"):
            if plan_name and selected:
                selected_ids = [exercise_dict[name] for name in selected]
                create_plan(st.session_state['user_id'], plan_name, selected_ids)
                st.success("تم إنشاء الخطة بنجاح!")
                st.session_state['page'] = 'plans'
                st.rerun()
            else:
                st.error("الرجاء إدخال اسم الخطة واختيار التمارين")

def log_page():
    st.title("📝 تسجيل تمرين")
    exercises = get_all_exercises()
    ex_names = {f"{ex[1]} - {ex[2]}": ex for ex in exercises}
    selected = st.selectbox("اختر التمرين", list(ex_names.keys()))
    if selected:
        ex = ex_names[selected]
        col1, col2 = st.columns(2)
        with col1:
            sets = st.number_input("عدد الجولات", 1, 10, ex[7] or 3)
            reps = st.number_input("عدد التكرارات", 1, 50, ex[8] or 10)
        with col2:
            calories = st.number_input("السعرات المحروقة (تقديري)", 10, 1000, 100)
        if st.button("حفظ التمرين"):
            log_workout(st.session_state['user_id'], ex[0], sets, reps, calories)
            st.success("تم حفظ التمرين بنجاح!")

def history_page():
    st.title("📊 سجل التمارين")
    logs = get_workout_history(st.session_state['user_id'])
    if logs:
        df = pd.DataFrame(logs, columns=['id', 'user_id', 'exercise_id', 'date', 'sets', 'reps', 'calories', 'name'])
        st.dataframe(df[['date', 'name', 'sets', 'reps', 'calories']])
    else:
        st.info("لا يوجد سجل تمارين حتى الآن")

def main():
    init_db()
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'show_signup' not in st.session_state:
        st.session_state['show_signup'] = False
    if 'page' not in st.session_state:
        st.session_state['page'] = 'dashboard'

    if not st.session_state['logged_in']:
        if st.session_state.get('show_signup', False):
            signup_page()
            if st.button("↩️ العودة لتسجيل الدخول"):
                st.session_state['show_signup'] = False
                st.rerun()
        else:
            login_page()
        return

    with st.sidebar:
        st.write(f"👋 {st.session_state['username']}")
        if st.button("🏠 الرئيسية"):
            st.session_state['page'] = 'dashboard'
            st.rerun()
        if st.button("📚 مكتبة التمارين"):
            st.session_state['page'] = 'exercises'
            st.rerun()
        if st.button("📋 خططي"):
            st.session_state['page'] = 'plans'
            st.rerun()
        if st.button("📝 تسجيل تمرين"):
            st.session_state['page'] = 'log'
            st.rerun()
        if st.button("📊 سجلي"):
            st.session_state['page'] = 'history'
            st.rerun()
        if st.button("🚪 تسجيل الخروج"):
            st.session_state['logged_in'] = False
            st.rerun()

    if st.session_state['page'] == 'dashboard':
        dashboard_page()
    elif st.session_state['page'] == 'exercises':
        exercises_page()
    elif st.session_state['page'] == 'plans':
        plans_page()
    elif st.session_state['page'] == 'create_plan':
        create_plan_page()
    elif st.session_state['page'] == 'log':
        log_page()
    elif st.session_state['page'] == 'history':
        history_page()

if __name__ == "__main__":
    main()
```

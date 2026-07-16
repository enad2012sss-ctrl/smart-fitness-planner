import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime
import hashlib

st.set_page_config(page_title="🏋️ Fitness Planner", page_icon="💪", layout="wide")

def init_db():
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        height REAL,
        weight REAL,
        age INTEGER,
        goal TEXT,
        created_at TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        description TEXT,
        gif_url TEXT,
        sets_default INTEGER,
        reps_default INTEGER
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        exercise_id INTEGER,
        date TIMESTAMP,
        sets INTEGER,
        reps INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (exercise_id) REFERENCES exercises(id)
    )''')
    
    c.execute("SELECT COUNT(*) FROM exercises")
    if c.fetchone()[0] == 0:
        exercises = [
            ("جري سريع", "جري", "جري بأقصى سرعة", "https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif", 5, 4),
            ("جري تحمل", "جري", "جري لمسافات طويلة", "https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif", 1, 1),
            ("ضغط صدر", "حديد", "تمرين الصدر بالبار", "https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif", 4, 10),
            ("سحب أمامي", "حديد", "تمرين الظهر", "https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif", 4, 12),
            ("قرفصاء", "وزن جسم", "تمرين الأرجل", "https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif", 3, 20),
            ("ضغط", "وزن جسم", "تمرين الصدر", "https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif", 3, 15),
            ("بيربي", "فتنس", "تمرين شامل", "https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif", 3, 10),
            ("نط حبل", "فتنس", "تمرين كارديو", "https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif", 3, 60),
        ]
        c.executemany("INSERT INTO exercises (name, category, description, gif_url, sets_default, reps_default) VALUES (?, ?, ?, ?, ?, ?)", exercises)
        conn.commit()
    conn.close()

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def create_user(username, password, height, weight, age, goal):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, height, weight, age, goal, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (username, hash_password(password), height, weight, age, goal, datetime.now()))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def authenticate(username, password):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user

def get_exercises():
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT * FROM exercises")
    ex = c.fetchall()
    conn.close()
    return ex

def log_workout(user_id, exercise_id, sets, reps):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("INSERT INTO logs (user_id, exercise_id, date, sets, reps) VALUES (?, ?, ?, ?, ?)",
              (user_id, exercise_id, datetime.now(), sets, reps))
    conn.commit()
    conn.close()

def get_logs(user_id):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT l.*, e.name FROM logs l JOIN exercises e ON l.exercise_id = e.id WHERE l.user_id = ? ORDER BY l.date DESC", (user_id,))
    logs = c.fetchall()
    conn.close()
    return logs

def login_page():
    st.title("🏋️ Fitness Planner")
    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")
        if st.button("دخول"):
            user = authenticate(username, password)
            if user:
                st.session_state['user_id'] = user[0]
                st.session_state['username'] = user[1]
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("بيانات غير صحيحة")
    with col2:
        if st.button("حساب جديد"):
            st.session_state['show_signup'] = True
            st.rerun()

def signup_page():
    st.title("إنشاء حساب")
    with st.form("signup"):
        username = st.text_input("اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")
        confirm = st.text_input("تأكيد", type="password")
        height = st.number_input("الطول (سم)", 100, 250, 170)
        weight = st.number_input("الوزن (كجم)", 30, 200, 70)
        age = st.number_input("العمر", 10, 100, 25)
        goal = st.selectbox("الهدف", ["فقدان وزن", "بناء عضلات", "لياقة", "صحة"])
        if st.form_submit_button("إنشاء"):
            if password != confirm:
                st.error("كلمة المرور غير متطابقة")
            elif len(password) < 6:
                st.error("كلمة المرور قصيرة")
            elif create_user(username, password, height, weight, age, goal):
                st.success("تم إنشاء الحساب")
                st.session_state['show_signup'] = False
                st.rerun()
            else:
                st.error("اسم المستخدم موجود")

def main():
    init_db()
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'show_signup' not in st.session_state:
        st.session_state['show_signup'] = False

    if not st.session_state['logged_in']:
        if st.session_state.get('show_signup'):
            signup_page()
            if st.button("رجوع"):
                st.session_state['show_signup'] = False
                st.rerun()
        else:
            login_page()
        return

    st.sidebar.write(f"👋 {st.session_state['username']}")
    page = st.sidebar.radio("القائمة", ["الرئيسية", "تمارين", "تسجيل", "سجل"])

    if page == "الرئيسية":
        st.title("الرئيسية")
        logs = get_logs(st.session_state['user_id'])
        st.metric("عدد التمارين", len(logs))
        if logs:
            df = pd.DataFrame(logs, columns=['id', 'user_id', 'exercise_id', 'date', 'sets', 'reps', 'name'])
            st.dataframe(df[['date', 'name', 'sets', 'reps']])

    elif page == "تمارين":
        st.title("مكتبة التمارين")
        exercises = get_exercises()
        for ex in exercises:
            with st.container():
                c1, c2 = st.columns([1, 3])
                with c1:
                    st.image(ex[3], width=100)
                with c2:
                    st.subheader(ex[1])
                    st.write(f"**التصنيف:** {ex[2]}")
                    st.write(f"**الشرح:** {ex[3]}")
                    st.write(f"**الجولات:** {ex[4]} | **التكرارات:** {ex[5]}")
                st.divider()

    elif page == "تسجيل":
        st.title("تسجيل تمرين")
        exercises = get_exercises()
        ex_dict = {f"{ex[1]} - {ex[2]}": ex[0] for ex in exercises}
        selected = st.selectbox("اختر التمرين", list(ex_dict.keys()))
        if selected:
            ex_id = ex_dict[selected]
            col1, col2 = st.columns(2)
            with col1:
                sets = st.number_input("الجولات", 1, 10, 3)
            with col2:
                reps = st.number_input("التكرارات", 1, 50, 10)
            if st.button("حفظ"):
                log_workout(st.session_state['user_id'], ex_id, sets, reps)
                st.success("تم الحفظ")

    elif page == "سجل":
        st.title("سجل التمارين")
        logs = get_logs(st.session_state['user_id'])
        if logs:
            df = pd.DataFrame(logs, columns=['id', 'user_id', 'exercise_id', 'date', 'sets', 'reps', 'name'])
            st.dataframe(df[['date', 'name', 'sets', 'reps']])
        else:
            st.info("لا يوجد سجل")

if __name__ == "__main__":
    main()
```

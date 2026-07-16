import streamlit as st
import sqlite3
import pandas as pd
import hashlib
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="Fitness Planner", layout="wide")

# 1. إدارة قاعدة البيانات
def init_db():
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        created_at TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
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
    
    # إدخال تمارين افتراضية إذا كانت الجداول فارغة
    c.execute("SELECT COUNT(*) FROM exercises")
    if c.fetchone()[0] == 0:
        ex = [
            ("جري سريع", "جري", 5, 4),
            ("جري تحمل", "جري", 1, 1),
            ("ضغط صدر", "حديد", 4, 10),
            ("سحب أمامي", "حديد", 4, 12),
            ("قرفصاء", "وزن جسم", 3, 20),
            ("ضغط", "وزن جسم", 3, 15),
            ("بيربي", "فتنس", 3, 10),
            ("نط حبل", "فتنس", 3, 60),
        ]
        c.executemany("INSERT INTO exercises (name, category, sets_default, reps_default) VALUES (?, ?, ?, ?)", ex)
        conn.commit()
    conn.close()

# تشغيل قاعدة البيانات تلقائياً
init_db()

# 2. دوال التشفير والمصادقة
def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def create_user(username, password):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, created_at) VALUES (?, ?, ?)", 
                  (username, hash_password(password), datetime.now()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT id, username FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user

# 3. دوال التمارين والربط
def get_exercises():
    conn = sqlite3.connect('fitness.db')
    df = pd.read_sql_query("SELECT * FROM exercises", conn)
    conn.close()
    return df

def log_exercise(user_id, exercise_id, sets, reps):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("INSERT INTO logs (user_id, exercise_id, date, sets, reps) VALUES (?, ?, ?, ?, ?)",
              (user_id, exercise_id, datetime.now(), sets, reps))
    conn.commit()
    conn.close()

def get_user_logs(user_id):
    conn = sqlite3.connect('fitness.db')
    query = '''
        SELECT logs.date as 'التاريخ', exercises.name as 'التمرين', exercises.category as 'الفئة', logs.sets as 'الجولات', logs.reps as 'التكرارات'
        FROM logs 
        JOIN exercises ON logs.exercise_id = exercises.id 
        WHERE logs.user_id = ?
        ORDER BY logs.date DESC
    '''
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    return df

# 4. واجهة المستخدم (Streamlit UI)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.title("🏋️‍♂️ تطبيق Fitness Planner")
    tab1, tab2 = st.tabs(["تسجيل الدخول", "إنشاء حساب جديد"])
    
    with tab1:
        user_input = st.text_input("اسم المستخدم", key="login_user")
        pass_input = st.text_input("كلمة المرور", type="password", key="login_pass")
        if st.button("دخول"):
            user = login_user(user_input, pass_input)
            if user:
                st.session_state.logged_in = True
                st.session_state.user_id = user[0]
                st.session_state.username = user[1]
                st.success(f"مرحباً بك مجدداً {user[1]}!")
                st.rerun()
            else:
                st.error("اسم المستخدم أو كلمة المرور غير صحيحة.")
                
    with tab2:
        new_user = st.text_input("اختر اسم مستخدم", key="reg_user")
        new_pass = st.text_input("اختر كلمة مرور", type="password", key="reg_pass")
        if st.button("تسجيل"):
            if new_user and new_pass:
                if create_user(new_user, new_pass):
                    st.success("تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول.")
                else:
                    st.error("اسم المستخدم مسجل مسبقاً، اختر اسماً آخر.")
            else:
                st.warning("الرجاء ملء جميع الحقول.")

else:
    # واجهة المستخدم بعد تسجيل الدخول بنجاح
    st.sidebar.title(f"👋 مرحباً، {st.session_state.username}")
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = ""
        st.rerun()
        
    st.title("💪 لوحة التحكم الرياضية")
    
    # جلب التمارين المتاحة للربط
    exercises_df = get_exercises()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📝 تسجيل تمرين جديد")
        
        # قائمة منسدلة لاختيار التمرين من قاعدة البيانات
        exercise_options = {row['name']: row['id'] for _, row in exercises_df.iterrows()}
        selected_exercise_name = st.selectbox("اختر التمرين:", list(exercise_options.keys()))
        selected_exercise_id = exercise_options[selected_exercise_name]
        
        # جلب القيم الافتراضية للتمرين المحدد
        default_data = exercises_df[exercises_df['id'] == selected_exercise_id].iloc[0]
        
        sets = st.number_input("عدد الجولات", min_value=1, value=int(default_data['sets_default']))
        reps = st.number_input("عدد التكرارات", min_value=1, value=int(default_data['reps_default']))
        
        if st.button("حفظ التمرين في السجل"):
            log_exercise(st.session_state.user_id, selected_exercise_id, sets, reps)
            st.success("تم تسجيل التمرين بنجاح!")
            st.rerun()
            
    with col2:
        st.subheader("📊 سجل تمارينك السابقة")
        logs_df = get_user_logs(st.session_state.user_id)
        
        if not logs_df.empty:
            st.dataframe(logs_df, use_container_width=True)
        else:
            st.info("لا توجد تمارين مسجلة بعد. ابدأ بإضافة تمرينك الأول!")

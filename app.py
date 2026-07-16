import streamlit as st
import sqlite3
import pandas as pd
import hashlib
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Fitness Planner Pro", layout="wide", page_icon="💪")

# ==================== دالة الاتصال بقاعدة البيانات ====================
def get_connection():
    return sqlite3.connect('fitness.db', check_same_thread=False)

# ==================== إعداد قاعدة البيانات ====================
def init_db():
    conn = get_connection()
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
        weight REAL DEFAULT 0,
        notes TEXT DEFAULT '',
        duration INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (exercise_id) REFERENCES exercises(id)
    )''')
    
    c.execute("SELECT COUNT(*) FROM exercises")
    if c.fetchone()[0] == 0:
        ex = [
            ("جري سريع", "كارديو", 5, 4),
            ("جري تحمل", "كارديو", 1, 1),
            ("ضغط صدر", "حديد", 4, 10),
            ("سحب أمامي", "حديد", 4, 12),
            ("قرفصاء", "وزن جسم", 3, 20),
            ("ضغط", "وزن جسم", 3, 15),
            ("بيربي", "فتنس", 3, 10),
            ("نط حبل", "فتنس", 3, 60),
            ("رفعة مميتة", "حديد", 3, 8),
            ("بلانك", "وزن جسم", 3, 45),
            ("طعنات", "وزن جسم", 3, 12),
            ("سباحة", "كارديو", 1, 30)
        ]
        c.executemany("INSERT INTO exercises (name, category, sets_default, reps_default) VALUES (?, ?, ?, ?)", ex)
        conn.commit()
    conn.close()

# ==================== دوال المستخدمين ====================
def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def create_user(username, password):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, created_at) VALUES (?, ?, ?)", 
                 (username, hash_password(password), datetime.now()))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
             (username, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user

# ==================== دوال التمارين ====================
def get_exercises(category=None):
    conn = get_connection()
    c = conn.cursor()
    if category and category != "الكل":
        c.execute("SELECT * FROM exercises WHERE category = ?", (category,))
    else:
        c.execute("SELECT * FROM exercises")
    ex = c.fetchall()
    conn.close()
    return ex

def get_categories():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT DISTINCT category FROM exercises")
    cats = [row[0] for row in c.fetchall()]
    conn.close()
    return cats

def add_exercise(name, category, sets_default, reps_default):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO exercises (name, category, sets_default, reps_default) VALUES (?, ?, ?, ?)",
                 (name, category, sets_default, reps_default))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def delete_exercise(exercise_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM logs WHERE exercise_id = ?", (exercise_id,))
    c.execute("DELETE FROM exercises WHERE id = ?", (exercise_id,))
    conn.commit()
    conn.close()

def update_exercise(exercise_id, name, category, sets_default, reps_default):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE exercises SET name=?, category=?, sets_default=?, reps_default=? WHERE id=?",
             (name, category, sets_default, reps_default, exercise_id))
    conn.commit()
    conn.close()

# ==================== دوال السجلات ====================
def log_workout(user_id, exercise_id, sets, reps, weight=0, notes="", duration=0):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO logs (user_id, exercise_id, date, sets, reps, weight, notes, duration) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
             (user_id, exercise_id, datetime.now(), sets, reps, weight, notes, duration))
    conn.commit()
    conn.close()

def get_logs(user_id, days=30):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT l.id, l.date, e.name, e.category, l.sets, l.reps, l.weight, l.notes, l.duration
        FROM logs l 
        JOIN exercises e ON l.exercise_id = e.id 
        WHERE l.user_id = ? AND l.date >= date('now', ?)
        ORDER BY l.date DESC
    """, (user_id, f'-{days} days'))
    logs = c.fetchall()
    conn.close()
    return logs

def get_stats(user_id, days=30):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT e.category, COUNT(*), SUM(l.sets), SUM(l.reps)
        FROM logs l 
        JOIN exercises e ON l.exercise_id = e.id 
        WHERE l.user_id = ? AND l.date >= date('now', ?)
        GROUP BY e.category
    """, (user_id, f'-{days} days'))
    stats = c.fetchall()
    conn.close()
    return stats

def delete_log(log_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM logs WHERE id = ?", (log_id,))
    conn.commit()
    conn.close()

# ==================== واجهة تسجيل الدخول ====================
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🏋️ Fitness Planner Pro")
        st.markdown("---")
        
        tab1, tab2 = st.tabs(["تسجيل الدخول", "إنشاء حساب"])
        
        with tab1:
            username = st.text_input("اسم المستخدم", key="login_user")
            password = st.text_input("كلمة المرور", type="password", key="login_pass")
            if st.button("دخول", use_container_width=True):
                user = authenticate_user(username, password)
                if user:
                    st.session_state['user_id'] = user[0]
                    st.session_state['username'] = user[1]
                    st.session_state['logged_in'] = True
                    st.rerun()
                else:
                    st.error("❌ بيانات غير صحيحة")
        
        with tab2:
            new_user = st.text_input("اسم المستخدم الجديد", key="reg_user")
            new_pass = st.text_input("كلمة المرور", type="password", key="reg_pass")
            if st.button("إنشاء حساب", use_container_width=True):
                if len(new_user) < 3:
                    st.error("اسم المستخدم يجب أن يكون 3 أحرف على الأقل")
                elif len(new_pass) < 4:
                    st.error("كلمة المرور يجب أن تكون 4 أحرف على الأقل")
                elif create_user(new_user, new_pass):
                    st.success("✅ تم إنشاء الحساب! يمكنك تسجيل الدخول الآن")
                else:
                    st.error("❌ اسم المستخدم موجود مسبقاً")

# ==================== الصفحة الرئيسية ====================
def dashboard():
    st.title("📊 لوحة التحكم")
    
    days = st.selectbox("الفترة", [7, 14, 30, 90], index=2, key="dash_days")
    logs = get_logs(st.session_state['user_id'], days)
    
    col1, col2, col3, col4 = st.columns(4)
    if logs:
        df = pd.DataFrame(logs, columns=['id', 'date', 'name', 'category', 'sets', 'reps', 'weight', 'notes', 'duration'])
        today = datetime.now().strftime('%Y-%m-%d')
        today_logs = df[df['date'].str.startswith(today)] if not df.empty else pd.DataFrame()
        
        with col1:
            st.metric("📝 إجمالي التمارين", len(df))
        with col2:
            st.metric("🏃 تمارين اليوم", len(today_logs))
        with col3:
            st.metric("💪 إجمالي الجولات", df['sets'].sum() if not df.empty else 0)
        with col4:
            st.metric("🔄 إجمالي التكرارات", df['reps'].sum() if not df.empty else 0)
        
        st.markdown("---")
        
        # رسوم بيانية
        col1, col2 = st.columns(2)
        with col1:
            if not df.empty:
                category_counts = df['category'].value_counts().reset_index()
                category_counts.columns = ['الفئة', 'العدد']
                fig = px.pie(category_counts, values='العدد', names='الفئة', title="توزيع التمارين حسب الفئة")
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if not df.empty:
                df['date_only'] = df['date'].str[:10]
                daily = df.groupby('date_only').size().reset_index(name='العدد')
                fig = px.line(daily, x='date_only', y='العدد', title="نشاط التمارين اليومي", markers=True)
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("لا يوجد سجل تمارين في هذه الفترة")

# ==================== صفحة التمارين ====================
def exercises_page():
    st.title("📚 مكتبة التمارين")
    
    tab1, tab2 = st.tabs(["عرض التمارين", "إضافة تمرين"])
    
    with tab1:
        cats = ["الكل"] + get_categories()
        selected_cat = st.selectbox("تصفية حسب الفئة", cats)
        
        exercises = get_exercises(None if selected_cat == "الكل" else selected_cat)
        
        for ex in exercises:
            with st.expander(f"🏋️ {ex[1]} - {ex[2]}"):
                col1, col2 = st.columns(2)
                with col1:
                    new_name = st.text_input("الاسم", ex[1], key=f"name_{ex[0]}")
                    new_cat = st.selectbox("الفئة", get_categories(), 
                                          index=get_categories().index(ex[2]) if ex[2] in get_categories() else 0,
                                          key=f"cat_{ex[0]}")
                with col2:
                    new_sets = st.number_input("الجولات الافتراضية", 1, 20, ex[3], key=f"sets_{ex[0]}")
                    new_reps = st.number_input("التكرارات الافتراضية", 1, 100, ex[4], key=f"reps_{ex[0]}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💾 حفظ التعديلات", key=f"save_{ex[0]}"):
                        update_exercise(ex[0], new_name, new_cat, new_sets, new_reps)
                        st.success("تم التحديث!")
                        st.rerun()
                with col2:
                    if st.button("🗑️ حذف", key=f"del_{ex[0]}"):
                        delete_exercise(ex[0])
                        st.success("تم الحذف!")
                        st.rerun()
    
    with tab2:
        st.subheader("إضافة تمرين جديد")
        with st.form("add_exercise"):
            name = st.text_input("اسم التمرين")
            category = st.text_input("الفئة (مثال: كارديو، حديد، وزن جسم)")
            col1, col2 = st.columns(2)
            with col1:
                sets = st.number_input("الجولات الافتراضية", 1, 20, 3)
            with col2:
                reps = st.number_input("التكرارات الافتراضية", 1, 100, 10)
            
            if st.form_submit_button("إضافة", use_container_width=True):
                if name and category:
                    if add_exercise(name, category, sets, reps):
                        st.success(f"✅ تم إضافة {name}")
                        st.rerun()
                    else:
                        st.error("حدث خطأ")
                else:
                    st.warning("الرجاء ملء جميع الحقول")

# ==================== صفحة تسجيل التمارين ====================
def log_page():
    st.title("📝 تسجيل تمرين جديد")
    
    exercises = get_exercises()
    if not exercises:
        st.warning("لا توجد تمارين! أضف تمارين أولاً من صفحة التمارين")
        return
    
    ex_dict = {f"{ex[1]} ({ex[2]})": ex for ex in exercises}
    selected_name = st.selectbox("اختر التمرين", list(ex_dict.keys()))
    selected_ex = ex_dict[selected_name]
    
    with st.form("log_workout"):
        col1, col2, col3 = st.columns(3)
        with col1:
            sets = st.number_input("الجولات", 1, 20, selected_ex[3])
        with col2:
            reps = st.number_input("التكرارات", 1, 100, selected_ex[4])
        with col3:
            weight = st.number_input("الوزن (كجم)", 0.0, 500.0, 0.0, step=2.5)
        
        col1, col2 = st.columns(2)
        with col1:
            duration = st.number_input("المدة (دقائق)", 0, 300, 0)
        with col2:
            notes = st.text_area("ملاحظات", placeholder="مثال: شعرت بالتعب، زدت الوزن...", height=100)
        
        if st.form_submit_button("💾 حفظ التمرين", use_container_width=True):
            log_workout(st.session_state['user_id'], selected_ex[0], sets, reps, weight, notes, duration)
            st.success("✅ تم حفظ التمرين بنجاح!")
            st.rerun()

# ==================== صفحة السجل ====================
def history_page():
    st.title("📋 سجل التمارين")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        days = st.selectbox("عرض آخر", [7, 14, 30, 90, 365], index=2, key="hist_days")
    with col2:
        export_format = st.selectbox("تصدير", ["CSV", "Excel"])
    
    logs = get_logs(st.session_state['user_id'], days)
    
    if logs:
        df = pd.DataFrame(logs, columns=['id', 'date', 'name', 'category', 'sets', 'reps', 'weight', 'notes', 'duration'])
        
        # تحويل التاريخ
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d %H:%M')
        
        # عرض الجدول مع إمكانية الحذف
        st.dataframe(df[['date', 'name', 'category', 'sets', 'reps', 'weight', 'duration', 'notes']], 
                    use_container_width=True,
                    column_config={
                        "date": "التاريخ",
                        "name": "التمرين",
                        "category": "الفئة",
                        "sets": "الجولات",
                        "reps": "التكرارات",
                        "weight": "الوزن (كجم)",
                        "duration": "المدة (دقيقة)",
                        "notes": "ملاحظات"
                    })
        
        # تصدير
        if st.button(f"📥 تحميل {export_format}", use_container_width=True):
            if export_format == "CSV":
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button("تحميل CSV", csv, "fitness_log.csv", "text/csv")
            else:
                from io import BytesIO
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='سجل التمارين')
                st.download_button("تحميل Excel", output.getvalue(), "fitness_log.xlsx")
        
        # حذف سجل
        st.markdown("---")
        st.subheader("🗑️ حذف سجلات")
        log_to_delete = st.selectbox("اختر السجل للحذف", 
                                     [f"{row['date']} - {row['name']}" for _, row in df.iterrows()])
        if st.button("حذف السجل المحدد", type="secondary"):
            idx = list(df.iterrows())[list(df['date'] + ' - ' + df['name']).index(log_to_delete)][0]
            delete_log(df.iloc[list(df['date'] + ' - ' + df['name']).index(log_to_delete)]['id'])
            st.success("تم الحذف!")
            st.rerun()
    else:
        st.info("لا يوجد سجل في هذه الفترة")

# ==================== صفحة الإحصائيات ====================
def stats_page():
    st.title("📈 الإحصائيات المتقدمة")
    
    days = st.selectbox("الفترة", [7, 14, 30, 90], index=2, key="stats_days")
    stats = get_stats(st.session_state['user_id'], days)
    
    if stats:
        df_stats = pd.DataFrame(stats, columns=['الفئة', 'عدد التمارين', 'مجموع الجولات', 'مجموع التكرارات'])
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(df_stats, x='الفئة', y='عدد التمارين', title="عدد التمارين حسب الفئة", color='الفئة')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(df_stats, x='الفئة', y='مجموع الجولات', title="مجموع الجولات حسب الفئة", color='الفئة')
            st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df_stats, use_container_width=True)
    else:
        st.info("لا توجد بيانات كافية")

# ==================== البرنامج الرئيسي ====================
def main():
    init_db()
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    if not st.session_state['logged_in']:
        login_page()
        return
    
    # الشريط الجانبي
    with st.sidebar:
        st.title("💪 Fitness Planner")
        st.markdown(f"**مرحباً {st.session_state['username']}** 👋")
        st.markdown("---")
        
        page = st.radio(
            "📱 القائمة",
            ["📊 لوحة التحكم", "📚 التمارين", "📝 تسجيل تمرين", "📋 السجل", "📈 إحصائيات"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        if st.button("🚪 تسجيل الخروج", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    
    # توجيه الصفحات
    page_map = {
        "📊 لوحة التحكم": dashboard,
        "📚 التمارين": exercises_page,
        "📝 تسجيل تمرين": log_page,
        "📋 السجل": history_page,
        "📈 إحصائيات": stats_page
    }
    
    page_map[page]()

if __name__ == "__main__":
    main()

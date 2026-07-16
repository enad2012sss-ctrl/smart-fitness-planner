import streamlit as st
import sqlite3
import pandas as pd

# ================== دالة تهيئة قاعدة البيانات ==================
def init_db():
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    
    # 1. إنشاء الجدول مع مفتاح أساسي متزايد (id) لتجنب مشاكل التكرار
    c.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,          -- UNIQUE يمنع التكرار
            muscle_group TEXT NOT NULL,
            equipment TEXT,
            description TEXT
        )
    ''')
    
    # 2. بيانات نموذجية (استبدلها بقائمتك الحقيقية)
    sample_data = [
        ('Bench Press', 'Chest', 'Barbell', 'Lie on a flat bench and press the bar up.'),
        ('Squat', 'Legs', 'Barbell', 'Stand with feet shoulder-width apart, lower hips back and down.'),
        ('Pull-up', 'Back', 'Pull-up bar', 'Hang from a bar and pull your chest up to it.'),
        ('Plank', 'Core', 'None', 'Hold a push-up position with elbows on the ground.'),
        ('Bicep Curl', 'Arms', 'Dumbbell', 'Curl the dumbbell up while keeping elbows fixed.'),
    ]
    
    # 3. إدراج البيانات بأمان (تجنب تكرار الأسماء باستخدام INSERT OR IGNORE)
    c.executemany('''
        INSERT OR IGNORE INTO exercises (name, muscle_group, equipment, description)
        VALUES (?, ?, ?, ?)
    ''', sample_data)
    
    conn.commit()
    conn.close()

# ================== دالة جلب البيانات ==================
def load_exercises():
    conn = sqlite3.connect('fitness.db')
    df = pd.read_sql_query("SELECT * FROM exercises", conn)
    conn.close()
    return df

# ================== واجهة Streamlit ==================
def main():
    st.set_page_config(page_title="Smart Fitness Planner", layout="wide")
    st.title("🏋️ Smart Fitness Planner")
    
    # تهيئة قاعدة البيانات عند أول تحميل
    init_db()
    
    # عرض البيانات
    st.subheader("📋 قائمة التمارين")
    df = load_exercises()
    
    if df.empty:
        st.warning("لا توجد تمارين في القاعدة بعد.")
    else:
        st.dataframe(df, use_container_width=True)
    
    # إضافة تمرين جديد (اختياري)
    with st.expander("➕ إضافة تمرين جديد"):
        with st.form("add_form"):
            name = st.text_input("اسم التمرين")
            muscle = st.selectbox("المجموعة العضلية", ["Chest", "Back", "Legs", "Arms", "Core", "Shoulders"])
            equip = st.text_input("الأجهزة المطلوبة")
            desc = st.text_area("الوصف")
            submitted = st.form_submit_button("حفظ")
            
            if submitted and name:
                conn = sqlite3.connect('fitness.db')
                c = conn.cursor()
                try:
                    c.execute('''
                        INSERT INTO exercises (name, muscle_group, equipment, description)
                        VALUES (?, ?, ?, ?)
                    ''', (name, muscle, equip, desc))
                    conn.commit()
                    st.success("تمت الإضافة بنجاح!")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("❌ هذا التمرين موجود مسبقاً (الاسم مكرر).")
                finally:
                    conn.close()

if __name__ == "__main__":
    main()

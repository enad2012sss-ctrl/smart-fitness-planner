import streamlit as st
import pandas as pd
from fpdf import FPDF

# 1. قاعدة بيانات ضخمة مع GIF لكل تمرين
fitness_db = {
    "حديد": [
        {"name": "Bench Press", "ar": "ضغط الصدر بالبار", "gif": "https://media.giphy.com/media/xT5LMHxhOfscxPfIfm/giphy.gif", "muscle": "الصدر", "benefit": "تضخيم الصدر وزيادة القوة"},
        {"name": "Squat", "ar": "سكوات", "gif": "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif", "muscle": "الأرجل", "benefit": "بناء الكتلة العضلية للرجل"},
        {"name": "Deadlift", "ar": "الرفعة الميتة", "gif": "https://media.giphy.com/media/3oGRFrq6v6RwG5Z8wI/giphy.gif", "muscle": "الظهر", "benefit": "تقوية الظهر والجزء الخلفي"},
        {"name": "Bicep Curl", "ar": "تكوير الباي", "gif": "https://media.giphy.com/media/3o7aD2saNWQLZ1WnM4/giphy.gif", "muscle": "الباي", "benefit": "تضخيم عضلة البايسبس"}
    ],
    "علاج طبيعي": [
        {"name": "Knee Extension", "ar": "تمديد الركبة", "gif": "https://media.giphy.com/media/3o7abKhuvqV5nF4kKY/giphy.gif", "muscle": "الركبة", "benefit": "استشفاء إصابات الركبة"},
        {"name": "Shoulder Rotation", "ar": "لف الكتف", "gif": "https://media.giphy.com/media/3o7aCTfyhYawdOXcFW/giphy.gif", "muscle": "الكتف", "benefit": "علاج الكتف المتجمد"},
        {"name": "Cat-Cow Stretch", "ar": "تمديد القط والبقرة", "gif": "https://media.giphy.com/media/3oGRF5a3zW6zY5Z6E8/giphy.gif", "muscle": "الظهر", "benefit": "تخفيف ألم أسفل الظهر"}
    ],
    "يوجا": [
        {"name": "Child Pose", "ar": "وضعية الطفل", "gif": "https://media.giphy.com/media/3oGRF5a3zW6zY5Z6E8/giphy.gif", "muscle": "الظهر", "benefit": "استرخاء الظهر وتخفيف التوتر"},
        {"name": "Downward Dog", "ar": "الكلب النازل", "gif": "https://media.giphy.com/media/l4FGt8w0d9i9Qg7Dq/giphy.gif", "muscle": "الجسم كامل", "benefit": "إطالة العمود الفقري"}
    ],
    "كارديو": [
        {"name": "Jumping Jacks", "ar": "القفز فتح وضم", "gif": "https://media.giphy.com/media/3o7abKhuvqV5nF4kKY/giphy.gif", "muscle": "الجسم كامل", "benefit": "حرق الدهون ورفع اللياقة"},
        {"name": "High Knees", "ar": "الجري في المكان", "gif": "https://media.giphy.com/media/3oGRFrq6v6RwG5Z8wI/giphy.gif", "muscle": "البطن والرجل", "benefit": "حرق سعرات وتنشيف"}
    ]
}

# 2. قاموس الترجمة
translations = {
    "العربية": {"title": "🏆 منصة اللياقة البدنية الاحترافية", "tab1": "🏋️ التمارين", "tab2": "🩹 علاج طبيعي", "tab3": "🤖 المدرب الذكي", "tab4": "📊 حاسبة السعرات", "choose_sport": "اختر نوع الرياضة", "benefits": "**الفوائد:**", "muscle": "**العضلة:**", "rehab_title": "إعادة التأهيل", "injury": "مكان الإصابة", "ai_title": "المدرب الذكي", "ai_prompt": "اكتب هدفك", "calc_title": "حاسبة السعرات", "weight": "الوزن kg", "height": "الطول cm", "age": "العمر", "gender": "الجنس", "goal": "الهدف", "calculate": "احسب", "download": "تحميل الجدول PDF"},
    "English": {"title": "🏆 Pro Fitness AI Platform", "tab1": "🏋️ Exercises", "tab2": "🩹 Physical Therapy", "tab3": "🤖 AI Coach", "tab4": "📊 Calorie Calculator", "choose_sport": "Choose Sport Type", "benefits": "**Benefits:**", "muscle": "**Muscle:**", "rehab_title": "Rehabilitation", "injury": "Injury Location", "ai_title": "AI Coach", "ai_prompt": "Write your goal", "calc_title": "Calorie Calculator", "weight": "Weight kg", "height": "Height cm", "age": "Age", "gender": "Gender", "goal": "Goal", "calculate": "Calculate", "download": "Download PDF"}
}

st.set_page_config(page_title="Pro Fitness AI", layout="wide")

lang = st.sidebar.selectbox("Language / اللغة", ["العربية", "English"])
t = translations[lang]

st.title(t["title"])

# 3. 4 تبويبات
tab1, tab2, tab3, tab4 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"]])

# تبويب 1: التمارين + GIF
with tab1:
    category = st.selectbox(t["choose_sport"], list(fitness_db.keys()))
    search = st.text_input("بحث عن تمرين" if lang=="العربية" else "Search Exercise")

    for ex in fitness_db[category]:
        if search.lower() in ex["name"].lower() or search in ex["ar"]:
            c1, c2 = st.columns([1, 3])
            name = ex["ar"] if lang == "العربية" else ex["name"]
            c1.image(ex["gif"], width=180)
            c2.subheader(name)
            c2.write(f"{t['muscle']} {ex['muscle']}")
            c2.write(f"{t['benefits']} {ex['benefit']}")
            st.divider()

# تبويب 2: علاج طبيعي
with tab2:
    st.subheader(t["rehab_title"])
    injury_map = {"الركبة": "علاج طبيعي", "الكتف": "علاج طبيعي", "الظهر": "علاج طبيعي"}
    injury = st.selectbox(t["injury"], list(injury_map.keys()))
    if injury:
        for ex in fitness_db[injury_map[injury]]:
            if ex["muscle"] == injury:
                c1, c2 = st.columns([1, 3])
                name = ex["ar"] if lang == "العربية" else ex["name"]
                c1.image(ex["gif"], width=180)
                c2.subheader(name)
                c2.write(f"{t['benefits']} {ex['benefit']}")
                st.divider()

# تبويب 3: المدرب الذكي
with tab3:
    st.subheader(t["ai_title"])
    goal = st.text_area(t["ai_prompt"])
    if st.button("إنشاء خطة" if lang=="العربية" else "Generate Plan"):
        st.success("مثال خطة 7 أيام:")
        st.markdown("""
        **اليوم 1 - صدر وتراي**: Bench Press 4x12, Bicep Curl 3x15
        **اليوم 2 - رجل**: Squat 4x10, Deadlift 3x8
        **التغذية**: بروتين 2g لكل كيلو من وزنك
        """)

# تبويب 4: حاسبة السعرات + PDF
with tab4:
    st.subheader(t["calc_title"])
    col1, col2 = st.columns(2)
    weight = col1.number_input(t["weight

import streamlit as st

# قاموس الترجمة (يمكنك إضافة أي لغة هنا)
translations = {
    "العربية": {
        "title": "🏆 منصة اللياقة البدنية الاحترافية",
        "search": "🔍 ابحث عن تمرينك هنا...",
        "benefit": "الفوائد",
        "sets": "الجلسات",
        "reps": "التكرار",
        "bmi_title": "📊 حاسبة مؤشر كتلة الجسم",
        "weight": "الوزن (كجم)",
        "height": "الطول (سم)",
        "ai_title": "🤖 المدرب الذكي (AI)"
    },
    "English": {
        "title": "🏆 Professional Fitness Platform",
        "search": "🔍 Search for your exercise here...",
        "benefit": "Benefits",
        "sets": "Sets",
        "reps": "Reps",
        "bmi_title": "📊 BMI Calculator",
        "weight": "Weight (kg)",
        "height": "Height (cm)",
        "ai_title": "🤖 AI Personal Trainer"
    }
}

# اختيار اللغة
lang = st.sidebar.selectbox("🌐 Select Language / اختر اللغة", ["العربية", "English"])
t = translations[lang]

# قاعدة البيانات
database = {
    "Fitness": [
        {"name": "Jumping Rope", "ar_name": "نط الحبل", "gif": "https://media.giphy.com/media/l41lTjJp8whYyG5wY/giphy.gif", "sets": "4", "reps": "60 sec", "benefit": "Heart health"},
    ]
}

st.title(t["title"])

# عرض التمارين بناءً على اللغة
search = st.text_input(t["search"])
for cat, exercises in database.items():
    for ex in exercises:
        name = ex["ar_name"] if lang == "العربية" else ex["name"]
        if search.lower() in name.lower() or search == "":
            col1, col2 = st.columns([1, 2])
            col1.image(ex['gif'], width=200)
            col2.subheader(name)
            col2.write(f"**{t['benefit']}:** {ex['benefit']}")
            col2.caption(f"{t['sets']}: {ex['sets']} | {t['reps']}: {ex['reps']}")
            st.divider()

# القياسات
with st.sidebar:
    st.subheader(t["bmi_title"])
    w = st.number_input(t["weight"], 40, 200, 70)
    h = st.number_input(t["height"], 140, 220, 175)
    st.metric("BMI", f"{w / ((h/100)**2):.1f}")

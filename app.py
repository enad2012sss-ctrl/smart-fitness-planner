import streamlit as st

# قاعدة بيانات مركزية (قابلة للتوسع لمئات التمارين)
database = {
    "فتنس": [
        {"name": "نط الحبل", "gif": "https://media.giphy.com/media/l41lTjJp8whYyG5wY/giphy.gif", "sets": "4", "reps": "60 ثانية", "benefit": "تحسين نبضات القلب"},
        {"name": "تسلق الجبال", "gif": "https://media.giphy.com/media/3o7TKMGpxxHOGTdzJC/giphy.gif", "sets": "3", "reps": "45 ثانية", "benefit": "حرق دهون البطن"}
    ],
    "كمال أجسام": [
        {"name": "ضغط الصدر بالبار", "gif": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjEx.../giphy.gif", "sets": "4", "reps": "10", "benefit": "تضخيم الصدر"},
        {"name": "سكوات", "gif": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjEx.../giphy.gif", "sets": "4", "reps": "12", "benefit": "قوة الأرجل"}
    ],
    "يوجا": [
        {"name": "وضعية الطفل", "gif": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjEx.../giphy.gif", "sets": "1", "reps": "2 دقيقة", "benefit": "استرخاء الجسم"}
    ]
}

# دمج كافة التمارين للبحث الشامل
all_exercises = [ex for cat in database.values() for ex in cat]

st.set_page_config(page_title="Fitness Pro", layout="wide")
st.title("🏆 منصة اللياقة البدنية الاحترافية")

# التبويبات الرئيسية
tab1, tab2, tab3 = st.tabs(["البحث عن التمارين", "القياسات", "المساعد الذكي (AI)"])

with tab1:
    search = st.text_input("🔍 ابحث عن تمرينك هنا...")
    results = [ex for ex in all_exercises if search.lower() in ex['name'].lower()] if search else all_exercises
    for ex in results:
        c1, c2 = st.columns([1, 2])
        c1.image(ex['gif'], width=200)
        c2.subheader(ex['name'])
        c2.write(f"**الفوائد:** {ex['benefit']}")
        c2.caption(f"الجلسات: {ex['sets']} | التكرار: {ex['reps']}")
        st.divider()

with tab2:
    st.subheader("📊 حاسبة مؤشر كتلة الجسم")
    weight = st.number_input("الوزن (كجم)", 40, 200, 70)
    height = st.number_input("الطول (سم)", 140, 220, 175)
    bmi = weight / ((height/100)**2)
    st.metric("النتيجة", f"{bmi:.1f}")

with tab3:
    st.subheader("🤖 المدرب الذكي (AI)")
    st.write("اطرح سؤالاً عن برنامج تدريبي أو نصيحة رياضية...")
    user_query = st.text_input("مثال: صمم لي جدول تمرين للمبتدئين")
    if user_query:
        st.info("جاري التحليل... (يرجى ربط مفتاح OpenAI API في إعدادات التطبيق)")

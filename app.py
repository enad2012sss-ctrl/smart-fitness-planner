import streamlit as st

# قاعدة بيانات مُحدثة لاستيعاب التمارين (يمكنك إضافة المئات هنا بنفس النمط)
database = {
    "فتنس": [
        {"name": "نط الحبل", "gif": "https://media.giphy.com/media/l41lTjJp8whYyG5wY/giphy.gif", "sets": "4", "reps": "60 ثانية", "benefit": "تحسين نبضات القلب"},
        {"name": "تسلق الجبال", "gif": "https://media.giphy.com/media/3o7TKMGpxxHOGTdzJC/giphy.gif", "sets": "3", "reps": "45 ثانية", "benefit": "حرق دهون البطن"}
    ],
    "كمال أجسام": [
        {"name": "ضغط الصدر بالبار", "gif": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjEx.../giphy.gif", "sets": "4", "reps": "10", "benefit": "تضخيم عضلات الصدر"},
        {"name": "سكوات", "gif": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjEx.../giphy.gif", "sets": "4", "reps": "12", "benefit": "قوة الأرجل"}
    ],
    "إطالات ويوجا": [
        {"name": "وضعية الطفل", "gif": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjEx.../giphy.gif", "sets": "1", "reps": "2 دقيقة", "benefit": "استرخاء الجسم"},
        {"name": "إطالة الصدر", "gif": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjEx.../giphy.gif", "sets": "2", "reps": "30 ثانية", "benefit": "مرونة الكتف"}
    ]
}

# دمج جميع التمارين في قائمة واحدة للبحث
all_exercises = []
for cat in database.values():
    all_exercises.extend(cat)

st.title("🔍 محرك البحث الرياضي الذكي")

# شريط البحث
search_query = st.text_input("اكتب اسم التمرين الذي تبحث عنه... (مثلاً: سكوات، نط الحبل)")

# فلترة التمارين بناءً على البحث
if search_query:
    results = [ex for ex in all_exercises if search_query.lower() in ex['name'].lower()]
else:
    results = all_exercises

# عرض النتائج
for ex in results:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(ex['gif'], width=200)
    with col2:
        st.subheader(ex['name'])
        st.write(f"**الفوائد:** {ex['benefit']}")
        st.caption(f"الجلسات: {ex['sets']} | التكرار: {ex['reps']}")
    st.divider()

# قسم القياسات
st.sidebar.subheader("📊 قياسات الجسم")
w = st.sidebar.number_input("الوزن (كجم)", 40, 200, 70)
bmi = w / (1.75**2)
st.sidebar.metric("مؤشر كتلة الجسم", f"{bmi:.1f}")

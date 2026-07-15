import streamlit as st

# إعداد عنوان الصفحة وأيقونة تفاعلية
st.set_page_config(page_title="مخطط اللياقة الذكي", page_icon="🏋️‍♂️")

st.title("🏋️‍♂️ مخطط اللياقة البدنية الذكي")
st.write("أدخل بياناتك للحصول على جدول التمارين المخصص لك مع الشرح بالصور المتحركة:")

# مدخلات المستخدم الذكية
goal = st.selectbox("ما هو هدفك الرياضي الرئيسي؟", ["بناء عضلات", "خسارة وزن وحرق دهون", "لياقة عامة ومرونة"])
level = st.selectbox("ما هو مستواك الرياضي الحالي؟", ["مبتدئ", "متوسط", "متقدم"])
days = st.slider("كم يوماً تستطيع التدرب في الأسبوع؟", min_value=1, max_value=7, value=3)

if st.button("توليد جدول التمارين الذكي"):
    st.success("🤖 تم توليد خطتك المخصصة بنجاح بناءً على خوارزمية التحسين:")
    
    # محاكاة بسيطة للذكاء الاصطناعي بناءً على مدخلات المستخدم
    if goal == "بناء عضلات":
        st.subheader("📅 اليوم الأول: تمارين الجزء العلوي (Upper Body)")
        st.write("- **تمرين الضغط (Push-ups):** 3 جولات × 12 تكرار.")
        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Z5bmt3OG9oZmsydG13c3V5M2RjNnY3ZzR5ZWdndWZqd2g2cWp6ZCZjdD1n/3o7TKoWXm3okO1kg6A/giphy.gif", caption="طريقة أداء تمرين الضغط بشكل صحيح")
        
        st.write("- **تمرين العقلة أو السحب (Pull-ups/Rows):** 3 جولات × 10 تكرارات.")
        
    elif goal == "خسارة وزن وحرق دهون":
        st.subheader("📅 اليوم الأول: تمارين كارديو وحرق دهون (HIIT)")
        st.write("- **تمرين القفز (Jumping Jacks):** 4 جولات × 45 ثانية.")
        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM2Zkb2NodTVvMWNndmNqajRpdHBsZHFzcmUyd250cjIxbWlmbTVwMCZjdD1n/l3q2XhfQ8oCkm1xs4/giphy.gif", caption="تمرين القفز لحرق الدهون")
        
    else:
        st.subheader("📅 اليوم الأول: لياقة عامة وإطالات")
        st.write("- **تمارين تمدد وإطالات كاملة للجسم.**")

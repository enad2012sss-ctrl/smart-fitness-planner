import streamlit as st
import pandas as pd
import datetime

# 4 & 5. قاموس التمارين مع وسائط مخصصة
exercises_db = {
    "حديد": {"name": "السكوات", "video": "https://youtu.be/some_id1", "desc": "لتقوية الأرجل"},
    "منزلي": {"name": "الضغط", "video": "https://youtu.be/some_id2", "desc": "لشد الصدر"},
    "يوغا": {"name": "وضعية المحارب", "video": "https://youtu.be/some_id3", "desc": "للاستشفاء"}
}

# 7. نظام الإشعارات المخصص (محاكاة)
def schedule_notification(time, goal):
    st.success(f"تم جدولة إشعار تحفيزي لـ {goal} في الساعة {time.strftime('%H:%M')}")

st.title("🏆 منصة اللياقة الذكية المتكاملة")

# 9. دمج القياسات في قاعدة بيانات (Dataframe)
if 'measurements' not in st.session_state:
    st.session_state.measurements = pd.DataFrame(columns=["التاريخ", "الوزن", "الهدف"])

# واجهة الميزات
tab1, tab2, tab3 = st.tabs(["التمارين والوسائط", "القياسات والبيانات", "جدولة النشاط"])

with tab1:
    choice = st.selectbox("اختر نوع التمرين:", list(exercises_db.keys()))
    st.write(f"### {exercises_db[choice]['name']}")
    st.video(exercises_db[choice]['video']) # ميزة 4 و 5
    st.info(exercises_db[choice]['desc'])

with tab2:
    st.subheader("تسجيل القياسات الجسمانية") # ميزة 9
    new_weight = st.number_input("الوزن الحالي (كجم)")
    if st.button("حفظ القياس"):
        new_data = {"التاريخ": datetime.date.today(), "الوزن": new_weight, "الهدف": "تنشيف"}
        st.session_state.measurements = pd.concat([st.session_state.measurements, pd.DataFrame([new_data])], ignore_index=True)
    st.table(st.session_state.measurements)

with tab3:
    st.subheader("جدولة التنبيهات (ميزة 7)") # ميزة 7
    notif_time = st.time_input("اختر وقت التنبيه اليومي:")
    if st.button("تفعيل التنبيه"):
        schedule_notification(notif_time, "ممارسة الرياضة")

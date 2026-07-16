import streamlit as st

from init_db import init_database
from database import SessionLocal
from auth import create_user, login_user

# إنشاء قاعدة البيانات
init_database()

st.set_page_config(
    page_title="Smart Fitness AI",
    page_icon="💪",
    layout="wide"
)

st.title("💪 Smart Fitness AI")
st.write("مرحبًا بك في النسخة الاحترافية من التطبيق.")

menu = st.sidebar.selectbox(
    "القائمة",
    [
        "الرئيسية",
        "تسجيل الدخول",
        "إنشاء حساب"
    ]
)

if menu == "الرئيسية":

    st.header("🏠 الصفحة الرئيسية")
    st.info("سيتم إضافة لوحة التحكم هنا.")

elif menu == "تسجيل الدخول":

    st.header("🔐 تسجيل الدخول")
    st.info("سنقوم ببرمجتها في الخطوة التالية.")

elif menu == "إنشاء حساب":

    st.header("📝 إنشاء حساب")

    username = st.text_input("اسم المستخدم")

    email = st.text_input("البريد الإلكتروني")

    password = st.text_input(
        "كلمة المرور",
        type="password"
    )

    age = st.number_input(
        "العمر",
        min_value=15,
        max_value=100,
        value=25
    )

    weight = st.number_input(
        "الوزن",
        min_value=40.0,
        max_value=200.0,
        value=70.0
    )

    height = st.number_input(
        "الطول",
        min_value=140.0,
        max_value=220.0,
        value=170.0
    )

    level = st.selectbox(
        "مستوى اللياقة",
        [
            "مبتدئ",
            "متوسط",
            "متقدم"
        ]
    )

    goal = st.selectbox(
        "الهدف",
        [
            "تنشيف",
            "تضخيم",
            "المحافظة"
        ]
    )

    if st.button("إنشاء الحساب"):

        db = SessionLocal()

        user = create_user(
            db,
            username,
            email,
            password,
            age,
            weight,
            height,
            level,
            goal
        )

        db.close()

        if user:
            st.success("✅ تم إنشاء الحساب بنجاح")

        else:
            st.error("اسم المستخدم أو البريد الإلكتروني مستخدم بالفعل")

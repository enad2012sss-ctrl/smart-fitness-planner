import streamlit as st
from init_db import init_database

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
    st.write("سنربطها بقاعدة البيانات في الخطوة القادمة.")

elif menu == "إنشاء حساب":
    st.header("📝 إنشاء حساب")
    st.write("سنضيف نموذج التسجيل في الخطوة القادمة.")

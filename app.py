
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# تنظیمات اولیه صفحه
st.set_page_config(page_title="مدیریت هزینه‌ها", page_icon="💰")

st.title("💰 مدیریت هزینه‌های خانوادگی")

# اتصال به Google Sheet
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("expenseapp-465605-58429a8da4fc.json", scope)
client = gspread.authorize(creds)

# آدرس Google Sheet شما
sheet_url = "https://docs.google.com/spreadsheets/d/1yUhjtvWYj1e3BGux72Pcpc7amklK3XKxVj8Cl348eVI/edit#gid=0"
sheet = client.open_by_url(sheet_url).sheet1

# فرم ورود داده‌ها
st.subheader("➕ ثبت هزینه جدید")
category = st.selectbox("دسته خرج:", ["🍔 غذا", "🚗 حمل و نقل", "💡 قبض", "🎉 سرگرمی", "📦 متفرقه"])
amount = st.number_input("مقدار (تومان):", min_value=0)
note = st.text_input("توضیح (اختیاری):")
date = st.date_input("تاریخ:", datetime.date.today())
submit = st.button("ثبت")

# ثبت در Google Sheet
if submit:
    try:
        sheet.append_row([str(date), category, amount, note])
        st.success("✅ هزینه با موفقیت در Google Sheet ذخیره شد!")
    except Exception as e:
        st.error(f"❌ خطا در ذخیره: {e}")

# نمایش گزارش
st.subheader("📊 گزارش هزینه‌ها")
try:
    data = sheet.get_all_values()
    if len(data) > 1:
        for row in data[1:]:
            st.write(f"{row[0]} | {row[1]} | {row[2]} تومان | {row[3]}")
    else:
        st.info("هنوز داده‌ای ثبت نشده.")
except Exception as e:
    st.error(f"خطا در دریافت داده‌ها: {e}")

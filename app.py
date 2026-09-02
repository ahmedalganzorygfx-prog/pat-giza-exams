import base64
import os
import pandas as pd
import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="لوحة تحكم الامتحانات - فرع الجيزة",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 🎨 CSS لتنسيق التطبيق وإصلاح مشكلة الحروف وتوضيح نص القائمة الجانبية
st.markdown(
    """
    <style>
    /* محاذاة RTL */
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl;
    }

    [data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
    }

    /* 🛠️ حل مشكلة الحروف عند تقليص/إخفاء القائمة الجانبية */
    [data-testid="stSidebar"][aria-expanded="false"] {
        margin-left: 0rem !important;
    }
    
    [data-testid="stSidebar"] * {
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    /* 💡 تنسيق صندوق الحقوق والمعلومات في السايدبار ليكون ناصع الوضوح */
    div[data-testid="stSidebar"] div[data-testid="stAlert"] {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3) !important;
    }

    div[data-testid="stSidebar"] div[data-testid="stAlert"] * {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        text-align: center !important;
    }

    /* 🎯 بطاقة الهيدر الملونة والأنيقة */
    .header-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #334155;
        border-radius: 20px;
        padding: 30px 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4), 0 0 15px rgba(56, 189, 248, 0.15);
        margin-bottom: 25px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .header-logo {
        width: 200px;
        height: auto;
        margin-bottom: 15px;
        filter: drop-shadow(0px 4px 10px rgba(0, 0, 0, 0.5));
    }

    .main-title {
        color: #ffffff;
        font-size: 30px;
        font-weight: 800;
        margin-bottom: 8px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }

    .sub-title {
        color: #38bdf8;
        font-size: 22px;
        font-weight: 700;
    }

    /* 🎯 توسيط العناوين الفرعية */
    .section-title-center {
        text-align: center !important;
        font-size: 24px !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        margin-top: 20px !important;
        margin-bottom: 15px !important;
    }

    /* 🔘 أزرار التصفية - مرتبة من اليمين إلى اليسار */
    div[data-testid="stRadio"] > div {
        display: flex !important;
        flex-direction: row !important;
        justify-content: center !important;
        flex-wrap: wrap !important;
        gap: 12px !important;
    }

    div[data-testid="stRadio"] label {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
        color: #e2e8f0 !important;
        border: 2px solid #334155 !important;
        padding: 10px 20px !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        cursor: pointer !important;
        transition: all 0.25s ease-in-out !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
    }

    div[data-testid="stRadio"] label > div:first-child {
        display: none !important;
    }

    div[data-testid="stRadio"] label:hover {
        background: #334155 !important;
        border-color: #38bdf8 !important;
        color: #ffffff !important;
        transform: translateY(-2px) !important;
    }

    div[data-testid="stRadio"] label[data-checked="true"] {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.7) !important;
        transform: scale(1.03) !important;
    }

    /* 📊 توسيط كروت الإحصائيات بالكامل */
    div[data-testid="stMetric"] {
        background-color: #1e293b !important;
        padding: 18px 10px !important;
        border-radius: 14px !important;
        border: 1px solid #334155 !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3) !important;
    }

    div[data-testid="stMetric"] > div {
        width: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        text-align: center !important;
    }

    div[data-testid="stMetricLabel"] > div {
        width: 100% !important;
        text-align: center !important;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-size: 30px !important;
        font-weight: 800 !important;
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        text-align: center !important;
        margin-top: 4px !important;
    }

    div[data-testid="stMetricValue"] > div {
        width: 100% !important;
        text-align: center !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# دالة تحويل الصورة إلى Base64
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        ext = path.split(".")[-1].lower()
        mime_type = "image/png" if ext == "png" else f"image/{ext}"
        return f"data:{mime_type};base64,{encoded_string}"
    return None


# 2. البحث عن اللوجو وعرضه
possible_files = [
    "logo.png",
    "logo.jpg",
    "logo.jpeg",
    "Logo.png",
    "Logo.jpg",
    "Logo.PNG",
]
found_logo = None

for file in possible_files:
    if os.path.exists(file):
        found_logo = file
        break

logo_b64 = get_image_base64(found_logo) if found_logo else ""

header_html = f"""
<div class="header-card">
    {"<img src='" + logo_b64 + "' class='header-logo' />" if logo_b64 else ""}
    <div class="main-title">🏛️ الأكاديمية المهنية للمعلمين - فرع الجيزة</div>
    <div class="sub-title">📝 لوحة تحكم وإحصائيات الامتحانات أونلاين</div>
</div>
"""

st.markdown(header_html, unsafe_allow_html=True)

# 3. القائمة الجانبية (Sidebar)
st.sidebar.header("📁 إدارة البيانات")
uploaded_file = st.sidebar.file_uploader(
    "تحميل ملف الإكسيل (Excel)", type=["xlsx", "xls"]
)

st.sidebar.divider()

# عرض نص حقوق التصميم والتنفيذ بلون ناصع وواضح
st.sidebar.info("✨ تصميم وتنفيذ:\nأحمد الجنزوري - مدير الفرع")

# 4. جلب وتجهيز البيانات
if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, dtype=str).fillna("-")
        df.columns = df.columns.str.strip()
    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة الملف: {e}")
        st.stop()
else:
    st.warning(
        "⚠️ يرجى رفع ملف إكسيل من القائمة الجانبية (يمين الشاشة) لعرض البيانات والإحصائيات."
    )
    st.stop()

# 5. شريط البحث والتاريخ العلوي
col_search, col_date, col_reset = st.columns([2, 2, 1])

with col_search:
    search_query = st.text_input("🔍 بحث بالرقم القومي أو كود المعلم:")

with col_date:
    selected_date = st.date_input("📅 تاريخ الاختبار:", value=None)

with col_reset:
    st.write(" ")
    st.write(" ")
    if st.button("🔄 إعادة تعيين", use_container_width=True):
        st.rerun()

# 6. البرامج التدريبية
st.markdown(
    '<div class="section-title-center">🎯 اختر البرنامج التدريبي</div>',
    unsafe_allow_html=True,
)

program_options = [
    "الكل",
    "تطبيقات تربوية للمعلم المساعد",
    "مدير ووكيل ادارة مدرسية",
    "مدير ووكيل ادارة تعليمية",
    "أساسيات التوجيه الفني",
]

selected_program = st.radio(
    label="اختر البرنامج",
    options=program_options,
    horizontal=True,
    label_visibility="collapsed",
)

# 7. فلترة البيانات
filtered_df = df.copy()

if selected_program != "الكل" and "البرنامج" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["البرنامج"] == selected_program]

if selected_date and "وقت أداء الاختبار" in filtered_df.columns:
    date_str = str(selected_date)
    filtered_df = filtered_df[
        filtered_df["وقت أداء الاختبار"].astype(str).str.startswith(date_str)
    ]

if search_query:
    cond_code = (
        filtered_df["كود المعلم"].str.contains(
            search_query, case=False, na=False
        )
        if "كود المعلم" in filtered_df.columns
        else False
    )
    cond_id = (
        filtered_df["الرقم القومي"].str.contains(
            search_query, case=False, na=False
        )
        if "الرقم القومي" in filtered_df.columns
        else False
    )
    filtered_df = filtered_df[cond_code | cond_id]

# 8. الإحصائيات العامة
st.markdown(
    '<div class="section-title-center">📊 الإحصائيات العامة</div>',
    unsafe_allow_html=True,
)

total = len(filtered_df)
reserved = (
    len(
        filtered_df[
            filtered_df["الحالة"].isin(["محجوز", "حجز اختبار", "لم يختبر"])
        ]
    )
    if "الحالة" in filtered_df.columns
    else 0
)
passed = (
    len(filtered_df[filtered_df["الحالة"] == "اجتاز"])
    if "الحالة" in filtered_df.columns
    else 0
)
failed = (
    len(filtered_df[filtered_df["الحالة"] == "راسب"])
    if "الحالة" in filtered_df.columns
    else 0
)
pending = (
    len(filtered_df[filtered_df["الحالة"] == "قيد الاختبار"])
    if "الحالة" in filtered_df.columns
    else 0
)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("📊 إجمالي الممتحنين", total)
c2.metric("🎟️ حجز اختبار", reserved)
c3.metric("✅ ناجحين", passed)
c4.metric("❌ راسبين", failed)
c5.metric("⏳ قيد الاختبار", pending)

st.divider()

# 9. جدول بيانات المعلمين
st.markdown(
    '<div class="section-title-center">📋 جدول بيانات المعلمين</div>',
    unsafe_allow_html=True,
)

columns_to_show = [
    col
    for col in [
        "كود المعلم",
        "اسم المعلم",
        "الرقم القومي",
        "البرنامج",
        "الحالة",
        "وقت أداء الاختبار",
        "الإجراء",
    ]
    if col in filtered_df.columns
]

if not filtered_df.empty:
    st.dataframe(
        filtered_df[columns_to_show],
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("لا توجد نتائج تطابق خيارات البحث والتصفية لهذا البرنامج.")

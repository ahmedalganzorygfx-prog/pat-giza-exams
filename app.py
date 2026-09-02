import pandas as pd
import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="لوحة تحكم الامتحانات - فرع الجيزة",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# تحسين المظهر وتنسيق الصفحة بـ CSS
st.markdown(
    """
    <style>
    .main { background-color: #f8fafc; }
    div[data-testid="stMetricValue"] { font-weight: bold; }
    .stTable { font-size: 14px; }
    </style>
""",
    unsafe_allow_html=True,
)

# 2. الهيدر والشعار
col_logo, col_title = st.columns([1, 4])

with col_logo:
    # يمكنك إضافة رابط أو مسار اللوجو هنا
    st.image("https://via.placeholder.com/120?text=Logo", width=110)

with col_title:
    st.title("🏛️ الأكاديمية المهنية للمعلمين - فرع الجيزة")
    st.subheader("📝 لوحة تحكم وإحصائيات الامتحانات أونلاين")

st.divider()

# 3. القائمة الجانبية (Sidebar)
st.sidebar.header("📁 إدارة البيانات والبرامج")

# رفع ملف إكسيل
uploaded_file = st.sidebar.file_uploader(
    "تحميل ملف الإكسيل (Excel)", type=["xlsx", "xls"]
)

# قائمة البرامج التدريبية للفلترة
program_options = [
    "الكل",
    "تطبيقات تربوية للمعلم المساعد",
    "مدير ووكيل ادارة مدرسية",
    "مدير ووكيل ادارة تعليمية",
    "أساسيات التوجيه الفني",
]

selected_program = st.sidebar.selectbox(
    "🎯 اختر البرنامج التدريبي:", program_options
)

st.sidebar.divider()
st.sidebar.info("تصميم وتنفيذ:\nأحمد الجنزوري - مدير الفرع")

# 4. جلب وتجهيز البيانات
if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, dtype=str).fillna("-")
        df.columns = df.columns.str.strip()
    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة الملف: {e}")
        st.stop()
else:
    # بيانات افتراضية/توضيحية في حالة عدم رفع ملف
    st.warning(
        "⚠️ يرجى رفع ملف إكسيل من القائمة الجانبية لعرض البيانات والإحصائيات."
    )
    st.stop()

# 5. شريط البحث والفلاتر العلوي
col_search, col_date, col_reset = st.columns([2, 2, 1])

with col_search:
    search_query = st.text_input("🔍 بحث بالرقم القومي أو كود المعلم:")

with col_date:
    selected_date = st.date_input("📅 تاريخ الاختبار:", value=None)

# تطبيق الفلاتر على DataFrame
filtered_df = df.copy()

# فلترة البرنامج
if selected_program != "الكل" and "البرنامج" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["البرنامج"] == selected_program
    ]

# فلترة التاريخ
if selected_date and "وقت أداء الاختبار" in filtered_df.columns:
    date_str = str(selected_date)
    filtered_df = filtered_df[
        filtered_df["وقت أداء الاختبار"].astype(str).str.startswith(date_str)
    ]

# فلترة البحث
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

# 6. حساب الإحصائيات والأرقام
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

# 7. عرض بطاقات الإحصائيات الخمس الـ 5 Cards
st.write("### 📊 الإحصائيات العامة")
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("📊 إجمالي الممتحنين", total)
c2.metric("🎟️ حجز اختبار", reserved)
c3.metric("✅ ناجحين", passed)
c4.metric("❌ راسبين", failed)
c5.metric("⏳ قيد الاختبار", pending)

st.divider()

# 8. عرض الجدول التفاعلي للبيانات
st.write("### 📋 جدول بيانات المعلمين")

# تحديد وتريب الأعمدة المعروضة
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
        filtered_df[columns_to_show], use_container_width=True, hide_index=True
    )
else:
    st.info("لا توجد نتائج تطابق خيارات البحث والتصفية.")

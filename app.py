import base64
import glob
import os
import altair as alt
import pandas as pd
import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="لوحة تحكم الامتحانات - فرع الجيزة",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 🎨 CSS لتنسيق التطبيق ومحاذاة الجدول والعناصر من اليمين
st.markdown(
    """
    <style>
    /* محاذاة RTL عامة */
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl;
    }

    /* 🎯 محاذاة عناوين وأجسام جدول البيانات من اليمين للجميع */
    [data-testid="stDataFrame"] div[role="columnheader"] {
        text-align: right !important;
        justify-content: flex-start !important;
        direction: rtl !important;
    }

    [data-testid="stDataFrame"] div[role="gridcell"] {
        text-align: right !important;
        direction: rtl !important;
    }

    /* 🎯 محاذاة وتوسيط عناصر السايدبار بالكامل */
    [data-testid="stSidebar"] {
        direction: rtl;
        text-align: center !important;
    }

    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }

    /* 🛠️ إخفاء عناصر السايدبار عند التقليص */
    [data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarContent"] {
        display: none !important;
    }

    /* 🎯 توسيط عنوان السايدبار */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        text-align: center !important;
        width: 100% !important;
    }

    /* 🔘 توسيط حاوية أزرار الراديو بداخل السايدبار */
    [data-testid="stSidebar"] div[data-testid="stRadio"] {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
    }

    [data-testid="stSidebar"] div[data-testid="stRadio"] > div {
        display: flex !important;
        flex-direction: column !important;
        gap: 10px !important;
        width: 100% !important;
        align-items: center !important;
    }

    /* 🎨 تنسيق أزرار التبويبات وتوسيط النص بالداخل */
    [data-testid="stSidebar"] div[data-testid="stRadio"] label {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
        color: #e2e8f0 !important;
        border: 2px solid #334155 !important;
        padding: 12px 15px !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        font-size: 14px !important;
        cursor: pointer !important;
        transition: all 0.25s ease-in-out !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
    }

    [data-testid="stSidebar"] div[data-testid="stRadio"] label > div:first-child {
        display: none !important;
    }

    [data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {
        background: #334155 !important;
        border-color: #38bdf8 !important;
        color: #ffffff !important;
        transform: translateY(-2px) !important;
    }

    [data-testid="stSidebar"] div[data-testid="stRadio"] label[data-checked="true"] {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.6) !important;
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

    /* 🎨 تصميم خريطة البرامج المخصصة (Custom Legend) */
    .custom-legend-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 15px;
        margin-top: 15px;
        direction: rtl;
    }

    .custom-legend-item {
        display: flex;
        align-items: center;
        gap: 8px;
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 8px 16px;
        border-radius: 20px;
        color: #ffffff;
        font-weight: 700;
        font-size: 14px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    .legend-color-dot {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        display: inline-block;
    }

    /* 💡 بطاقة الحقوق في أسفل الصفحة (Footer) */
    .page-footer-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #38bdf8;
        border-radius: 16px;
        padding: 15px 25px;
        text-align: center;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4);
        margin: 40px auto 20px auto;
        max-width: 450px;
    }

    .page-footer-card p {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
        margin: 0 !important;
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
st.sidebar.markdown(
    "<h3 style='text-align: center;'>🎯 البرامج التدريبية</h3>",
    unsafe_allow_html=True,
)

program_options = [
    "الكل",
    "تطبيقات تربوية للمعلم المساعد",
    "مدير ووكيل ادارة مدرسية",
    "مدير ووكيل ادارة تعليمية",
    "أساسيات التوجيه الفني",
]

selected_program = st.sidebar.radio(
    label="اختر البرنامج التدريبي:",
    options=program_options,
    index=0,
    label_visibility="collapsed",
)


# 4. قراءة البيانات
@st.cache_data
def load_data_from_project():
    excel_files = glob.glob("*.xlsx") + glob.glob("*.xls")
    if not excel_files:
        return None, "لم يتم العثور على أي ملف إكسيل (.xlsx أو .xls) في مجلد المشروع."

    file_path = excel_files[0]
    try:
        df = pd.read_excel(file_path, dtype=str).fillna("-")
        df.columns = df.columns.str.strip()
        return df, None
    except Exception as e:
        return None, f"حدث خطأ أثناء قراءة الملف {file_path}: {e}"


df, err_msg = load_data_from_project()

if err_msg:
    st.error(f"⚠️ {err_msg}")
    st.stop()

# 5. شريط البحث والتاريخ
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

# 6. فلترة البيانات
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

# 7. الإحصائيات العامة
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

# 🍩 الرسم البياني الدائري التفاعلي + خريطة برامج مخصصة
if "البرنامج" in df.columns and not df.empty:
    st.markdown(
        '<div class="section-title-center">🍩 توزيع الممتحنين حسب البرنامج التدريبي</div>',
        unsafe_allow_html=True,
    )

    prog_counts = df["البرنامج"].value_counts().reset_index()
    prog_counts.columns = ["البرنامج_التدريبي", "عدد_الممتحنين"]

    colors = [
        "#38bdf8",
        "#f59e0b",
        "#10b981",
        "#ec4899",
        "#8b5cf6",
        "#6366f1",
        "#14b8a6",
    ]

    pie_chart = (
        alt.Chart(prog_counts)
        .mark_arc(innerRadius=65, outerRadius=125)
        .encode(
            theta=alt.Theta(field="عدد_الممتحنين", type="quantitative"),
            color=alt.Color(
                field="البرنامج_التدريبي",
                type="nominal",
                scale=alt.Scale(
                    domain=prog_counts["البرنامج_التدريبي"].tolist(),
                    range=colors[: len(prog_counts)],
                ),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("البرنامج_التدريبي", title="البرنامج"),
                alt.Tooltip("عدد_الممتحنين", title="عدد الممتحنين"),
            ],
        )
        .properties(height=320)
        .configure_view(strokeWidth=0)
    )

    st.altair_chart(pie_chart, use_container_width=True)

    legend_items = []
    for idx, row in prog_counts.iterrows():
        color = colors[idx % len(colors)]
        label = row["البرنامج_التدريبي"]
        count = row["عدد_الممتحنين"]
        item = f"""<div class="custom-legend-item">
            <span class="legend-color-dot" style="background-color: {color};"></span>
            <span>{label} ({count})</span>
        </div>"""
        legend_items.append(item)

    legend_html = f'<div class="custom-legend-container">{"".join(legend_items)}</div>'
    st.markdown(legend_html, unsafe_allow_html=True)

st.divider()

# 8. جدول بيانات المعلمين
st.markdown(
    '<div class="section-title-center">📋 جدول بيانات المعلمين</div>',
    unsafe_allow_html=True,
)

# 🎯 عكس ترتيب القائمة لتظهر بصرية في الجدول من اليمين إلى اليسار:
# (أقصى اليمين: كود المعلم -> اسم المعلم -> الرقم القومي -> البرنامج -> الحالة -> وقت أداء الاختبار :أقصى اليسار)
desired_order_rtl = [
    "وقت أداء الاختبار",
    "الحالة",
    "البرنامج",
    "الرقم القومي",
    "اسم المعلم",
    "كود المعلم",
]

# التأكد من وجود العمود في الملف
columns_to_show = [
    col for col in desired_order_rtl if col in filtered_df.columns
]

if not filtered_df.empty:
    st.dataframe(
        filtered_df[columns_to_show],
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("لا توجد نتائج تطابق خيارات البحث والتصفية لهذا البرنامج.")

# 9. بطاقة الحقوق في أسفل الصفحة
st.markdown(
    """
    <div class="page-footer-card">
        <p>✨ تصميم وتنفيذ: <b>أحمد الجنزوري - مدير الفرع</b></p>
    </div>
    """,
    unsafe_allow_html=True,
)

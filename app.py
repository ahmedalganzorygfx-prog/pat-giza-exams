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
    initial_sidebar_state="collapsed",
)

# 🎨 CSS لتنسيق التطبيق المخصص للموبايل والشاشات المختلفة
st.markdown(
    """
    <style>
    /* محاذاة RTL عامة */
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl;
    }

    /* 🎯 محاذاة عناوين وأجسام جدول البيانات */
    [data-testid="stDataFrame"] div[role="columnheader"],
    [data-testid="stDataFrame"] div[role="gridcell"] {
        text-align: right !important;
        direction: rtl !important;
    }

    /* 🎯 محاذاة السايدبار */
    [data-testid="stSidebar"] {
        direction: rtl;
        text-align: center !important;
    }

    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        padding: 10px !important;
    }

    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        text-align: center !important;
        width: 100% !important;
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] div[data-testid="stRadio"] {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
    }

    [data-testid="stSidebar"] div[data-testid="stRadio"] > div {
        display: flex !important;
        flex-direction: column !important;
        gap: 8px !important;
        width: 100% !important;
        align-items: center !important;
    }

    /* 🎨 تصميم أزرار القائمة الجانبية */
    [data-testid="stSidebar"] div[data-testid="stRadio"] label {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
        color: #ffffff !important;
        border: 2px solid #334155 !important;
        padding: 10px 12px !important;
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

    [data-testid="stSidebar"] div[data-testid="stRadio"] label p {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 14px !important;
        margin: 0 !important;
    }

    [data-testid="stSidebar"] div[data-testid="stRadio"] label[data-checked="true"] {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.5) !important;
    }

    /* 🎯 بطاقة الهيدر الملونة */
    .header-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #334155;
        border-radius: 20px;
        padding: 20px 15px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4), 0 0 15px rgba(56, 189, 248, 0.15);
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .header-logo {
        max-width: 160px;
        width: 100%;
        height: auto;
        margin-bottom: 12px;
        filter: drop-shadow(0px 4px 8px rgba(0, 0, 0, 0.5));
    }

    .main-title {
        color: #ffffff;
        font-size: 24px;
        font-weight: 800;
        margin-bottom: 6px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }

    .sub-title {
        color: #38bdf8;
        font-size: 18px;
        font-weight: 700;
    }

    .section-title-center {
        text-align: center !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        margin-top: 15px !important;
        margin-bottom: 15px !important;
    }

    /* 📊 كروت الإحصائيات (Metrics) */
    div[data-testid="stMetric"] {
        background-color: #1e293b !important;
        padding: 12px 8px !important;
        border-radius: 12px !important;
        border: 1px solid #334155 !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3) !important;
        margin-bottom: 8px !important;
    }

    div[data-testid="stMetricLabel"] label, div[data-testid="stMetricLabel"] p {
        color: #38bdf8 !important;
        font-weight: 800 !important;
        font-size: 14px !important;
    }

    div[data-testid="stMetricValue"] > div {
        width: 100% !important;
        text-align: center !important;
        color: #ffffff !important;
        font-size: 24px !important;
        font-weight: 900 !important;
    }

    /* 🎨 خريطة البرامج المخصصة (Custom Legend) */
    .custom-legend-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 8px;
        margin-top: 12px;
        direction: rtl;
    }

    .custom-legend-item {
        display: flex;
        align-items: center;
        gap: 6px;
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 6px 12px;
        border-radius: 16px;
        color: #ffffff;
        font-weight: 700;
        font-size: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    .legend-color-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        display: inline-block;
    }

    /* 💡 بطاقة الحقوق أسفل الصفحة */
    .page-footer-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #38bdf8;
        border-radius: 14px;
        padding: 12px 20px;
        text-align: center;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4);
        margin: 30px auto 15px auto;
        width: 90%;
        max-width: 400px;
    }

    .page-footer-card p {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 14px !important;
        line-height: 1.5 !important;
        margin: 0 !important;
    }

    /* 📱 تحسينات خاصة بالشاشات الصغيرة والموبايل */
    @media (max-width: 768px) {
        .header-card {
            padding: 15px 10px;
            border-radius: 15px;
        }

        .header-logo {
            max-width: 120px;
        }

        .main-title {
            font-size: 18px !important;
        }

        .sub-title {
            font-size: 14px !important;
        }

        .section-title-center {
            font-size: 16px !important;
        }

        .block-container {
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
            padding-top: 1rem !important;
        }
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
    search_query = st.text_input("🔍 بحث بالرقم القومي/كود المعلم:")

with col_date:
    selected_date = st.date_input("📅 تاريخ الاختبار:", value=None)

with col_reset:
    st.write("")
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

c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 1])

c1.metric("📊 إجمالي الممتحنين", total)
c2.metric("🎟️ حجز اختبار", reserved)
c3.metric("✅ ناجحين", passed)
c4.metric("❌ راسبين", failed)
c5.metric("⏳ قيد الاختبار", pending)

# 🍩 الرسم البياني الدائري التفاعلي
if "البرنامج" in df.columns and not df.empty:
    st.markdown(
        '<div class="section-title-center">🍩 توزيع الممتحنين حسب البرنامج</div>',
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
        .mark_arc(innerRadius=50, outerRadius=100)
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
        .properties(height=260)
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

desired_order_rtl = [
    "وقت أداء الاختبار",
    "الحالة",
    "البرنامج",
    "الرقم القومي",
    "اسم المعلم",
    "كود المعلم",
]

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

# 9. بطاقة الحقوق أسفل الصفحة
st.markdown(
    """
    <div class="page-footer-card">
        <p>✨ تصميم وتنفيذ: <b>أحمد الجنزوري - مدير الفرع</b></p>
    </div>
    """,
    unsafe_allow_html=True,
)

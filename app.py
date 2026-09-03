import base64
import glob
import io
import os
import altair as alt
import pandas as pd
import requests
import streamlit as st

# مكتبات ReportLab والخطوط
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

# مكتبات دعم إعادة تشكيل اللغة العربية والمحاذاة
import arabic_reshaper
from bidi.algorithm import get_display


# 🛠️ تحميل وتسجيل الخط العربي Amiri تلقائياً لحل مشكلة المربعات السوداء
def setup_arabic_font():
    font_path = "Amiri-Regular.ttf"
    if not os.path.exists(font_path):
        url = "https://github.com/google/fonts/raw/main/ofl/amiri/Amiri-Regular.ttf"
        response = requests.get(url)
        with open(font_path, "wb") as f:
            f.write(response.content)

    pdfmetrics.registerFont(TTFont("Amiri", font_path))


setup_arabic_font()


# 🛠️ دالة معالجة النص العربي للـ PDF
def process_arabic(text):
    if not text or str(text).strip() == "-" or str(text).strip() == "":
        return "-"
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)


# 1. إعدادات الصفحة
st.set_page_config(
    page_title="لوحة تحكم الامتحانات - فرع الجيزة",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 🎨 CSS لتنسيق الواجهة والبطاقات والسايدبار
st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl;
    }

    [data-testid="stDataFrame"] div[role="columnheader"], [data-testid="stDataFrame"] div[role="gridcell"] {
        text-align: right !important;
        direction: rtl !important;
    }

    [data-testid="stSidebar"] {
        direction: rtl;
        text-align: center !important;
    }

    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }

    [data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarContent"] {
        display: none !important;
    }

    [data-testid="stSidebar"] div[data-testid="stRadio"] label {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
        color: #ffffff !important;
        border: 2px solid #334155 !important;
        padding: 12px 15px !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        cursor: pointer !important;
        width: 100% !important;
        text-align: center !important;
    }

    [data-testid="stSidebar"] div[data-testid="stRadio"] label[data-checked="true"] {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.6) !important;
    }

    .header-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #334155;
        border-radius: 20px;
        padding: 30px 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
        margin-bottom: 25px;
    }

    .header-logo {
        width: 200px;
        height: auto;
        margin-bottom: 15px;
    }

    .main-title {
        color: #ffffff !important;
        font-size: 30px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .sub-title {
        color: #38bdf8 !important;
        font-size: 22px;
        font-weight: 700;
    }

    .section-title-center {
        text-align: center !important;
        font-size: 24px !important;
        font-weight: 800 !important;
        margin-top: 20px !important;
        margin-bottom: 15px !important;
    }

    .custom-metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 18px 10px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        margin-bottom: 10px;
    }

    .custom-metric-title {
        background-color: #facc15 !important;
        color: #0f172a !important;
        padding: 4px 14px !important;
        border-radius: 8px !important;
        font-size: 16px !important;
        font-weight: 900 !important;
        display: inline-block !important;
        margin-bottom: 8px !important;
    }

    .custom-metric-value {
        color: #ffffff !important;
        font-size: 32px !important;
        font-weight: 900 !important;
        margin: 0 !important;
    }

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
        color: #ffffff !important;
        font-weight: 700;
        font-size: 14px;
    }

    .legend-color-dot {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        display: inline-block;
    }

    .page-footer-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #38bdf8;
        border-radius: 16px;
        padding: 15px 25px;
        text-align: center;
        margin: 40px auto 20px auto;
        max-width: 450px;
    }

    .page-footer-card p {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        margin: 0 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)


def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        ext = path.split(".")[-1].lower()
        mime_type = "image/png" if ext == "png" else f"image/{ext}"
        return f"data:{mime_type};base64,{encoded_string}"
    return None


possible_files = [
    "logo.png",
    "logo.jpg",
    "logo.jpeg",
    "Logo.png",
    "Logo.jpg",
    "Logo.PNG",
]
found_logo = next((f for f in possible_files if os.path.exists(f)), None)
logo_b64 = get_image_base64(found_logo) if found_logo else ""

header_html = f"""
<div class="header-card">
    {"<img src='" + logo_b64 + "' class='header-logo' />" if logo_b64 else ""}
    <div class="main-title">🏛️ الأكاديمية المهنية للمعلمين - فرع الجيزة</div>
    <div class="sub-title">📝 لوحة تحكم وإحصائيات الامتحانات أونلاين</div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# 3. القائمة الجانبية
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


@st.cache_data
def load_data_from_project(file_path, mtime=None):
    try:
        df = pd.read_excel(file_path, dtype=str).fillna("-")
        df.columns = df.columns.str.strip()
        return df, None
    except Exception as e:
        return None, f"حدث خطأ أثناء قراءة الملف {file_path}: {e}"


excel_files = glob.glob("*.xlsx") + glob.glob("*.xls")
if not excel_files:
    st.error(
        "⚠️ لم يتم العثور على أي ملف إكسيل (.xlsx أو .xls) في مجلد المشروع."
    )
    st.stop()

file_path = excel_files[0]
file_mtime = os.path.getmtime(file_path)
df, err_msg = load_data_from_project(file_path, file_mtime)

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
        st.cache_data.clear()
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

# 7. حساب الإحصائيات
total = len(filtered_df)
if "الحالة" in filtered_df.columns:
    status_series = filtered_df["الحالة"].astype(str).str.strip()
    reserved = len(
        status_series[
            status_series.isin(
                ["محجوز", "حجز اختبار", "لم يختبر", "حجز", "لم يجتز"]
            )
        ]
    )
    passed = len(status_series[status_series.isin(["اجتاز", "ناجح", "ناجحين"])])
    failed = len(status_series[status_series.isin(["راسب", "راسبين"])])
    pending = len(
        status_series[status_series.isin(["قيد الاختبار", "جاري الاختبار"])]
    )
else:
    reserved = passed = failed = pending = 0


# 📄 دالة إنشاء تقرير PDF المحدثة مع الخط العربي والتوقيعات
def generate_pdf_report(data_df, program_filter):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30,
    )

    title_style = ParagraphStyle(
        name="ArabicTitle",
        fontName="Amiri",
        fontSize=18,
        leading=22,
        alignment=1,
        spaceAfter=12,
    )
    subtitle_style = ParagraphStyle(
        name="ArabicSubTitle",
        fontName="Amiri",
        fontSize=11,
        leading=15,
        alignment=1,
        spaceAfter=18,
    )
    heading_style = ParagraphStyle(
        name="ArabicHeading",
        fontName="Amiri",
        fontSize=14,
        leading=18,
        alignment=2,
        spaceAfter=10,
    )
    cell_style = ParagraphStyle(
        name="ArabicCell", fontName="Amiri", fontSize=10, leading=14, alignment=1
    )
    header_cell_style = ParagraphStyle(
        name="ArabicHeaderCell",
        fontName="Amiri",
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=colors.whitesmoke,
    )
    signature_style = ParagraphStyle(
        name="ArabicSignature",
        fontName="Amiri",
        fontSize=11,
        leading=16,
        alignment=1,
    )

    elements = []

    # 1. العنوان والترويسة
    elements.append(
        Paragraph(
            process_arabic(
                "تقرير إحصائيات الامتحانات - الأكاديمية المهنية للمعلمين فرع الجيزة"
            ),
            title_style,
        )
    )
    now_str = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
    prog_str = (
        f"البرنامج: {program_filter}"
        if program_filter != "الكل"
        else "جميع البرامج التدريبية"
    )
    elements.append(
        Paragraph(
            process_arabic(f"تاريخ استخراج التقرير: {now_str}  |  {prog_str}"),
            subtitle_style,
        )
    )
    elements.append(Spacer(1, 10))

    # 2. الإحصائيات العامة
    elements.append(
        Paragraph(process_arabic("1. الإحصائيات العامة:"), heading_style)
    )
    stats_headers = [
        "قيد الاختبار",
        "راسبين",
        "ناجحين",
        "حجز اختبار",
        "إجمالي الممتحنين",
    ]
    stats_data_row = [pending, failed, passed, reserved, total]

    table1_data = [
        [
            Paragraph(process_arabic(h), header_cell_style)
            for h in stats_headers
        ],
        [
            Paragraph(process_arabic(str(val)), cell_style)
            for val in stats_data_row
        ],
    ]

    t1 = Table(table1_data, colWidths=[100, 100, 100, 100, 120])
    t1.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
                ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#f8fafc")),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    elements.append(t1)
    elements.append(Spacer(1, 15))

    # 3. الإحصائيات حسب التواريخ
    if "وقت أداء الاختبار" in data_df.columns:
        elements.append(
            Paragraph(
                process_arabic("2. توزيع الإحصائيات حسب التواريخ:"),
                heading_style,
            )
        )

        temp_df = data_df.copy()
        temp_df["التاريخ"] = (
            temp_df["وقت أداء الاختبار"]
            .astype(str)
            .apply(lambda x: x.split(" ")[0] if " " in x else x)
        )

        date_group = (
            temp_df.groupby("التاريخ")
            .size()
            .reset_index(name="إجمالي الممتحنين")
        )

        date_table_headers = ["إجمالي الممتحنين", "التاريخ"]
        date_table_rows = [
            [
                Paragraph(process_arabic(h), header_cell_style)
                for h in date_table_headers
            ]
        ]

        for _, row in date_group.iterrows():
            date_table_rows.append(
                [
                    Paragraph(
                        process_arabic(str(row["إجمالي الممتحنين"])), cell_style
                    ),
                    Paragraph(process_arabic(str(row["التاريخ"])), cell_style),
                ]
            )

        t2 = Table(date_table_rows, colWidths=[250, 250])
        t2.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0284c7")),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f5f9")]),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        elements.append(t2)
        elements.append(Spacer(1, 15))

    # 4. الإحصائيات حسب البرامج
    if "البرنامج" in data_df.columns:
        elements.append(
            Paragraph(
                process_arabic("3. توزيع الممتحنين حسب البرنامج التدريبي:"),
                heading_style,
            )
        )

        prog_group = (
            data_df.groupby("البرنامج")
            .size()
            .reset_index(name="عدد الممتحنين")
        )

        prog_table_headers = ["عدد الممتحنين", "البرنامج التدريبي"]
        prog_table_rows = [
            [
                Paragraph(process_arabic(h), header_cell_style)
                for h in prog_table_headers
            ]
        ]

        for _, row in prog_group.iterrows():
            prog_table_rows.append(
                [
                    Paragraph(
                        process_arabic(str(row["عدد الممتحنين"])), cell_style
                    ),
                    Paragraph(process_arabic(str(row["البرنامج"])), cell_style),
                ]
            )

        t3 = Table(prog_table_rows, colWidths=[150, 350])
        t3.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#334155")),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        elements.append(t3)

    # ✍️ 5. تذييل التقرير والتوقيعات
    elements.append(Spacer(1, 35))

    signatures_data = [
        [
            Paragraph(
                process_arabic("<b>مدير الفرع</b><br/><br/>أحمد الجنزوري"),
                signature_style,
            ),
            Paragraph(
                process_arabic("<b>المختص</b><br/><br/>..........................."),
                signature_style,
            ),
        ]
    ]

    sig_table = Table(signatures_data, colWidths=[250, 250])
    sig_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    elements.append(sig_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer


# قسم الإحصائيات العامة مع زر تحميل PDF
col_title, col_pdf = st.columns([3, 1])
with col_title:
    st.markdown(
        '<div class="section-title-center">📊 الإحصائيات العامة</div>',
        unsafe_allow_html=True,
    )
with col_pdf:
    st.write(" ")
    pdf_bytes = generate_pdf_report(filtered_df, selected_program)
    st.download_button(
        label="📄 استخراج تقرير PDF",
        data=pdf_bytes,
        file_name=f"تقرير_الإحصائيات_{pd.Timestamp.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

metrics_data = [
    ("📊 إجمالي الممتحنين", total),
    ("🎟️ حجز اختبار", reserved),
    ("✅ ناجحين", passed),
    ("❌ راسبين", failed),
    ("⏳ قيد الاختبار", pending),
]

cols = st.columns(5)
for i, (title, val) in enumerate(metrics_data):
    with cols[i]:
        card_html = f"""
        <div class="custom-metric-card">
            <div class="custom-metric-title">{title}</div>
            <div class="custom-metric-value">{val}</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

# الرسم البياني
if "البرنامج" in df.columns and not df.empty:
    st.markdown(
        '<div class="section-title-center">🍩 توزيع الممتحنين حسب البرنامج التدريبي</div>',
        unsafe_allow_html=True,
    )
    prog_counts = df["البرنامج"].value_counts().reset_index()
    prog_counts.columns = ["البرنامج_التدريبي", "عدد_الممتحنين"]

    colors_list = [
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
                    range=colors_list[: len(prog_counts)],
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
        color = colors_list[idx % len(colors_list)]
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

# 8. جدول البيانات
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

# 9. التذييل
st.markdown(
    """
    <div class="page-footer-card">
        <p>✨ تصميم وتنفيذ: <b>أحمد الجنزوري - مدير الفرع</b></p>
    </div>
    """,
    unsafe_allow_html=True,
)

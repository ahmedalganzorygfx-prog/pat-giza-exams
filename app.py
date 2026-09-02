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

# 🎨 CSS فائق القوة لإجبار Streamlit على إظهار التبويبات كأزرار بارزة جداً
st.markdown(
    """
    <style>
    /* محاذاة الصفحة بالكامل RTL */
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl;
    }

    [data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
    }

    /* 🎯 توسيط العناوين الرئيسية */
    .section-title-center {
        text-align: center !important;
        font-size: 24px !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        margin-top: 20px !important;
        margin-bottom: 20px !important;
    }

    /* 🎯 الهيدر الرئيسي */
    .header-container {
        text-align: center;
        padding: 10px 0px 20px 0px;
    }
    .main-title {
        color: #ffffff;
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #38bdf8;
        font-size: 22px;
        font-weight: 700;
        margin-top: 0px;
    }

    /* 🌟🔥 جعل container التبويبات كشريط أزرار بارز بالكامل 🔥🌟 */
    [data-testid="stTabs"] {
        direction: rtl !important;
    }

    div[aria-label="Tabs"], div[role="tablist"], [data-baseweb="tab-list"] {
        display: flex !important;
        justify-content: center !important;
        gap: 12px !important;
        background-color: #0f172a !important;
        padding: 12px 18px !important;
        border-radius: 16px !important;
        border: 2px solid #334155 !important;
        margin-bottom: 25px !important;
    }

    /* 🔘 زر التبويب الافتراضي - بارز ومجسم */
    button[role="tab"], button[data-baseweb="tab"] {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
        color: #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        border: 1px solid #475569 !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.4) !important;
        transition: all 0.25s ease-in-out !important;
        margin: 0 4px !important;
        cursor: pointer !important;
    }

    /* 🖱️ عند تحريك الماوس فوق الزر */
    button[role="tab"]:hover, button[data-baseweb="tab"]:hover {
        background: #334155 !important;
        color: #ffffff !important;
        border-color: #38bdf8 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(56, 189, 248, 0.25) !important;
    }

    /* 🎯⚡ الزر المحدد/النشط (Selected Active Button) ⚡🎯 */
    button[role="tab"][aria-selected="true"], button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border: 2px solid #38bdf8 !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.7), 0 4px 10px rgba(0, 0, 0, 0.5) !important;
        transform: scale(1.03) !important;
    }

    /* إخفاء الخط الأفق السفي الافتراضي المموه لـ Streamlit */
    [data-baseweb="tab-highlight"], div[data-baseweb="tab-border"] {
        display: none !important;
        height: 0px !important;
    }

    /* 📊 كروت الإحصائيات */
    div[data-testid="stMetric"] {
        background-color: #1e293b !important;
        padding: 16px !important;
        border-radius: 12px !important;
        border: 1px solid #334155 !important;
        text-align: center !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3) !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        justify-content: center !important;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-size: 28px !important;
        font-weight: 800 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 2. الهيدر وشعار الفرع (في المنتصف)
logo_path = "logo.png"
if os.path.exists(logo_path):
    c_left, c_mid, c_right = st.columns([1, 4, 1])
    with c_mid:
        st.markdown(
            """
            <div class="header-container">
                <div class="main-title">🏛️ الأكاديمية المهنية للمعلمين - فرع الجيزة</div>
                <div class="sub-title">📝 لوحة تحكم وإحصائيات الامتحانات أونلاين</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c_right:
        st.image(logo_path, width=110)
else:
    st.markdown(
        """
        <div class="header-container">
            <div class="main-title">🏛️ الأكاديمية المهنية للمعلمين - فرع الجيزة</div>
            <div class="sub-title">📝 لوحة تحكم وإحصائيات الامتحانات أونلاين</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# 3. القائمة الجانبية (Sidebar)
st.sidebar.header("📁 إدارة البيانات")

uploaded_file = st.sidebar.file_uploader(
    "تحميل ملف الإكسيل (Excel)", type=["xlsx", "xls"]
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

# 6. البرامج التدريبية (عنوان موسط + أزرار تبويب بارزة جداً)
st.markdown(
    '<div class="section-title-center">🎯 البرامج التدريبية</div>',
    unsafe_allow_html=True,
)

program_options = [
    "الكل",
    "تطبيقات تربوية للمعلم المساعد",
    "مدير ووكيل ادارة مدرسية",
    "مدير ووكيل ادارة تعليمية",
    "أساسيات التوجيه الفني",
]

tabs = st.tabs(program_options)

for tab, program_name in zip(tabs, program_options):
    with tab:
        filtered_df = df.copy()

        if program_name != "الكل" and "البرنامج" in filtered_df.columns:
            filtered_df = filtered_df[
                filtered_df["البرنامج"] == program_name
            ]

        if selected_date and "وقت أداء الاختبار" in filtered_df.columns:
            date_str = str(selected_date)
            filtered_df = filtered_df[
                filtered_df["وقت أداء الاختبار"]
                .astype(str)
                .str.startswith(date_str)
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

        # 7. الإحصائيات العامة (عنوان موسط)
        st.markdown(
            '<div class="section-title-center">📊 الإحصائيات العامة</div>',
            unsafe_allow_html=True,
        )

        total = len(filtered_df)
        reserved = (
            len(
                filtered_df[
                    filtered_df["الحالة"].isin(
                        ["محجوز", "حجز اختبار", "لم يختبر"]
                    )
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

        # 8. جدول بيانات المعلمين (عنوان موسط)
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

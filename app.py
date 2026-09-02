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

# 🎨 تنسيق CSS لتصنيفات وتبويبات بارزة جداً (Pill-style Tabs)
st.markdown(
    """
    <style>
    /* محاذاة الصفحة بالكامل RTL */
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl;
        text-align: right;
    }
    
    [data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
    }

    /* 🌟 جعل حاوية التبويبات بارزة مع مسافات مريحة */
    div[data-baseweb="tab-list"] {
        direction: rtl !important;
        gap: 12px !important;
        background-color: #0f172a !important; /* خلفية داكنة للحاوية */
        padding: 10px !important;
        border-radius: 12px !important;
        border: 1px solid #1e293b !important;
    }

    /* 🏷️ تصميم التبويب كـ زر بارز (Button Style) */
    button[data-baseweb="tab"] {
        background-color: #1e293b !important;
        color: #94a3b8 !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-size: 15px !important;
        font-weight: bold !important;
        border: 1px solid #334155 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
    }

    /* 🖱️ تأثير عند إشارة الماوس (Hover) */
    button[data-baseweb="tab"]:hover {
        background-color: #334155 !important;
        color: #ffffff !important;
        border-color: #0284c7 !important;
    }

    /* 🎯 التبويب المختار (Active Tab) - لون أزرق بارز مع إضاءة */
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #0284c7 !important;
        color: #ffffff !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 0 12px rgba(2, 132, 199, 0.6) !important;
    }

    /* إخفاء الخط السفلي الافتراضي لـ Streamlit */
    div[data-baseweb="tab-highlight"] {
        display: none !important;
    }

    /* 📊 كروت الإحصائيات */
    div[data-testid="stMetric"] {
        background-color: #1e293b !important;
        padding: 15px !important;
        border-radius: 12px !important;
        border: 1px solid #334155 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3) !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-size: 26px !important;
        font-weight: bold !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 2. الهيدر وشعار الفرع
col_title, col_logo = st.columns([4, 1])

with col_logo:
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width=120)
    else:
        st.image(
            "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            width=100,
        )

with col_title:
    st.title("🏛️ الأكاديمية المهنية للمعلمين - فرع الجيزة")
    st.subheader("📝 لوحة تحكم وإحصائيات الامتحانات أونلاين")

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

# 6. البرامج التدريبية كـ تبويبات بارزة
st.write("### 🎯 البرامج التدريبية:")

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

        # 7. حساب الإحصائيات
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

        st.write("#### 📊 الإحصائيات العامة")
        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric("📊 إجمالي الممتحنين", total)
        c2.metric("🎟️ حجز اختبار", reserved)
        c3.metric("✅ ناجحين", passed)
        c4.metric("❌ راسبين", failed)
        c5.metric("⏳ قيد الاختبار", pending)

        st.divider()

        # 8. عرض جدول البيانات
        st.write("#### 📋 جدول بيانات المعلمين")

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

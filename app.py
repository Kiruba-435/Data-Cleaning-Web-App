
import streamlit as st
import pandas as pd
from modules.cleaning import clean_data
from modules.report import generate_report
from io import BytesIO

st.set_page_config("🧼 Smart Data Cleaning", layout="centered")

# --- Navbar ---
st.sidebar.title("🔗 Navigation")
nav = st.sidebar.radio("Go to", ["Home", "Data Cleaning", "About"], index=1)

if nav == "Home":
    st.title("🧼 Smart Data Cleaning App")
    st.markdown("Welcome! This app helps you clean your data easily. Use the sidebar to navigate.")

    # User testimonial at the top
    st.markdown("---")
    st.subheader("⭐ What Our Users Say")
    st.success("'This app saved me hours of manual work! The cleaning and reporting features are top-notch.' — Data Analyst")
    st.markdown("<span style='color: #ff4b4b; font-weight: bold;'>User feedback is crucial for us. It helps us improve and deliver the best experience!</span>", unsafe_allow_html=True)

    # Visible, relevant image
    st.image("https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=800&q=80", use_column_width=True)

    st.markdown("---")
    st.subheader("✨ Why Use This App?")
    st.markdown("""
    - **Instant Data Cleaning:** Clean your data in seconds with just a few clicks.
    - **Smart Outlier Detection:** Remove outliers using advanced IQR techniques.
    - **One-Click Encoding:** Effortlessly encode categorical columns for ML.
    - **Interactive Reports:** Get a summary of all cleaning steps performed.
    - **Download Ready:** Export your cleaned data instantly in CSV or Excel format.
    """)

    st.markdown("---")
    st.info("Try the Data Cleaning tab now and experience hassle-free preprocessing!")



elif nav == "Data Cleaning":
    st.title("🧹 Smart Data Cleaning App")
    st.markdown("Upload your dataset and apply the cleaning operations you choose — individually or combined.")

    uploaded_file = st.file_uploader("📂 Upload CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file:
        file_type = uploaded_file.name.split('.')[-1].lower()
        if file_type == "csv":
            df = pd.read_csv(uploaded_file)
        elif file_type == "xlsx":
            df = pd.read_excel(uploaded_file)
        else:
            st.error("❌ Unsupported file format.")
            st.stop()

        st.markdown("## 🔍 Raw Data Preview")
        st.dataframe(df.head(), use_container_width=True)

        st.markdown("## 🛠️ Cleaning Options")

        drop_columns = st.multiselect("✂️ Drop Columns (optional):", df.columns.tolist())
        do_cleaning = st.toggle("🧼 Handle Missing Values & Duplicates", value=True)
        do_encoding = st.toggle("🔠 Encode Categorical Columns", value=False)
        do_outliers = st.toggle("📏 Remove Outliers using IQR", value=False)

        iqr_multiplier = 1.5
        if do_outliers:
            iqr_multiplier = st.slider("IQR Sensitivity", 1.0, 3.0, 1.5, 0.1)

        if st.button("✨ Clean My Data"):
            cleaned_df, encoded_count, dupes, outliers = clean_data(
                df,
                drop_columns=drop_columns,
                do_cleaning=do_cleaning,
                do_outliers=do_outliers,
                do_encoding=do_encoding,
                iqr_multiplier=iqr_multiplier
            )

            report = generate_report(
                original_df=df,
                cleaned_df=cleaned_df,
                encoded_count=encoded_count,
                duplicates_removed=dupes,
                outliers_removed=outliers,
                dropped_columns=drop_columns
            )

            st.success("✅ Cleaning complete!")

            st.markdown("### 📊 Cleaned Data Preview")
            st.dataframe(cleaned_df.head(), use_container_width=True)

            with st.expander("📋 Full Cleaning Summary", expanded=True):
                for key, value in report.items():
                    st.write(f"**{key}:** {value}")

            # Dynamic file download
            if file_type == "csv":
                csv = cleaned_df.to_csv(index=False).encode("utf-8")
                name = uploaded_file.name.replace(".csv", "") + "_cleaned.csv"
                st.download_button("📥 Download CSV", csv, name, "text/csv")
            else:
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                    cleaned_df.to_excel(writer, index=False, sheet_name="Cleaned Data")
                name = uploaded_file.name.replace(".xlsx", "") + "_cleaned.xlsx"
                st.download_button("📥 Download Excel", buffer.getvalue(), name, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.info("👆 Upload a CSV or Excel file to begin.")

elif nav == "About":
    st.title("ℹ️ About This App")
    st.markdown("""
    **Smart Data Cleaning App** helps you quickly clean and preprocess your datasets for analysis and machine learning.
    - Drop columns
    - Handle missing values & duplicates
    - Encode categorical columns
    - Remove outliers

    **Extra Information:**
    - Built for data analysts, students, and ML engineers.
    - No coding required—just upload and clean!
    - Supports both CSV and Excel files.

    ---
    **Developed by [Kiruba](https://www.linkedin.com/in/kiruba-435/)**
    - Connect on LinkedIn: [linkedin.com/in/kiruba-435](https://www.linkedin.com/in/kiruba-435/)
    - For feedback or collaboration, reach out via LinkedIn or GitHub.

    Built with Streamlit.  
    [GitHub](https://github.com/Kiruba-435/Data-Cleaning-Web-App)
    """)

import streamlit as st
import pandas as pd
from modules.cleaning import clean_data
from modules.report import generate_report
from io import BytesIO

st.set_page_config("🧼 Smart Data Cleaning", layout="centered")

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

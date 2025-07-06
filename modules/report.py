def generate_report(original_df, cleaned_df, encoded_count, duplicates_removed, outliers_removed, dropped_columns):
    return {
        "Original Shape": original_df.shape,
        "Cleaned Shape": cleaned_df.shape,
        "Missing Values (Before)": original_df.isnull().sum().sum(),
        "Missing Values (After)": cleaned_df.isnull().sum().sum(),
        "Duplicates Removed": duplicates_removed,
        "Categorical Columns Encoded": encoded_count,
        "Outliers Removed (Approx)": outliers_removed,
        "Dropped Columns": dropped_columns or "None"
    }

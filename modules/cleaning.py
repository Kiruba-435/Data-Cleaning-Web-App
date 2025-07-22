import pandas as pd
from sklearn.preprocessing import LabelEncoder
from .outliers import remove_outliers_iqr

def clean_data(df, drop_columns=None, do_cleaning=True, do_outliers=True, do_encoding=True, iqr_multiplier=1.5):
    original_rows = df.shape[0]

    if drop_columns:
        df = df.drop(columns=[col for col in drop_columns if col in df.columns])

    if do_cleaning:
        num_cols = df.select_dtypes(include='number').columns
        df[num_cols] = df[num_cols].fillna(df[num_cols].median())

        cat_cols = df.select_dtypes(include='object').columns
        df[cat_cols] = df[cat_cols].fillna(df[cat_cols].mode().iloc[0])

        duplicates_removed = df.duplicated().sum()
        df = df.drop_duplicates()
    else:
        cat_cols = df.select_dtypes(include='object').columns
        duplicates_removed = 0

    if do_outliers:
        before_rows = df.shape[0]
        df = remove_outliers_iqr(df, multiplier=iqr_multiplier)
        outliers_removed = before_rows - df.shape[0]
    else:
        outliers_removed = 0

    if do_encoding:
        le = LabelEncoder()
        for col in cat_cols:
            df[col] = le.fit_transform(df[col])
        encoded_count = len(cat_cols)
    else:
        encoded_count = 0

    

    return df, encoded_count, duplicates_removed, outliers_removed

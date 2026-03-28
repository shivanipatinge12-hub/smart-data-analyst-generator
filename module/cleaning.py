import pandas as pd
def clean_data(df):
    report = {}
    before = df.shape[0]
    df = df.drop_duplicates()
    after = df.shape[0]
    report["duplicates_removed"] = before - after
    missing_before = df.isnull().sum().sum()
    fill_details = {}
    for col in df.columns:
        if df[col].dtype == "object":
            mode_series = df[col].mode()
            if not mode_series.empty:
                mode_val = mode_series[0]
                df[col] = df[col].fillna(mode_val)
                fill_details[col] = f"Filled with mode ({mode_val})"
            else:
                fill_details[col] = "No mode found"
            df[col] = df[col].astype(str).str.lower().str.strip()
        else:
            mean_val = df[col].mean()
            if pd.notnull(mean_val):
                df[col] = df[col].fillna(mean_val)
                fill_details[col] = f"Filled with mean ({round(mean_val, 2)})"
            else:
                fill_details[col] = "No mean available"
    missing_after = df.isnull().sum().sum()
    report["missing_before"] = int(missing_before)
    report["missing_after"] = int(missing_after)
    report["fill_details"] = fill_details
    outlier_info = {}
    for col in df.select_dtypes(include=['int64', 'float64']).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        before_count = df.shape[0]
        df = df[(df[col] >= lower) & (df[col] <= upper)]
        after_count = df.shape[0]
        outlier_info[col] = before_count - after_count
    report["outliers_removed"] = outlier_info
    df = df.reset_index(drop=True)
    df = df.dropna(axis=1, how='all')
    for col in df.columns:
        if df[col].dtype == "object":
            try:
                df[col] = pd.to_numeric(df[col])
            except:
                pass
    summary = {}
    for col in df.columns:
        summary[col] = {
            "dtype": str(df[col].dtype),
            "missing": int(df[col].isnull().sum()),
            "unique": int(df[col].nunique())
        }
        if df[col].dtype in ['int64', 'float64']:
            summary[col]["mean"] = float(df[col].mean())
            summary[col]["min"] = float(df[col].min())
            summary[col]["max"] = float(df[col].max())
    report["column_summary"] = summary
    return df, report
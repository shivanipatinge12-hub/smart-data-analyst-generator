import pandas as pd
def load_data(file):
    try:
        df = pd.read_csv(file, sep=None, engine='python')
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        print("Error loading file:", e)
        return None
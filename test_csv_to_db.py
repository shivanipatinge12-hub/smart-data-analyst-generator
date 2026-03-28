import pandas as pd
from db import get_connection
try:
    file_path = "data.csv"
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.replace('[^A-Za-z0-9_]', '_', regex=True)
    conn = get_connection()
    cursor = conn.cursor()
    table_name = "dataset"
    cursor.execute(f"""
    IF OBJECT_ID('{table_name}', 'U') IS NOT NULL
    DROP TABLE {table_name};
    """)
    columns = df.columns
    column_defs = []
    for col in columns:
        if df[col].dtype == 'int64':
            column_defs.append(f"[{col}] INT")
        elif df[col].dtype == 'float64':
            column_defs.append(f"[{col}] FLOAT")
        else:
            column_defs.append(f"[{col}] VARCHAR(MAX)")
    create_query = f"""
    CREATE TABLE {table_name} (
        id INT IDENTITY(1,1) PRIMARY KEY,
        {', '.join(column_defs)}
    )
    """
    cursor.execute(create_query)
    conn.commit()
    col_names = ','.join([f"[{col}]" for col in columns])
    placeholders = ','.join(['?' for _ in columns])
    insert_query = f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})"
    data = [tuple(row) for _, row in df.iterrows()]
    cursor.executemany(insert_query, data)
    conn.commit()
    conn.close()
    print("CSV uploaded successfully into SQL Server")
except Exception as e:
    print("Error:", e)
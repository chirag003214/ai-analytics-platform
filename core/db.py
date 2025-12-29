import sqlite3
import os

DB_PATH = "analytics.db"

def write_table(df, table_name: str):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )
    conn.close()



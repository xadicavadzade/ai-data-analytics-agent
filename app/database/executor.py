import sqlite3
import pandas as pd


class SQLExecutor:

    def execute(self, database_path: str, sql: str):

        conn = sqlite3.connect(database_path)

        try:
            df = pd.read_sql_query(sql, conn)
            return df

        finally:
            conn.close()
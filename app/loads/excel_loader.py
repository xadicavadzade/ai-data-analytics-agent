import os
import re
import uuid
import sqlite3

import pandas as pd
from fastapi import UploadFile

from app.loads.base_load import BaseLoader


class ExcelLoader(BaseLoader):

    async def load(self, file: UploadFile) -> str:

        os.makedirs("uploads", exist_ok=True)

        db_name = f"{uuid.uuid4().hex}.db"
        database_path = os.path.join("uploads", db_name)

        excel = pd.ExcelFile(file.file)

        conn = sqlite3.connect(database_path)

        try:
            for sheet in excel.sheet_names:

                df = excel.parse(sheet)

                if df.empty or len(df.columns) == 0:
                    continue

                table_name = re.sub(r"\W+", "_", sheet)

                df.to_sql(
                    table_name,
                    conn,
                    index=False,
                    if_exists="replace",
                )

        finally:
            conn.close()

        return database_path
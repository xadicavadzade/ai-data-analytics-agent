import os
import uuid
import sqlite3

import pandas as pd
from fastapi import UploadFile

from app.loaders.base import BaseLoader


class ExcelLoader(BaseLoader):

    async def load(self, file: UploadFile) -> str:

        os.makedirs("uploads", exist_ok=True)

        db_name = f"{uuid.uuid4().hex}.db"

        database_path = os.path.join("uploads", db_name)

        excel = pd.ExcelFile(file.file)

        conn = sqlite3.connect(database_path)

        for sheet in excel.sheet_names:

            df = excel.parse(sheet)

            df.to_sql(
                sheet,
                conn,
                index=False,
                if_exists="replace",
            )

        conn.close()

        return database_path
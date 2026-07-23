import os
import uuid
import sqlite3

import pandas as pd
from fastapi import UploadFile

from app.loaders.base import BaseLoader


class CSVLoader(BaseLoader):

    async def load(self, file: UploadFile) -> str:

        os.makedirs("uploads", exist_ok=True)

        table_name = os.path.splitext(file.filename)[0]

        db_name = f"{uuid.uuid4().hex}.db"

        database_path = os.path.join("uploads", db_name)

        df = pd.read_csv(file.file)

        conn = sqlite3.connect(database_path)

        df.to_sql(
            table_name,
            conn,
            index=False,
            if_exists="replace",
        )

        conn.close()

        return database_path
import os
import uuid

from fastapi import UploadFile

from app.loads.base_load import BaseLoader


class SQLiteLoader(BaseLoader):

    async def load(self, file: UploadFile) -> str:
        """
        Saves uploaded SQLite database and returns its path.
        """

        os.makedirs("uploads", exist_ok=True)

        extension = os.path.splitext(file.filename)[1].lower()

        filename = f"{uuid.uuid4().hex}{extension}"

        database_path = os.path.join("uploads", filename)

        contents = await file.read()

        with open(database_path, "wb") as db_file:
            db_file.write(contents)

        return database_path
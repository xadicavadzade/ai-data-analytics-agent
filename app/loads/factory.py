from fastapi import HTTPException

from app.loads.csv_loader import CSVLoader
from app.loads.excel_loader import ExcelLoader
from app.loads.sqlite_loader import SQLiteLoader


class LoaderFactory:

    @staticmethod
    def get_loader(filename: str):

        ext = filename.split(".")[-1].lower()

        if ext in ["db", "sqlite", "sqlite3"]:
            return SQLiteLoader()

        if ext == "csv":
            return CSVLoader()

        if ext in ["xlsx", "xls"]:
            return ExcelLoader()

        raise HTTPException(
            status_code=400,
            detail="Unsupported file type.",
        )
import aiosqlite

class SQLiteConnection:

    async def connect(self, database_path: str):
        return await aiosqlite.connect(database_path)
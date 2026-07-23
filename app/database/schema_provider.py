from app.database.connection import SQLiteConnection
class SchemaProvider:

    def __init__(self,connection : SQLiteConnection):
        self.connection = connection
    async def get_schema(self,database_path:str) -> str:
        conn = await self.connection.connect(database_path)
       
        
        try :
            cursor = await conn.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table';
            """)

            tables = await cursor.fetchall()

            schema = []

            for table in tables:
                table_name = table[0] #table is tuple

                schema.append(f"Table: {table_name}")

                cursor = await conn.execute(f"PRAGMA table_info({table_name})")
                columns = await cursor.fetchall()
                
                for column in columns:
                    schema.append(f"- {column[1]} {column[2]}")

        finally:
            await conn.close()

        return "\n".join(schema)




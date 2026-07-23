from app.database.connection import SQLiteConnection


class SchemaProvider:

    def __init__(self, connection: SQLiteConnection):
        self.connection = connection

    async def get_schema(self, database_path: str) -> str:
        conn = await self.connection.connect(database_path)

        try:
            cursor = await conn.execute("""
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                AND name NOT LIKE 'sqlite_%';
            """)

            tables = await cursor.fetchall()

            schema = []

            for table in tables:
                table_name = table[0]

                schema.append(f"Table: {table_name}")

                cursor = await conn.execute(
                    f'PRAGMA table_info("{table_name}")'
                )

                columns = await cursor.fetchall()

                for column in columns:
                    column_name = column[1]
                    column_type = column[2]

                    schema.append(
                        f"- {column_name}: {column_type}"
                    )

            return "\n".join(schema)

        finally:
            await conn.close()
import re


class SQLValidator:

    FORBIDDEN_KEYWORDS = {
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "REPLACE",
        "ATTACH",
        "DETACH",
        "PRAGMA",
    }

    @staticmethod
    def validate_sql(sql: str) -> None:

        if not sql or not sql.strip():
            raise ValueError("Generated SQL is empty.")

        sql = sql.strip()

        if sql == "CANNOT_GENERATE_SQL":
            raise ValueError(
                "Cannot generate SQL for this question."
            )

        sql_upper = sql.upper()

        if not (
            sql_upper.startswith("SELECT")
            or sql_upper.startswith("WITH")
        ):
            raise ValueError(
                "Only SELECT and WITH statements are allowed."
            )

        for keyword in SQLValidator.FORBIDDEN_KEYWORDS:

            pattern = rf"\b{keyword}\b"

            if re.search(pattern, sql_upper):
                raise ValueError(
                    f"Forbidden SQL keyword detected: {keyword}"
                )
import pandas as pd
import pytest

from unittest.mock import MagicMock, AsyncMock

from app.models.state import AgentState
from app.tools.sql_tool import SQLTool


@pytest.mark.asyncio
async def test_sql_tool_run():

    executor = MagicMock()
    llm = AsyncMock()
    schema_provider = AsyncMock()
    memory = MagicMock()

    schema_provider.get_schema.return_value = "CREATE TABLE employees(id INT, name TEXT);"

    llm.generate.return_value = "SELECT * FROM employees"

    executor.execute.return_value = pd.DataFrame(
        {
            "id": [1, 2],
            "name": ["Ali", "Veli"],
        }
    )

    tool = SQLTool(
        executor=executor,
        llm=llm,
        schema_provider=schema_provider,
        conversation_memory=memory,
    )

    state = AgentState(
        question="Show all employees",
        database_path="dummy.db",
    )

    result = await tool.run(state)

    assert result.generated_sql == "SELECT * FROM employees"

    assert result.df is not None

    assert len(result.df) == 2

    schema_provider.get_schema.assert_called_once_with("dummy.db")

    llm.generate.assert_called_once()

    executor.execute.assert_called_once_with(
        "dummy.db",
        "SELECT * FROM employees",
    )

    memory.add.assert_called_once_with(
        "Show all employees"
    )
import pandas as pd
import pytest

from app.models.state import AgentState
from app.tools.pandas_tool import PandasTool


@pytest.mark.asyncio
async def test_run_returns_analysis():

    tool = PandasTool()

    state = AgentState(
        question="Analyze dataframe",
        df=pd.DataFrame(
            {
                "name": ["Ali", "Veli", "Ali"],
                "age": [20, 25, 20],
                "salary": [1000, 2000, 1000],
            }
        ),
    )

    result = await tool.run(state)

    assert result.df_analysis is not None


@pytest.mark.asyncio
async def test_shape():

    tool = PandasTool()

    state = AgentState(
        question="Analyze dataframe",
        df=pd.DataFrame(
            {
                "name": ["Ali", "Veli", "Ali"],
                "age": [20, 25, 20],
                "salary": [1000, 2000, 1000],
            }
        ),
    )

    result = await tool.run(state)

    assert result.df_analysis["shape"]["rows"] == 3
    assert result.df_analysis["shape"]["columns"] == 3


@pytest.mark.asyncio
async def test_column_analysis():

    tool = PandasTool()

    state = AgentState(
        question="Analyze dataframe",
        df=pd.DataFrame(
            {
                "name": ["Ali", "Veli", "Ali"],
                "age": [20, 25, 20],
                "salary": [1000, 2000, 1000],
            }
        ),
    )

    result = await tool.run(state)

    assert result.df_analysis["numeric_columns"] == [
        "age",
        "salary",
    ]

    assert result.df_analysis["categorical_columns"] == [
        "name",
    ]


@pytest.mark.asyncio
async def test_duplicate_count():

    tool = PandasTool()

    state = AgentState(
        question="Analyze dataframe",
        df=pd.DataFrame(
            {
                "name": ["Ali", "Veli", "Ali"],
                "age": [20, 25, 20],
                "salary": [1000, 2000, 1000],
            }
        ),
    )

    result = await tool.run(state)

    assert result.df_analysis["duplicates"] == 1


@pytest.mark.asyncio
async def test_empty_dataframe():

    tool = PandasTool()

    state = AgentState(
        question="Analyze dataframe",
        df=pd.DataFrame(),
    )

    with pytest.raises(ValueError):
        await tool.run(state)


@pytest.mark.asyncio
async def test_none_dataframe():

    tool = PandasTool()

    state = AgentState(
        question="Analyze dataframe",
        df=None,
    )

    with pytest.raises(ValueError):
        await tool.run(state)
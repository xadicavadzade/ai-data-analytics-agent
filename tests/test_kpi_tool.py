import pandas as pd
import pytest

from app.models.state import AgentState
from app.tools.kpi_tool import KPITool


@pytest.mark.asyncio
async def test_run_returns_kpis():

    tool = KPITool()

    state = AgentState(
        question="Generate KPIs",
        df=pd.DataFrame(
            {
                "name": ["Ali", "Veli", "Ali"],
                "age": [20, 25, 20],
                "salary": [1000, 2000, 1000],
            }
        ),
    )

    result = await tool.run(state)

    assert result.kpis is not None


@pytest.mark.asyncio
async def test_basic_kpis():

    tool = KPITool()

    state = AgentState(
        question="Generate KPIs",
        df=pd.DataFrame(
            {
                "name": ["Ali", "Veli", "Ali"],
                "age": [20, 25, 20],
                "salary": [1000, 2000, 1000],
            }
        ),
    )

    result = await tool.run(state)

    assert result.kpis["row_count"] == 3
    assert result.kpis["column_count"] == 3
    assert result.kpis["duplicate_rows"] == 1
    assert result.kpis["missing_values"] == 0


@pytest.mark.asyncio
async def test_numeric_summary():

    tool = KPITool()

    state = AgentState(
        question="Generate KPIs",
        df=pd.DataFrame(
            {
                "name": ["Ali", "Veli", "Ali"],
                "age": [20, 25, 20],
                "salary": [1000, 2000, 1000],
            }
        ),
    )

    result = await tool.run(state)

    summary = result.kpis["numeric_summary"]

    assert summary["age"]["sum"] == 65
    assert summary["age"]["mean"] == 65 / 3
    assert summary["age"]["min"] == 20
    assert summary["age"]["max"] == 25

    assert summary["salary"]["sum"] == 4000
    assert summary["salary"]["mean"] == 4000 / 3
    assert summary["salary"]["min"] == 1000
    assert summary["salary"]["max"] == 2000


@pytest.mark.asyncio
async def test_top_categories():

    tool = KPITool()

    state = AgentState(
        question="Generate KPIs",
        df=pd.DataFrame(
            {
                "name": ["Ali", "Veli", "Ali"],
                "age": [20, 25, 20],
                "salary": [1000, 2000, 1000],
            }
        ),
    )

    result = await tool.run(state)

    top = result.kpis["top_categories"]

    assert top["name"]["value"] == "Ali"
    assert top["name"]["count"] == 2


@pytest.mark.asyncio
async def test_unique_counts():

    tool = KPITool()

    state = AgentState(
        question="Generate KPIs",
        df=pd.DataFrame(
            {
                "name": ["Ali", "Veli", "Ali"],
                "age": [20, 25, 20],
                "salary": [1000, 2000, 1000],
            }
        ),
    )

    result = await tool.run(state)

    unique = result.kpis["unique_counts"]

    assert unique["name"] == 2
    assert unique["age"] == 2
    assert unique["salary"] == 2


@pytest.mark.asyncio
async def test_empty_dataframe():

    tool = KPITool()

    state = AgentState(
        question="Generate KPIs",
        df=pd.DataFrame(),
    )

    with pytest.raises(ValueError):
        await tool.run(state)


@pytest.mark.asyncio
async def test_none_dataframe():

    tool = KPITool()

    state = AgentState(
        question="Generate KPIs",
        df=None,
    )

    with pytest.raises(ValueError):
        await tool.run(state)
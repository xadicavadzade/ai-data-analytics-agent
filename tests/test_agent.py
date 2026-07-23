import pytest

from unittest.mock import AsyncMock, MagicMock

from app.agent.analytics_agent import AnalyticsAgent
from app.models.state import AgentState


@pytest.mark.asyncio
async def test_agent_run_without_chart():

    planner = AsyncMock()
    sql_tool = AsyncMock()
    pandas_tool = AsyncMock()
    chart_tool = AsyncMock()
    insight_tool = AsyncMock()
    kpi_tool = AsyncMock()

    plan = MagicMock()
    plan.steps = []

    planner.create_plan.return_value = plan

    state = AgentState(
        question="Show all employees"
    )

    sql_tool.run.return_value = state
    pandas_tool.run.return_value = state
    kpi_tool.run.return_value = state
    insight_tool.run.return_value = state

    agent = AnalyticsAgent(
        planner=planner,
        sql_tool=sql_tool,
        pandas_tool=pandas_tool,
        chart_tool=chart_tool,
        insight_tool=insight_tool,
        kpi_tool=kpi_tool,
    )

    result = await agent.run(state)

    assert result == state

    planner.create_plan.assert_called_once_with(
        question="Show all employees"
    )

    sql_tool.run.assert_called_once_with(state)
    pandas_tool.run.assert_called_once_with(state)
    kpi_tool.run.assert_called_once_with(state)
    insight_tool.run.assert_called_once_with(state)

    chart_tool.run.assert_not_called()


@pytest.mark.asyncio
async def test_agent_run_with_chart():

    planner = AsyncMock()
    sql_tool = AsyncMock()
    pandas_tool = AsyncMock()
    chart_tool = AsyncMock()
    insight_tool = AsyncMock()
    kpi_tool = AsyncMock()

    plan = MagicMock()
    plan.steps = ["chart"]

    planner.create_plan.return_value = plan

    state = AgentState(
        question="Show employee chart"
    )

    sql_tool.run.return_value = state
    pandas_tool.run.return_value = state
    kpi_tool.run.return_value = state
    chart_tool.run.return_value = state
    insight_tool.run.return_value = state

    agent = AnalyticsAgent(
        planner=planner,
        sql_tool=sql_tool,
        pandas_tool=pandas_tool,
        chart_tool=chart_tool,
        insight_tool=insight_tool,
        kpi_tool=kpi_tool,
    )

    result = await agent.run(state)

    assert result == state

    planner.create_plan.assert_called_once_with(
        question="Show employee chart"
    )

    sql_tool.run.assert_called_once_with(state)
    pandas_tool.run.assert_called_once_with(state)
    kpi_tool.run.assert_called_once_with(state)
    chart_tool.run.assert_called_once_with(state)
    insight_tool.run.assert_called_once_with(state)


@pytest.mark.asyncio
async def test_agent_raises_exception():

    planner = AsyncMock()
    sql_tool = AsyncMock()
    pandas_tool = AsyncMock()
    chart_tool = AsyncMock()
    insight_tool = AsyncMock()
    kpi_tool = AsyncMock()

    planner.create_plan.side_effect = Exception("Planner failed")

    state = AgentState(
        question="Show employees"
    )

    agent = AnalyticsAgent(
        planner=planner,
        sql_tool=sql_tool,
        pandas_tool=pandas_tool,
        chart_tool=chart_tool,
        insight_tool=insight_tool,
        kpi_tool=kpi_tool,
    )

    with pytest.raises(Exception, match="Planner failed"):
        await agent.run(state)
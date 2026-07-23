import pytest
from unittest.mock import AsyncMock, patch

from app.models.state import AgentState
from app.models.insight import AnalystInsight
from app.tools.insight_tool import InsightTool


@pytest.mark.asyncio
@patch("app.tools.insight_tool.build_insight_prompt")
async def test_run_returns_insight(mock_prompt):

    mock_prompt.return_value = "fake prompt"

    llm = AsyncMock()

    llm.generate.return_value = """
    {
        "summary": "Average salary is increasing.",
        "key_findings": [
            "Engineering has the highest salaries",
            "Average salary increased by 12%",
            "Senior roles earn significantly more"
        ],
        "breakdown": "Engineering employees have the highest average salary.",
        "recommendation": "Review compensation strategy for other departments.",
        "caveat": "Analysis is based only on the selected dataset."
    }
    """

    tool = InsightTool(llm)

    state = AgentState(
        question="Analyze salaries",
        generated_sql="SELECT * FROM employees",
        df_analysis={},
        kpis={},
    )

    result = await tool.run(state)

    assert isinstance(result.insight, AnalystInsight)

    assert result.insight.summary == "Average salary is increasing."

    assert result.insight.recommendation == (
        "Review compensation strategy for other departments."
    )

    mock_prompt.assert_called_once_with(
        state.question,
        state.generated_sql,
        state.df_analysis,
        state.kpis,
    )

    llm.generate.assert_called_once_with("fake prompt")
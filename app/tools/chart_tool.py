import os
import uuid
import matplotlib.pyplot as plt

from app.tools.base_tool import BaseTool
from app.models.state import AgentState
from app.llm.clients import LLMClient
from app.config.prompts import build_chart_prompt
from app.models.chart_spec import ChartPlan, ChartSpec
from app.config.logger import setup_logger

logger = setup_logger(__name__)


class ChartTool(BaseTool):
    def __init__(self, llm: LLMClient):
        self.llm = llm

    async def _deciding_chart(self, state: AgentState):
        columns = state.df.columns.tolist()

        prompt = build_chart_prompt(
            state.question,
            columns,
            state.df_analysis,
        )

        response = await self.llm.generate(prompt)

        return ChartPlan.model_validate_json(response)

    def _plot_chart(self, df, chart_spec: ChartSpec, path: str):

        plt.figure(figsize=(8, 5))

        if chart_spec.chart_type == "bar":
            df.plot(
                kind="bar",
                x=chart_spec.x,
                y=chart_spec.y,
            )

        elif chart_spec.chart_type == "line":
            df.plot(
                kind="line",
                x=chart_spec.x,
                y=chart_spec.y,
            )

        elif chart_spec.chart_type == "scatter":
            df.plot(
                kind="scatter",
                x=chart_spec.x,
                y=chart_spec.y,
            )

        elif chart_spec.chart_type == "pie":
            df.set_index(chart_spec.x)[chart_spec.y].plot(
                kind="pie",
                autopct="%1.1f%%",
            )

        elif chart_spec.chart_type == "histogram":
            df[chart_spec.x].plot(
                kind="hist",
                bins=10,
            )

        else:
            raise ValueError(
                f"Unsupported chart type: {chart_spec.chart_type}"
            )

        if chart_spec.title:
            plt.title(chart_spec.title)

        plt.tight_layout()
        plt.savefig(path)
        plt.close()

    async def run(self, state: AgentState) -> AgentState:

        if state.df is None:
            raise ValueError("No dataframe found.")

        # Charts qovluğunu yarat
        os.makedirs("charts", exist_ok=True)

        plan = await self._deciding_chart(state)

        state.chart = plan

        chart_paths = []

        for spec in plan.charts:

            logger.info(f"Creating chart: {spec.chart_type}")

            # Unikal fayl adı
            path = f"charts/{uuid.uuid4().hex}.png"

            self._plot_chart(
                state.df,
                spec,
                path,
            )

            logger.info(f"Saving chart to {path}")

            chart_paths.append(path)

        state.chart_paths = chart_paths

        return state
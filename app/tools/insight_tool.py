from app.tools.base_tool import BaseTool
from app.models.state import AgentState
from app.llm.clients import LLMClient

from app.models.insight_response import AnalystInsight

from app.config.prompts import build_insight_prompt




class InsightTool(BaseTool):

    def __init__(self, llm:LLMClient):
        self.llm = llm

    async def _generate_insights(self, state: AgentState) -> str:
        prompt = build_insight_prompt(state.question,state.generated_sql,state.df_analysis,state.kpis)

        response = await self.llm.generate(prompt)

        return AnalystInsight.model_validate_json(response)

    async def run(self, state: AgentState) -> AgentState:

        insights = await self._generate_insights(state)



        state.insight  = insights

        return state
    



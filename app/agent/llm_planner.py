from app.config.prompts import build_planner_prompt
from app.llm.clients import LLMClient
from app.agent.base_planner import BasePlanner
from app.models.state import AgentState
from app.models.execution_plan import ExecutionPlan
from app.config.logger import setup_logger

logger = setup_logger(__name__)


class LLMPlanner(BasePlanner):

    def __init__(self, llm:LLMClient):
        self.llm = llm

    async def create_plan(self, question:str):

        try:

            prompt = build_planner_prompt(question)

            response = await self.llm.generate(prompt)

            plan = ExecutionPlan.model_validate_json(response)

            return plan
        

        except Exception as e:
            
            logger.exception(f"Planner failed: {e}")
            raise      
                



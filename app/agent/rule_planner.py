from app.agent.base_planner import BasePlanner
from app.models.execution_plan import ExecutionPlan
from app.models.state import AgentState


class RulePlanner(BasePlanner):

    async def create_plan(self, question:str) -> ExecutionPlan:

        question = question.lower()

        if "plot" in question:
            plan = ["sql", "chart"]

        elif "summarize" in question:
            plan = ["sql", "insight"]

        else:
            plan = ["sql"]

        return ExecutionPlan(steps=plan)
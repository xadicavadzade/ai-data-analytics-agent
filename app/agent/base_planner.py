from app.models.state import AgentState
from app.models.execution_plan import ExecutionPlan
from abc import ABC, abstractmethod


class BasePlanner(ABC):


    @abstractmethod
    async def create_plan(self, question:str) -> ExecutionPlan:
        ...
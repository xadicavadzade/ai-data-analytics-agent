from pydantic import BaseModel

class ExecutionPlan(BaseModel):
    steps: list[str]
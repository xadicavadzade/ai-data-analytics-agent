from pydantic import BaseModel


class ChartSpec(BaseModel):
    chart_type: str
    x: str
    y: str
    title: str | None = None

class ChartPlan(BaseModel):
    charts: list[ChartSpec]
from typing import Any

from pydantic import BaseModel

from app.models.chart_spec import ChartPlan

from app.models.insight_response import AnalystInsight

class QueryResponse(BaseModel):
    answer: AnalystInsight | None = None
    sql: str | None = None
    data: list[dict[str, Any]] | None = None
    kpis: dict[str,Any]
    chart: ChartPlan | None = None
    chart_paths: list[str] = []
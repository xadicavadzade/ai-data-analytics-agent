from dataclasses import dataclass,field
from typing import Any
import pandas as pd
from app.models.chart_spec import ChartPlan


@dataclass
class AgentState:

    question : str

    generated_sql : str | None = None

    df : pd.DataFrame = field(default_factory=pd.DataFrame)

    df_analysis : dict[str,Any] = field(default_factory=dict)

    insight  : str | None = None

    chart: ChartPlan | None = None

    chart_paths: list[str] = field(default_factory=list)

    execution_plan : list[str] | None = None

    database_path: str | None = None

    schema: str | None = None

    kpis: dict[str, Any] = field(default_factory=dict)






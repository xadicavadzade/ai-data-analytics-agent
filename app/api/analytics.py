from fastapi import APIRouter, Depends

from app.agent.analytics_agent import AnalyticsAgent
from app.api.dependencies import get_agent
from app.models.state import AgentState
from app.schemas.query import QueryRequest
from app.schemas.response import QueryResponse

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.post("/query", response_model=QueryResponse)
async def query(
    request: QueryRequest,
    agent: AnalyticsAgent = Depends(get_agent),
):
    state = AgentState(question=request.question,database_path=request.database_path)

    result = await agent.run(state)

  
    return QueryResponse(
        
        answer=result.insight,
        sql=result.generated_sql,
        data=result.df.head(100).to_dict(orient="records"),
        chart=result.chart,
        chart_paths=result.chart_paths,
        kpis=result.kpis
    )
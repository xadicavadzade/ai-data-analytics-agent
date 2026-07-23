from fastapi import APIRouter, Depends, UploadFile, File, Form

from app.agent.analytics_agent import AnalyticsAgent
from app.api.dependencies import get_agent
from app.loaders.factory import LoaderFactory
from app.models.state import AgentState
from app.schemas.response import QueryResponse

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.post("/query", response_model=QueryResponse)
async def query(
    question: str = Form(...),
    file: UploadFile = File(...),
    agent: AnalyticsAgent = Depends(get_agent),
):
    loader = LoaderFactory.get_loader(file.filename)

    database_path = await loader.load(file)

    state = AgentState(
        question=question,
        database_path=database_path,
    )

    result = await agent.run(state)

    return QueryResponse(
        answer=result.insight,
        sql=result.generated_sql,
        data=result.df.head(100).to_dict(orient="records"),
        chart=result.chart,
        chart_paths=result.chart_paths,
        kpis=result.kpis,
    )
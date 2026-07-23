from fastapi import APIRouter,Depends
from app.agent.analytics_agent import AnalyticsAgent
from app.api.dependencies import get_agent

router = APIRouter(prefix='/clear',tags=['Clear Interface'])


@router.post('')
async def clear_session(
    agent: AnalyticsAgent = Depends(get_agent)
):
        agent.conversation_memory.clear()
    
        return {"status": "cleared", "message": " History is deleted"}
from functools import lru_cache

from app.agent.analytics_agent import AnalyticsAgent
from app.builder import create_agent


@lru_cache
def get_agent() -> AnalyticsAgent:
    """
    Creates the AnalyticsAgent once and reuses the same instance
    for all incoming requests.
    """
    return create_agent()
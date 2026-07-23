from app.database.connection import SQLiteConnection
from app.database.schema_provider import SchemaProvider
from app.database.executor import SQLExecutor

from app.llm.clients import LLMClient

from app.tools.sql_tool import SQLTool
from app.tools.pandas_tool import PandasTool
from app.tools.chart_tool import ChartTool
from app.tools.insight_tool import InsightTool

from app.memory.conversation_memory import ConversationMemory

from app.agent.llm_planner import LLMPlanner

from app.agent.analytics_agent import AnalyticsAgent


from app.tools.kpi_tool import KPITool

def create_agent() -> AnalyticsAgent:
    connection = SQLiteConnection()

    schema_provider = SchemaProvider(connection)

    executor = SQLExecutor()

    llm = LLMClient()

    memory = ConversationMemory()

    sql_tool = SQLTool(executor,llm,schema_provider,memory)
    pandas_tool = PandasTool()
    chart_tool = ChartTool(llm)
    insight_tool = InsightTool(llm)

    kpi_tool = KPITool()

    

    planner =LLMPlanner(llm)

    agent = AnalyticsAgent(planner,sql_tool,pandas_tool,chart_tool,insight_tool,kpi_tool,memory)

    return agent


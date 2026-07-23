from app.agent.base_planner import BasePlanner
from app.tools.sql_tool import SQLTool
from app.tools.pandas_tool import PandasTool
from app.tools.chart_tool import ChartTool
from app.tools.insight_tool import InsightTool
from app.models.state import AgentState
from app.tools.kpi_tool import KPITool
from app.memory.conversation_memory import ConversationMemory

from app.config.logger import setup_logger


logger = setup_logger(__name__)

class AnalyticsAgent:

    def __init__(
        self,
        planner:BasePlanner ,
        sql_tool:SQLTool,
        pandas_tool:PandasTool,
        chart_tool:ChartTool,
        insight_tool:InsightTool,
        kpi_tool:KPITool,
        conversation_memory: ConversationMemory

    ):
        self.planner = planner

        self.sql_tool = sql_tool
        self.pandas_tool = pandas_tool
        self.chart_tool = chart_tool
        self.insight_tool = insight_tool
        self.kpi_tool = kpi_tool
        self.conversation_memory = conversation_memory


        self.tools ={
            'sql' : self.sql_tool,
            'pandas' : self.pandas_tool,
            'chart' : self.chart_tool,
            'insight' : self.insight_tool,
            'kpi_tool' : self.kpi_tool

        }


    async def run(self,state: AgentState )-> AgentState:

        try:

            logger.info("Agent started")


            plan = await self.planner.create_plan(question=state.question)

            print(plan)
    
            logger.info(f"Execution plan: {plan.steps}")

            # Core pipeline (always runs)
            state = await self.sql_tool.run(state)
            state = await self.pandas_tool.run(state)
            state = await self.kpi_tool.run(state)

            # Optional tools
            if "chart" in plan.steps:
                state = await self.chart_tool.run(state)

            # Always runs
            state = await self.insight_tool.run(state)

            return state

              
       
        
        except Exception as e:
            logger.exception(f"Agent failed: {e}")
            raise
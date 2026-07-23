from app.tools.base_tool import BaseTool
from app.models.state import AgentState
import pandas as pd
from app.database.executor import SQLExecutor
from app.llm.clients import LLMClient
from app.database.schema_provider import SchemaProvider
from app.config.prompts import build_sql_prompt

from app.config.logger import setup_logger

from app.validation.sql_validation import SQLValidator

from app.memory.conversation_memory import ConversationMemory


logger = setup_logger(__name__)


class SQLTool(BaseTool):

    def __init__(self,executor:SQLExecutor,llm: LLMClient,schema_provider:SchemaProvider,conversation_memory:ConversationMemory):
        self.executor = executor
        self.llm = llm
        self.schema_provider = schema_provider
        self.conversation_memory = conversation_memory

    async def _generate_sql(self, state: AgentState) -> str:
        question = state.question

        history = self.conversation_memory.get_context(4)

        state.schema = await self.schema_provider.get_schema(state.database_path)


        prompt = build_sql_prompt(question,state.schema,history)


        sql = await self.llm.generate(prompt)

       

        logger.info(f"Generated SQL:\n{sql}")



        return sql






        

    def _execute_sql(self,database_path:str,sql:str) -> pd.DataFrame :

        return self.executor.execute(database_path,sql)
        

    async def run(self,state: AgentState) -> AgentState:

        sql = await self._generate_sql(state)

        logger.info(f"Generated SQL:\n{sql}")

        SQLValidator.validate_sql(sql)

        df = self._execute_sql(state.database_path,sql)

        logger.info(f"df is None: {df is None}")

        if df is None:
            raise ValueError("SQL execution failed.")

        if df.empty:
            state.df_analysis = {
                "empty": True
            }

        logger.info(f"Rows returned: {len(df)}")

        self.conversation_memory.add(state.question)

        state.generated_sql = sql
        state.df = df
        return state



        
        
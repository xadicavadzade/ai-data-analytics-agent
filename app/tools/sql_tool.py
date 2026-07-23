from app.tools.base_tool import BaseTool
from app.models.state import AgentState
import pandas as pd
from app.database.executor import SQLExecutor
from app.llm.clients import LLMClient
from app.database.schema_provider import SchemaProvider
from app.config.prompts import build_sql_prompt,build_sql_correction_prompt

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

    async def _correct_sql(self,state: AgentState,previous_sql: str,error: str,) -> str:
        prompt = build_sql_correction_prompt(state.question,state.schema,previous_sql,error)

        sql = await self.llm.generate(prompt)

        return sql


    async def _generate_and_execute_sql(self,state: AgentState) -> tuple[str, pd.DataFrame]:

        sql = ""  #if sql generation fails, regeneration needs previous sql

        try :
            sql = await self._generate_sql(state)

            logger.info(f"Generated SQL:\n{sql}")

            SQLValidator.validate_sql(sql)
            
            df = self._execute_sql(state.database_path,sql)

            if df.empty:
                raise ValueError("The SQL returned zero rows.")

        except Exception as e:


            sql = await self._correct_sql(
                state,
                previous_sql=sql,
                error=str(e)
            )

            SQLValidator.validate_sql(sql)

            df = self._execute_sql(state.database_path,sql)

            if df.empty:
                raise ValueError("Corrected SQL also returned zero rows.")

            logger.info(f"Corrected SQL:\n{sql}")

        return sql,df



    async def _generate_sql(self, state: AgentState) -> str:
        question = state.question

        history = self.conversation_memory.get_context(4)

        state.schema = await self.schema_provider.get_schema(state.database_path)


        prompt = build_sql_prompt(question,state.schema,history)


        sql = await self.llm.generate(prompt)

        logger.info(f"RAW SQL: {repr(sql)}")


        return sql.strip()






        

    def _execute_sql(self,database_path:str,sql:str) -> pd.DataFrame :

        return self.executor.execute(database_path,sql)
        

    async def run(self,state: AgentState) -> AgentState:

        sql,df = await self._generate_and_execute_sql(state)


        logger.info(f"Rows returned: {len(df)}")

        self.conversation_memory.add(state.question)

        state.generated_sql = sql
        state.df = df
        return state



        
        
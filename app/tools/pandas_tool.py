import pandas as pd

from app.models.state import AgentState
from app.tools.base_tool import BaseTool


class PandasTool(BaseTool):

    def _basic_analysis(self, df: pd.DataFrame) -> dict:
        return {
            "shape": {
                "rows": len(df),
                "columns": len(df.columns),
            },
            "columns": list(df.columns),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "missing": df.isna().sum().to_dict(),
            "summary": df.describe(include="all").to_dict(),
            "head": df.head(5).to_dict(orient="records"),
        }

    def _column_analysis(self, df: pd.DataFrame) -> dict:
        return {
            "numeric_columns": df.select_dtypes(include="number").columns.tolist(),
            "categorical_columns": df.select_dtypes(include=["object", "category"]).columns.tolist(),
            "datetime_columns": df.select_dtypes(include=["datetime", "datetimetz"]).columns.tolist(),
        }

    def _unique_analysis(self, df: pd.DataFrame) -> dict:
        return {
            "unique_counts": df.nunique().to_dict(),
            "top_values": {
                col: df[col].value_counts().head(5).to_dict()
                for col in df.columns
            },
        }

    def _quality_analysis(self, df: pd.DataFrame) -> dict:
        return {
            "duplicates": int(df.duplicated().sum()),
            "memory_usage_mb": round(
                df.memory_usage(deep=True).sum() / (1024 * 1024),
                2,
            ),
        }

    def _correlation_analysis(self, df: pd.DataFrame) -> dict:
        numeric_df = df.select_dtypes(include="number")

        if numeric_df.shape[1] < 2:
            return {"correlation": {}}

        return {
            "correlation": numeric_df.corr().round(3).to_dict()
        }

    def _analyze_dataframe(self, state: AgentState) -> dict:

        df = state.df

        if df is None or df.empty:
            raise ValueError("No dataframe found.")

        analysis = {}

        analysis.update(self._basic_analysis(df))
        analysis.update(self._column_analysis(df))
        analysis.update(self._unique_analysis(df))
        analysis.update(self._quality_analysis(df))
        analysis.update(self._correlation_analysis(df))

        return analysis

    async def run(self, state: AgentState) -> AgentState:

        state.df_analysis = self._analyze_dataframe(state)

        return state
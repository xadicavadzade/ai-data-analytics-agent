import pandas as pd

from app.models.state import AgentState
from app.tools.base_tool import BaseTool


class KPITool(BaseTool):

    def _build_kpis(self, df: pd.DataFrame) -> dict:

        numeric_df = df.select_dtypes(include="number")
        categorical_df = df.select_dtypes(include=["object", "category"])

        kpis = {
            "row_count": len(df),
            "column_count": len(df.columns),
            "duplicate_rows": int(df.duplicated().sum()),
            "missing_values": int(df.isna().sum().sum()),
        }

        if not numeric_df.empty:
            kpis["numeric_summary"] = {
                column: {
                    "sum": float(numeric_df[column].sum()),
                    "mean": float(numeric_df[column].mean()),
                    "min": float(numeric_df[column].min()),
                    "max": float(numeric_df[column].max()),
                }
                for column in numeric_df.columns
            }

        if not categorical_df.empty:
            kpis["top_categories"] = {
                column: {
                    "value": df[column].mode(dropna=True).iloc[0]
                    if not df[column].mode(dropna=True).empty
                    else None,
                    "count": int(df[column].value_counts().iloc[0])
                    if not df[column].value_counts().empty
                    else 0,
                }
                for column in categorical_df.columns
            }

        kpis["unique_counts"] = {
            column: int(df[column].nunique())
            for column in df.columns
        }

        return kpis

    async def run(self, state: AgentState) -> AgentState:

        if state.df is None or state.df.empty:
            raise ValueError("No dataframe found.")

        state.kpis = self._build_kpis(state.df)

        return state
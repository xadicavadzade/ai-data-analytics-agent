import json


def build_chart_prompt(question: str, columns: list[str], analysis: dict) -> str:
    return f"""
You are a senior data visualization planner.

Your task is to decide whether a chart should be created.

Available chart types:
- bar
- line
- pie
- scatter
- histogram

Available columns:
{json.dumps(columns, indent=2)}

Data analysis:
{json.dumps(analysis, indent=2, default=str)}

User question:
{question}

Rules:

- Return ONLY valid JSON.
- Never explain your reasoning.
- Never use markdown.
- Never invent columns.
- Never invent chart types.
- Use ONLY the provided columns.
- If no visualization is useful, return:

{{"charts":[]}}

Response format:

{{
    "charts":[
        {{
            "chart_type":"bar",
            "x":"category",
            "y":"total_sales",
            "title":"Total Sales by Category"
        }}
    ]
}}
"""


def build_sql_prompt(question: str,schema: str,history: list[str]) -> str:

    history_text = (
        "\n".join(history)
        if history
        else "No previous conversation.")

    return f"""
You are a senior SQLite SQL engineer.

Generate ONE valid SQLite query.

Database schema:

{schema}

Previous Conversation:

{history_text}

Current User Question:

{question}

Rules:

- Return ONLY SQL.
- Never explain.
- Never use markdown.
- Never wrap SQL with ```sql.
- Use ONLY existing tables.
- Use ONLY existing columns.
- Never invent tables.
- Never invent columns.
- Never query SQLite internal tables.
- Never use:
    sqlite_master
    sqlite_sequence
    sqlite_stat1
    sqlite_*
- Never use UNION unless explicitly required.
- If the question cannot be answered from the schema, return EXACTLY:

CANNOT_GENERATE_SQL
"""

def build_insight_prompt(
    question: str,
    generated_sql: str,
    analysis: dict,
    kpis: dict,
) -> str:
    return f"""
You are a senior data analyst and business intelligence expert.

Your task is to analyze the provided data and generate a professional business insight report.

=========================
USER QUESTION
=========================
{question}

=========================
EXECUTED SQL
=========================
{generated_sql}

=========================
DATA SUMMARY
=========================
{json.dumps(analysis, indent=2, default=str)}

=========================
CALCULATED KPIs
=========================
{json.dumps(kpis, indent=2, default=str)}

=========================
INSTRUCTIONS
=========================

- Answer the user's question using ONLY the provided information.
- Do NOT invent facts, statistics, trends, or assumptions.
- Every conclusion must be supported by the supplied data.
- If the available information is insufficient, clearly state that the answer cannot be determined.
- Consider the SQL scope when interpreting the results. Do not generalize beyond the returned data.
- Keep the insights clear, concise, and business-oriented.

Return your response in EXACTLY the following JSON format:

{{
  "summary": "A concise 1–2 sentence executive summary.",
  "key_findings": [
    "Finding 1",
    "Finding 2",
    "Finding 3"
  ],
  "breakdown": "Explain which segment, category, or group stands out and why.",
  "recommendation": "Provide a practical, data-driven business recommendation.",
  "caveat": "Mention any limitations such as sample size, SQL scope, missing values, duplicate records, or unavailable information."
}}

Rules:
- Return ONLY valid JSON.
- Do NOT wrap the response in markdown.
- Do NOT include explanations before or after the JSON.
- Ensure the JSON is syntactically valid.
"""

def build_planner_prompt(question: str) -> str:
    return f"""
You are an execution planner for an AI data analytics agent.

Your task is to decide which OPTIONAL tools should run.

Core pipeline (always executed automatically):

1. sql
   - Generate SQL.
   - Execute the query.
   - Return a dataframe.

2. pandas
   - Analyze the dataframe.

3. kpi
   - Generate KPI metrics.

4. insight
   - Generate business insights.

The ONLY optional tool is: but most of the time create chart


chart
- Create one or more visualizations.

Generate a chart ONLY if the user explicitly requests or clearly implies a visualization.

Examples of visualization requests:

- chart
- graph
- plot
- visualization
- dashboard
- histogram
- scatter plot
- bar chart
- line chart
- pie chart
- heatmap
- visualize
- compare visually
- show trends

Examples

Question:
Show all sales.

Output:
{{"steps":[]}}

Question:
Which category has the highest sales?

Output:
{{"steps":[]}}

Question:
Plot sales by category.

Output:
{{"steps":["chart"]}}

Question:
Create a dashboard of sales.

Output:
{{"steps":["chart"]}}

Rules:

- Return ONLY valid JSON.
- Never include sql, pandas, kpi, or insight.
- Only return optional tools.
- If no optional tool is needed, return:
{{"steps":[]}}

Question:
{question}
"""


def build_sql_correction_prompt(
    question: str,
    schema: str,
    previous_sql: str,
    error: str,
) -> str:
    return f"""
You are an expert SQL engineer.

The previous SQL failed.

Question:
{question}

Schema:
{schema}

Previous SQL:
{previous_sql}

Failure:
{error}

Generate a corrected SQL query.

Rules:
- Return ONLY SQL.
- Do not explain.
- Use only the provided schema.
"""
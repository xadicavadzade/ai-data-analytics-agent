# AI Data Analytics Agent

An intelligent multi-tool AI Data Analytics Agent that transforms natural language questions into actionable business insights. The system combines LLM reasoning, SQL generation, Python data analysis, KPI calculation, visualization, and AI-powered insight generation through a modular agent architecture.

**Live Demo:** https://ai-analytic-agent.netlify.app/
**Backend :** https://ai-data-analytics-agent-p0fg.onrender.com

---

<img width="1918" height="887" alt="image" src="https://github.com/user-attachments/assets/a0a13071-2a79-44e6-bb85-f55c4f6bdad5" />

<img width="1917" height="891" alt="image" src="https://github.com/user-attachments/assets/16108961-0487-43af-9335-33c6d63aef36" />



## Overview

This project demonstrates how Large Language Models can orchestrate multiple specialized tools instead of simply generating text.

Rather than relying on a single prompt, the agent analyzes the user's request, creates an execution plan, selects the appropriate tools, executes them in sequence, and returns a complete analytical response.

Example questions:

- "What are the top-selling products?"
- "Show monthly revenue trends."
- "Calculate the average customer spending."
- "Generate a visualization for sales by category."
- "Give me business insights from this dataset."

---

# Features

- Natural language analytics
- AI-powered query planning
- Automatic SQL generation
- SQLite database integration
- Pandas-based data processing
- Automatic chart generation
- KPI calculation
- AI-generated business insights
- Conversation memory
- Modular tool architecture
- FastAPI REST API
- Responsive frontend
- Docker support
- Render backend deployment
- Netlify frontend deployment

---

# System Architecture

```text
                    User
                      │
                      ▼
              Frontend (Netlify)
                      │
              HTTP REST Request
                      │
                      ▼
             FastAPI Backend (Render)
                      │
                      ▼
             Analytics Agent
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
   LLM Planner             Conversation Memory
        │
        ▼
 Creates Execution Plan
        │
        ▼
 ┌──────────────────────────────────────────┐
 │                Tools                     │
 ├──────────────────────────────────────────┤
 │ SQL Tool                                │
 │ Pandas Tool                             │
 │ KPI Tool                                │
 │ Chart Tool                              │
 │ Insight Tool                            │
 └──────────────────────────────────────────┘
        │
        ▼
 SQLite Database / DataFrame / Charts
        │
        ▼
 AI Generated Response
        │
        ▼
            Frontend Display
```

---

# Agent Workflow

```text
User Question
      │
      ▼
LLM Planner
      │
Creates Execution Plan
      │
      ▼
Select Required Tools
      │
      ▼
Execute Tools Sequentially
      │
      ▼
Collect Results
      │
      ▼
Generate Business Insights
      │
      ▼
Return Final Response
```

---

# Project Structure

```text
app
│
├── agent
│   ├── analytics_agent.py
│   ├── llm_planner.py
│
├── api
│
├── config
│
├── database
│   ├── connection.py
│   ├── executor.py
│   ├── schema_provider.py
│
├── llm
│
├── memory
│
├── models
│
├── schemas
│
├── tools
│   ├── sql_tool.py
│   ├── pandas_tool.py
│   ├── chart_tool.py
│   ├── insight_tool.py
│   └── kpi_tool.py
│
└── validation
```

---

# AI Components

## LLM Planner

The planner acts as the reasoning engine of the system.

Responsibilities:

- Understand user intent
- Analyze the analytical task
- Decide which tools are required
- Produce an execution plan
- Coordinate multi-step reasoning

---

## SQL Tool

Responsible for:

- Understanding database schema
- Generating SQL queries
- Executing SQL
- Returning structured data

---

## Pandas Tool

Handles:

- Data transformation
- Aggregations
- Cleaning
- Statistical calculations
- Advanced dataframe operations

---

## KPI Tool

Calculates important business metrics such as:

- Revenue
- Profit
- Growth
- Sales
- Customer statistics

---

## Chart Tool

Uses AI to determine:

- Best visualization type
- Chart configuration
- Titles
- Axes

Then generates charts automatically.

---

## Insight Tool

Transforms raw analytical outputs into business-friendly insights.

Instead of only returning numbers, the model explains:

- trends
- anomalies
- opportunities
- recommendations

---

## Conversation Memory

Maintains conversational context so the agent can answer follow-up questions naturally without repeating previous work.

---

# Tech Stack

### Backend

- Python
- FastAPI
- SQLite
- Pandas
- Matplotlib
- Pydantic
- Uvicorn

### AI

- Groq API
- LLM-based Planning
- Natural Language to SQL
- AI Insight Generation

### Frontend

- HTML

### Deployment

- Render (Backend)
- Netlify (Frontend)
- Docker

---

# API Flow

```text
Browser
    │
    ▼
FastAPI Endpoint
    │
    ▼
Analytics Agent
    │
    ▼
LLM Planner
    │
    ▼
Selected Tools
    │
    ▼
Database + Pandas + Charts
    │
    ▼
Business Insights
    │
    ▼
JSON Response
```

---

# Running Locally

## Clone

```bash
git clone https://github.com/your-username/your-repository.git

cd your-repository
```

---

## Install

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=YOUR_API_KEY
```

---

## Run

```bash
uvicorn main:app --reload
```

Backend:

```
http://localhost:8000
```

---

# Docker

Build:

```bash
docker build -t ai-data-analytics-agent .
```

Run:

```bash
docker run -p 8000:8000 ai-data-analytics-agent
```

---

# Deployment

### Frontend

Netlify

https://ai-analytic-agent.netlify.app/

### Backend

Render

The backend API is deployed on Render and serves the FastAPI application, while the frontend is hosted separately on Netlify. CORS is configured to allow secure communication between both deployments.

---

# Key AI Concepts Demonstrated

- Agentic AI
- LLM Planning
- Tool Calling
- Natural Language → SQL
- Multi-step Reasoning
- AI-assisted Data Analysis
- Business Insight Generation
- Modular AI Architecture
- Conversation Memory
- Backend API Design

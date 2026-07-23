from pydantic import BaseModel


class AnalystInsight(BaseModel):
    summary: str
    key_findings: list[str]
    breakdown: str
    recommendation: str
    caveat: str
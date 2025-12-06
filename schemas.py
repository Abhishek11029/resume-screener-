from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class JobDescription(BaseModel):
    description: str


class ScoreBreakdown(BaseModel):
    skill_match: float
    semantic_similarity: float
    experience_match: float
    education_projects: float


class CandidateRanking(BaseModel):
    resume_id: str
    filename: str
    total_score: float
    scores: ScoreBreakdown
    strengths: List[str]
    weaknesses: List[str]
    summary: str


class RankingResponse(BaseModel):
    rankings: List[CandidateRanking]


class ResumeReport(BaseModel):
    resume_id: str
    filename: str
    parsed_data: Dict[str, Any]
    scores: ScoreBreakdown
    strengths: List[str]
    weaknesses: List[str]
    summary: str


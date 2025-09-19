from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class IntentLevel(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class OfferModel(BaseModel):
    name: str
    value_props: List[str]
    ideal_use_cases: List[str]

class LeadModel(BaseModel):
    name: str
    role: str
    company: str
    industry: str
    location: str
    linkedin_bio: str

class ScoredLeadModel(BaseModel):
    name: str
    role: str
    company: str
    intent: IntentLevel
    score: int
    reasoning: str

from typing import List, Dict
from app.models import LeadModel, IntentLevel


def calculate_rule_score(lead: Dict, offer: Dict) -> tuple[int, str]:
    """Calculate rule-based score (0-50 points)"""
    score = 0
    reasons = []

    # Role relevance (max 20 points)
    role = lead.get('role', '').lower()
    decision_maker_roles = ['ceo', 'cto', 'vp', 'director', 'head', 'founder', 'president']
    influencer_roles = ['manager', 'lead', 'senior', 'architect', 'specialist']

    if any(dm_role in role for dm_role in decision_maker_roles):
        score += 20
        reasons.append("Decision maker role (+20)")
    elif any(inf_role in role for inf_role in influencer_roles):
        score += 10
        reasons.append("Influencer role (+10)")
    else:
        reasons.append("Individual contributor role (+0)")

    # Industry match (max 20 points)
    industry = lead.get('industry', '').lower()
    ideal_cases = [case.lower() for case in offer.get('ideal_use_cases', [])]

    # Check for exact or partial matches
    if any(case in industry for case in ideal_cases):
        score += 20
        reasons.append("Perfect industry match (+20)")
    elif 'saas' in industry or 'software' in industry or 'tech' in industry:
        score += 10
        reasons.append("Adjacent industry match (+10)")
    else:
        reasons.append("No industry match (+0)")

    # Data completeness (max 10 points)
    required_fields = ['name', 'role', 'company', 'industry', 'location', 'linkedin_bio']
    complete_fields = sum(1 for field in required_fields if lead.get(field, '').strip())

    if complete_fields == len(required_fields):
        score += 10
        reasons.append("Complete profile (+10)")
    else:
        missing = len(required_fields) - complete_fields
        reasons.append(f"Missing {missing} fields (+0)")

    return score, "; ".join(reasons)


def determine_intent_from_score(total_score: int) -> IntentLevel:
    """Convert total score to intent level"""
    if total_score >= 70:
        return IntentLevel.HIGH
    elif total_score >= 40:
        return IntentLevel.MEDIUM
    else:
        return IntentLevel.LOW

from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import pandas as pd
import io
from app.models import OfferModel, ScoredLeadModel

router = APIRouter()

# Storage for uploaded data (in-memory for this demo)
stored_offer = None
stored_leads = []


@router.post("/offer")
async def create_offer(offer: OfferModel):
    global stored_offer
    stored_offer = offer
    return {"message": "Offer saved successfully", "offer": offer}


@router.post("/leads/upload")
async def upload_leads(file: UploadFile = File(...)):
    global stored_leads

    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be CSV format")

    try:
        # Read CSV file
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))

        # Validate required columns
        required_columns = ['name', 'role', 'company', 'industry', 'location', 'linkedin_bio']
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(status_code=400, detail=f"CSV must contain columns: {required_columns}")

        # Convert to list of dicts and store
        stored_leads = df.to_dict('records')

        return {"message": f"Successfully uploaded {len(stored_leads)} leads"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")


@router.post("/score")
async def score_leads():
    global scored_results

    if not stored_offer:
        raise HTTPException(status_code=400, detail="No offer data found. Upload offer first.")

    if not stored_leads:
        raise HTTPException(status_code=400, detail="No leads found. Upload leads first.")

    from app.services.scoring import calculate_rule_score, determine_intent_from_score
    from app.services.ai_service import get_ai_score

    scored_results = []

    for lead in stored_leads:
        # Calculate rule-based score
        rule_score, rule_reasoning = calculate_rule_score(lead, stored_offer.dict())

        # Get AI score
        ai_score, ai_reasoning = get_ai_score(lead, stored_offer.dict())

        # Combine scores
        total_score = rule_score + ai_score
        intent = determine_intent_from_score(total_score)

        # Create result
        result = {
            "name": lead["name"],
            "role": lead["role"],
            "company": lead["company"],
            "intent": intent,
            "score": total_score,
            "reasoning": f"Rules: {rule_reasoning}. AI: {ai_reasoning}"
        }
        scored_results.append(result)

    return {"message": f"Successfully scored {len(scored_results)} leads"}


# Add storage for results at top of file
scored_results = []


@router.get("/results", response_model=List[ScoredLeadModel])
async def get_results():
    if not scored_results:
        raise HTTPException(status_code=400, detail="No scored results found. Run /score first.")

    return scored_results

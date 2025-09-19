# Lead Scoring API

AI-powered lead scoring system that combines rule-based logic with OpenAI analysis to evaluate prospect buying intent.

## 🚀 Live Demo
**API Base URL:** https://lead-scoring-api-zkyv.onrender.com
**Interactive Docs:** https://lead-scoring-api-zkyv.onrender.com/docs

## Setup Instructions

1. **Clone repository:**
   git clone https://github.com/Chandrakala-E75/lead-scoring-api.git
   cd lead-scoring-api 

Install dependencies:
pip install -r requirements.txt

Set environment variable:
# Create .env file
   OPENAI_API_KEY=your_openai_api_key_here

## Run locally:
uvicorn app.main:app --reload

API Usage Examples
1. Upload Product Offer
  curl -X POST "https://lead-scoring-api-zkyv.onrender.com/offer" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AI Outreach Automation",
    "value_props": ["24/7 outreach", "6x more meetings"],
    "ideal_use_cases": ["B2B SaaS mid-market"]
  }'
2. Upload Leads CSV
  curl -X POST "https://lead-scoring-api-zkyv.onrender.com/leads/upload" \
  -F "file=@test_leads.csv"
3. Score All Leads
   curl -X POST "https://lead-scoring-api-zkyv.onrender.com/score"
4. Get Scored Results
    curl -X GET "https://lead-scoring-api-zkyv.onrender.com/results"
   
## Scoring Logic

Rule Layer (0-50 points)
Role Relevance: Decision maker (+20), Influencer (+10), Individual contributor (+0)
Industry Match: Exact ICP (+20), Adjacent industry (+10), No match (+0)
Data Completeness: All fields present (+10), Missing fields (+0)

AI Layer (0-50 points)
OpenAI GPT-3.5-turbo analyzes lead profile against offer context
Intent Classification: High (50pts), Medium (30pts), Low (10pts)
Prompt: Evaluates role relevance, company fit, and potential need

Final Scoring
Total Score: Rule points + AI points (0-100)
Intent Levels: High (70+), Medium (40-69), Low (<40)

Tech Stack
FastAPI - Modern Python web framework
OpenAI API - GPT-3.5-turbo for intent analysis
Pandas - CSV processing
Pydantic - Data validation
Render - Cloud deployment

CSV Format
csvname,role,company,industry,location,linkedin_bio
John Smith,VP Sales,TechCorp,SaaS,San Francisco,Experienced sales leader


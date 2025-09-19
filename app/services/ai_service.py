import os
from openai import OpenAI
from typing import Dict
from app.models import IntentLevel
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_ai_score(lead: Dict, offer: Dict) -> tuple[int, str]:
    """Get AI-based score (0-50 points) and reasoning"""

    try:
        # Create prompt with lead and offer context
        prompt = f"""
        Analyze this lead's buying intent for the given product offer.

        LEAD PROFILE:
        - Name: {lead.get('name')}
        - Role: {lead.get('role')}
        - Company: {lead.get('company')} 
        - Industry: {lead.get('industry')}
        - Location: {lead.get('location')}
        - LinkedIn Bio: {lead.get('linkedin_bio')}

        PRODUCT OFFER:
        - Name: {offer.get('name')}
        - Value Props: {', '.join(offer.get('value_props', []))}
        - Ideal Use Cases: {', '.join(offer.get('ideal_use_cases', []))}

        Based on the lead's profile and the product fit, classify their buying intent as High, Medium, or Low.
        Explain your reasoning in 1-2 sentences focusing on role relevance, company fit, and potential need.

        Respond in this format:
        Intent: [High/Medium/Low]
        Reasoning: [Your explanation]
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.3
        )

        result = response.choices[0].message.content.strip()

        # Parse the response
        lines = result.split('\n')
        intent_line = next((line for line in lines if line.startswith('Intent:')), '')
        reasoning_line = next((line for line in lines if line.startswith('Reasoning:')), '')

        # Extract intent and convert to score
        intent = intent_line.replace('Intent:', '').strip()
        reasoning = reasoning_line.replace('Reasoning:', '').strip()

        if 'High' in intent:
            ai_score = 50
        elif 'Medium' in intent:
            ai_score = 30
        else:
            ai_score = 10

        return ai_score, reasoning

    except Exception as e:
        # Fallback scoring if AI fails
        return 25, f"AI analysis unavailable: {str(e)}"

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any

from src.core.database import get_db
from src.models.user import User
from src.schemas.persona import OnboardingData, PersonaGenerationRequest
from src.services.persona_generation_service import PersonaGenerationService
from src.services.persona_service import PersonaService
from src.api.deps import get_current_user

router = APIRouter(prefix="/onboarding", tags=["onboarding"])

@router.post("/generate-persona")
async def generate_persona(
    request: PersonaGenerationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a persona from onboarding data using AI"""
    service = PersonaGenerationService(db)
    
    try:
        generated_persona = await service.generate_persona_from_onboarding(
            current_user.id,
            request.onboarding_data,
            request.custom_instructions
        )
        
        # Return the generated persona without saving yet
        return {
            "message": "Persona generated successfully",
            "persona": {
                "name": generated_persona.name,
                "persona_type": generated_persona.persona_type,
                "context": generated_persona.context,
                "professional_details": generated_persona.professional_details,
                "ai_settings": generated_persona.ai_settings,
                "response_templates": generated_persona.response_templates,
                "generated_by_ai": True
            },
            "preview": await service.get_persona_preview(generated_persona)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Persona generation failed: {str(e)}"
        )

@router.post("/save-persona")
async def save_generated_persona(
    persona_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Save the generated persona to the database"""
    from src.schemas.persona import PersonaCreate
    
    persona_create = PersonaCreate(
        name=persona_data.get("name"),
        persona_type=persona_data.get("persona_type", "custom"),
        context=persona_data.get("context", {}),
        professional_details=persona_data.get("professional_details", {}),
        ai_settings=persona_data.get("ai_settings", {}),
        is_default=persona_data.get("is_default", False)
    )
    
    service = PersonaService(db)
    persona = service.create_persona(current_user.id, persona_create)
    
    # Mark as AI-generated
    persona.generated_by_ai = True
    db.commit()
    
    return {
        "message": "Persona saved successfully",
        "persona": persona
    }

@router.get("/industries")
async def get_industries():
    """Get list of supported industries for onboarding"""
    return {
        "industries": [
            {"id": "healthcare", "name": "Healthcare", "icon": "🏥"},
            {"id": "real_estate", "name": "Real Estate", "icon": "🏠"},
            {"id": "banking_finance", "name": "Banking & Finance", "icon": "💰"},
            {"id": "software_development", "name": "Software Development", "icon": "💻"},
            {"id": "legal", "name": "Legal", "icon": "⚖️"},
            {"id": "education", "name": "Education", "icon": "📚"},
            {"id": "sales", "name": "Sales", "icon": "📊"},
            {"id": "marketing", "name": "Marketing", "icon": "📈"},
            {"id": "consulting", "name": "Consulting", "icon": "💼"},
            {"id": "hospitality", "name": "Hospitality", "icon": "🏨"},
            {"id": "custom", "name": "Custom", "icon": "✨"}
        ]
    }

@router.get("/industry-questions/{industry}")
async def get_industry_questions(industry: str):
    """Get onboarding questions for a specific industry"""
    questions = {
        "healthcare": [
            {"id": "specialization", "type": "multiselect", "label": "What is your medical specialization?", "options": ["Cardiology", "Pediatrics", "Oncology", "Neurology", "Orthopedics", "Other"]},
            {"id": "hospital", "type": "text", "label": "Which hospital or practice do you work with?"},
            {"id": "certifications", "type": "multiselect", "label": "What certifications do you hold?", "options": ["Board Certified", "ACLS", "BLS", "Fellowship", "Other"]},
            {"id": "patient_type", "type": "select", "label": "Who are your primary patients?", "options": ["Adults", "Children", "Elderly", "All"]}
        ],
        "real_estate": [
            {"id": "agency", "type": "text", "label": "What real estate agency are you with?"},
            {"id": "expertise", "type": "multiselect", "label": "What type of properties do you specialize in?", "options": ["Residential", "Commercial", "Luxury", "Industrial", "Land"]},
            {"id": "market", "type": "text", "label": "What markets do you primarily serve?"},
            {"id": "avg_price", "type": "text", "label": "What is your average sale price range?"}
        ],
        "banking_finance": [
            {"id": "bank", "type": "text", "label": "Which bank or firm do you work for?"},
            {"id": "role", "type": "select", "label": "What is your primary role?", "options": ["Wealth Manager", "Financial Advisor", "Investment Banker", "Credit Analyst", "Relationship Manager"]},
            {"id": "clients", "type": "select", "label": "Who are your primary clients?", "options": ["High-net-worth Individuals", "Corporate", "Institutional", "Retail"]}
        ],
        "software_development": [
            {"id": "tech_stack", "type": "multiselect", "label": "What is your tech stack?", "options": ["Python", "JavaScript", "TypeScript", "Go", "Rust", "Java", "C#", "React", "Vue", "Angular", "AWS", "Azure", "GCP"]},
            {"id": "seniority", "type": "select", "label": "What is your seniority level?", "options": ["Junior", "Mid-level", "Senior", "Lead", "Principal"]},
            {"id": "role", "type": "select", "label": "What is your primary role?", "options": ["Full Stack", "Backend", "Frontend", "DevOps", "Data Engineer", "ML Engineer"]}
        ]
    }
    
    return questions.get(industry, [
        {"id": "profession", "type": "text", "label": "What is your primary role?"},
        {"id": "company", "type": "text", "label": "What company or organization do you work for?"},
        {"id": "expertise", "type": "text", "label": "What is your area of expertise?"}
    ])


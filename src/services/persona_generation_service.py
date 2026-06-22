from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import json
import uuid

from src.models.persona import Persona
from src.models.user import User
from src.schemas.persona import OnboardingData, PersonaCreate
from src.ai.llm import LLMService
from src.ai.persona_builder import PersonaBuilder

class PersonaGenerationService:
    def __init__(self, db: Session):
        self.db = db
        self.llm = LLMService()
        self.builder = PersonaBuilder()
    
    async def generate_persona_from_onboarding(
        self,
        user_id: uuid.UUID,
        onboarding_data: OnboardingData,
        custom_instructions: Optional[str] = None
    ) -> Persona:
        prompt = self._build_generation_prompt(onboarding_data, custom_instructions)
        
        response = await self.llm.generate_persona(
            prompt=prompt,
            temperature=0.7,
            max_tokens=1500
        )
        
        persona_data = self._parse_generated_persona(response, onboarding_data)
        
        persona = Persona(
            user_id=user_id,
            name=f"{onboarding_data.full_name} - {onboarding_data.industry.title()}",
            persona_type=onboarding_data.industry.lower().replace(" ", "_"),
            context={
                "profession": onboarding_data.job_title,
                "specialization": onboarding_data.specialization,
                "company": onboarding_data.company,
                "location": "",
                "experience_years": onboarding_data.experience_years,
                "certifications": onboarding_data.certifications,
                "languages": onboarding_data.languages,
                "communication_style": onboarding_data.communication_style,
                "timezone": onboarding_data.timezone
            },
            professional_details=persona_data.get("professional_details", {}),
            ai_settings=persona_data.get("ai_settings", {
                "draft_style": "balanced",
                "signature": f"Best regards,\n{onboarding_data.full_name}",
                "tone_modifiers": []
            }),
            response_templates=persona_data.get("response_templates", {}),
            generated_by_ai=True,
            generation_prompt=prompt
        )
        
        return persona
    
    def _build_generation_prompt(self, data: OnboardingData, custom_instructions: str = None) -> str:
        base_prompt = f"""
        You are an expert at creating professional AI personas. Based on the following information about a user, generate a comprehensive persona profile.

        USER INFORMATION:
        - Full Name: {data.full_name}
        - Job Title: {data.job_title}
        - Company: {data.company}
        - Industry: {data.industry}
        - Specialization: {', '.join(data.specialization) if data.specialization else 'General'}
        - Experience: {data.experience_years} years
        - Communication Style: {data.communication_style}
        - Primary Audience: {data.primary_audience}
        - Certifications: {', '.join(data.certifications) if data.certifications else 'None'}
        - Languages: {', '.join(data.languages)}

        {f'CUSTOM INSTRUCTIONS: {custom_instructions}' if custom_instructions else ''}

        Generate a complete persona profile with professional_details, ai_settings, and response_templates.
        Format as a valid JSON object.
        """
        return base_prompt
    
    def _parse_generated_persona(self, response: str, onboarding_data: OnboardingData) -> Dict[str, Any]:
        try:
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return {
                    "professional_details": data.get("professional_details", {}),
                    "ai_settings": data.get("ai_settings", {
                        "draft_style": "balanced",
                        "signature": f"Best regards,\n{onboarding_data.full_name}",
                        "tone_modifiers": []
                    }),
                    "response_templates": data.get("response_templates", {})
                }
        except:
            pass
        
        return {
            "professional_details": {
                "industry": onboarding_data.industry,
                "specialization": onboarding_data.specialization
            },
            "ai_settings": {
                "draft_style": "balanced",
                "signature": f"Best regards,\n{onboarding_data.full_name}",
                "tone_modifiers": ["professional", "courteous"]
            },
            "response_templates": {}
        }
    
    async def get_persona_preview(self, persona: Persona) -> Dict[str, Any]:
        return {
            "name": persona.name,
            "type": persona.persona_type,
            "summary": f"Professional {persona.context.get('profession', '')}",
            "communication_style": persona.context.get('communication_style', 'professional'),
            "signature": persona.ai_settings.get('signature', '')
        }
    

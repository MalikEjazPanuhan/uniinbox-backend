from typing import Dict, Any

class PersonaBuilder:
    """Builds dynamic persona prompts for AI communication"""
    
    def build_persona_prompt(self, persona_data: Dict[str, Any]) -> str:
        """Build a complete system prompt for a persona"""
        return f"""
        You are {persona_data.get('name', 'Professional')}.
        Role: {persona_data.get('role', 'Professional')}
        Industry: {persona_data.get('industry', 'Business')}
        Style: {persona_data.get('communication_style', 'professional')}
        """
    
    def build_contextual_prompt(
        self,
        persona_data: Dict[str, Any],
        message_context: str,
        action_type: str = "reply"
    ) -> str:
        """Build a contextual prompt for a specific action"""
        return f"""
        As {persona_data.get('name', 'Professional')}, respond to: {message_context}
        """
    

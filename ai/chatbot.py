"""
POTENTIAL AI - Central Chatbot Service
Orchestrates the entire 12-step AI pipeline:
Input Validation -> Preprocessing -> TF-IDF Vectorization -> Intent Classification ->
Entity Extraction -> Experta Rule Engine -> Knowledge Graph Traversal ->
Response Generation -> Source Attribution.
"""

from typing import Dict, Any, Optional
from ai.response import get_response_generator
from ai.entities import extract_entities
from ai.classifier import get_classifier
from ai.knowledge_graph import get_knowledge_graph
from ai.knowledge import get_knowledge_base

class ChatbotService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChatbotService, cls).__new__(cls)
            cls._instance.response_generator = get_response_generator()
            cls._instance.classifier = get_classifier()
            cls._instance.kg = get_knowledge_graph()
            cls._instance.kb = get_knowledge_base()
        return cls._instance

    def process_message(self, message: str) -> Dict[str, Any]:
        """
        Executes full reasoning pipeline for an incoming user query.
        Returns complete response object with intent, confidence, sources, and AI details.
        """
        if not message or not str(message).strip():
            return {
                "response": "Please enter a question or topic so I can assist you with PRPCEM information.",
                "intent": "empty_input",
                "confidence": 1.0,
                "entities": {},
                "action": "PROMPT_USER",
                "reasoning": "Empty or whitespace-only message received.",
                "sources": [],
                "academic_year": "2025-26",
                "ai_details": {
                    "intent": "empty_input",
                    "confidence_score": 1.0,
                    "entities": {},
                    "experta_rule": "rule_empty_input",
                    "reasoning_action": "PROMPT_USER",
                    "knowledge_engine": "Input Validation"
                }
            }

        # Generate response from core AI pipeline
        result = self.response_generator.generate_response(str(message).strip())

        # Format consistent schema matching Phase 5.2
        return {
            "response": result.get("response", ""),
            "intent": result.get("intent", "unknown"),
            "confidence": result.get("confidence", 0.0),
            "entities": result.get("ai_details", {}).get("entities", {}),
            "action": result.get("ai_details", {}).get("reasoning_action", "UNKNOWN"),
            "reasoning": result.get("ai_details", {}).get("experta_rule", "unknown_rule"),
            "sources": result.get("sources", []),
            "academic_year": result.get("academic_year", "2025-26"),
            "ai_details": result.get("ai_details", {})
        }

def get_chatbot_service() -> ChatbotService:
    """Singleton getter for ChatbotService."""
    return ChatbotService()

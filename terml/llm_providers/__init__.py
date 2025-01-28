"""LLM Provider Interface and Implementations"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import os

class LLMProvider(ABC):
    """Base class for LLM providers"""
    
    @abstractmethod
    def get_response(self, messages: List[Dict[str, str]], system_prompt: str, max_tokens: int) -> str:
        """Get response from the LLM"""
        pass
    
    @abstractmethod
    def get_chat_response(self, user_input: str, conversation_history: List[Dict[str, str]]) -> str:
        """Get chat response from the LLM"""
        pass
    
    @abstractmethod
    def clear_chat_history(self):
        """Clear the chat history"""
        pass
    
    @abstractmethod
    def supports_streaming(self) -> bool:
        """Check if the provider supports streaming responses"""
        return False

def available_providers() -> List[str]:
    """
    Dynamically discover available LLM providers based on existing provider files.
    
    Returns:
        List of provider names (without .py extension)
    """
    current_dir = os.path.dirname(__file__)
    providers = [
        f.replace('.py', '') 
        for f in os.listdir(current_dir) 
        if f.endswith('.py') and f != '__init__.py'
    ]
    return providers

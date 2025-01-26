"""OpenRouter LLM Provider Implementation"""
import os
import requests
from typing import List, Dict, Any
from . import LLMProvider

class OpenRouterProvider(LLMProvider):
    """OpenRouter LLM provider implementation"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.conversation_history = []
        
    def get_response(self, messages: List[Dict[str, str]], system_prompt: str, max_tokens: int) -> str:
        """Get response from OpenRouter"""
        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "system", "content": system_prompt}] + messages,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error: {str(e)}"
            
    def get_chat_response(self, user_input: str, conversation_history: List[Dict[str, str]]) -> str:
        """Get chat response from OpenRouter"""
        self.conversation_history.append({"role": "user", "content": user_input})
        
        response = self.get_response(
            messages=self.conversation_history,
            system_prompt="You are a helpful assistant.",
            max_tokens=1000
        )
        
        self.conversation_history.append({"role": "assistant", "content": response})
        return response
        
    def clear_chat_history(self):
        """Clear the chat history"""
        self.conversation_history = []
        
    def supports_streaming(self) -> bool:
        """OpenRouter supports streaming responses"""
        return True

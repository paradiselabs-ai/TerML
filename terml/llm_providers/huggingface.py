"""HuggingFace LLM Provider Implementation"""
import os
import requests
from typing import List, Dict, Any
from . import LLMProvider

class HuggingFaceProvider(LLMProvider):
    """HuggingFace LLM provider implementation"""
    
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.base_url = "https://api-inference.huggingface.co/models"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.conversation_history = []
        
    def get_response(self, messages: List[Dict[str, str]], system_prompt: str, max_tokens: int) -> str:
        """Get response from HuggingFace"""
        # Convert messages to prompt format
        prompt = system_prompt + "\n\n"
        for message in messages:
            prompt += f"{message['role'].capitalize()}: {message['content']}\n"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "return_full_text": False
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/gpt2",  # Default model, can be configured
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()[0]["generated_text"]
        except Exception as e:
            return f"Error: {str(e)}"
            
    def get_chat_response(self, user_input: str, conversation_history: List[Dict[str, str]]) -> str:
        """Get chat response from HuggingFace"""
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
        """HuggingFace supports streaming responses"""
        return True

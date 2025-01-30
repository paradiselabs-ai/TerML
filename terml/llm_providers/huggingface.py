"""HuggingFace LLM Provider Implementation"""
import os
import logging
import requests
from typing import List, Dict, Any, Optional, Union
from . import LLMProvider

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HuggingFaceProviderError(Exception):
    """Custom exception for HuggingFace Provider errors"""
    pass

class HuggingFaceProvider(LLMProvider):
    """HuggingFace LLM provider implementation"""
    
    DEFAULT_MODEL = "deepseek-ai/DeepSeek-V3"
    INFERENCE_URL = "https://api-inference.huggingface.co/pipeline/"
    MODELS_URL = "https://api-inference.huggingface.co/models"
    
    def __init__(self, 
                 api_key: Optional[str] = None, 
                 model: Optional[str] = None,
                 max_retries: int = 3):
        """
        Initialize HuggingFace Provider
        
        :param api_key: HuggingFace API key (optional, will use env var if not provided)
        :param model: Specific model to use (optional, will use env var or default)
        :param max_retries: Maximum number of retries for API calls
        """
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        if not self.api_key:
            raise HuggingFaceProviderError("No HuggingFace API key provided")
        
        self.model = model or os.getenv("HUGGINGFACE_MODEL", self.DEFAULT_MODEL)
        self.max_retries = max_retries
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.conversation_history: List[Dict[str, str]] = []
        
        # Validate model on initialization
        self.validate_model(self.model)
        
    def validate_model(self, model: str) -> bool:
        """
        Validate if the specified model exists and is accessible
        
        :param model: Model name to validate
        :return: True if model is valid, False otherwise
        """
        try:
            # Use models endpoint to get model details
            response = requests.get(
                f"{self.MODELS_URL}/{model}",
                headers=self.headers
            )
            if response.status_code == 200:
                model_info = response.json()
                logger.info(f"Model {model} validated successfully")
                logger.info(f"Model Details: {model_info}")
                return True
            else:
                logger.warning(f"Model {model} validation failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Error validating model {model}: {e}")
            return False
        
    def get_model_details(self, model: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve detailed information about a specific model
        
        :param model: Model name (uses current model if not specified)
        :return: Dictionary of model details
        """
        current_model = model or self.model
        try:
            response = requests.get(
                f"{self.MODELS_URL}/{current_model}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error retrieving model details for {current_model}: {e}")
            return {}
        
    def list_available_models(self, filter_type: Optional[str] = None) -> List[str]:
        """
        List available models, optionally filtered by type
        
        :param filter_type: Optional filter like 'text-generation', 'translation', etc.
        :return: List of model names
        """
        try:
            response = requests.get(
                f"{self.MODELS_URL}",
                headers=self.headers
            )
            response.raise_for_status()
            models = response.json()
            
            if filter_type:
                models = [
                    model for model in models 
                    if filter_type.lower() in model.lower()
                ]
            
            return models
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []
        
    def get_response(self, 
                     messages: List[Dict[str, str]], 
                     system_prompt: str, 
                     max_tokens: int,
                     model: Optional[str] = None) -> str:
        """
        Get response from HuggingFace with advanced error handling
        
        :param messages: Conversation messages
        :param system_prompt: System context prompt
        :param max_tokens: Maximum tokens to generate
        :param model: Optional model override
        :return: Generated text response
        """
        # Convert messages to prompt format
        prompt = system_prompt + "\n\n"
        for message in messages:
            prompt += f"{message['role'].capitalize()}: {message['content']}\n"
        
        current_model = model or self.model
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "return_full_text": False,
                "temperature": 0.7,  # Added some randomness
                "top_p": 0.9,  # Nucleus sampling
            }
        }
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    f"{self.INFERENCE_URL}{current_model}",
                    headers=self.headers,
                    json=payload,
                    timeout=30  # Added timeout
                )
                response.raise_for_status()
                
                generated_text = response.json()[0]["generated_text"]
                logger.info(f"Successfully generated response using {current_model}")
                return generated_text
            
            except requests.exceptions.RequestException as e:
                logger.warning(f"API request failed (Attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt == self.max_retries - 1:
                    logger.error(f"All {self.max_retries} attempts failed")
                    return f"Error: {str(e)}"
        
    def get_chat_response(self, 
                           user_input: str, 
                           conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Get chat response from HuggingFace
        
        :param user_input: User's message
        :param conversation_history: Optional conversation history
        :return: AI's response
        """
        if conversation_history:
            self.conversation_history = conversation_history
        
        self.conversation_history.append({"role": "user", "content": user_input})
        
        response = self.get_response(
            messages=self.conversation_history,
            system_prompt="You are a helpful, respectful, and honest assistant.",
            max_tokens=1000
        )
        
        self.conversation_history.append({"role": "assistant", "content": response})
        return response
        
    def clear_chat_history(self):
        """Clear the chat history"""
        self.conversation_history = []
        logger.info("Chat history cleared")
        
    def supports_streaming(self) -> bool:
        """
        Check if streaming is supported
        
        :return: Always returns True for potential future implementation
        """
        return True

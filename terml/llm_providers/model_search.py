import os
import requests
import click
from typing import List, Dict, Optional

class ModelSearcher:
    """Advanced model search and discovery for Hugging Face"""
    
    SEARCH_URL = "https://huggingface.co/api/models"
    RESULTS_PER_PAGE = 10
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize ModelSearcher
        
        :param api_key: Optional API key for authenticated requests
        """
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else {},
            "Accept": "application/json"
        }
    
    def search_models(self, 
                      keyword: str, 
                      page: int = 1, 
                      task: Optional[str] = None) -> Dict:
        """
        Search for models with advanced filtering
        
        :param keyword: Search term
        :param page: Page number (1-indexed)
        :param task: Optional task filter (e.g., 'text-generation', 'translation')
        :return: Dictionary with search results and metadata
        """
        params = {
            "search": keyword,
            "sort": "downloads",  # Sort by popularity
            "limit": self.RESULTS_PER_PAGE,
            "offset": (page - 1) * self.RESULTS_PER_PAGE
        }
        
        if task:
            params["filter"] = task
        
        try:
            response = requests.get(
                self.SEARCH_URL, 
                params=params, 
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "total_models": data.get("totalModels", 0),
                "models": [
                    {
                        "id": model.get("id"),
                        "name": model.get("modelId"),
                        "downloads": model.get("downloads", 0),
                        "task": model.get("pipeline_tag"),
                        "description": model.get("description", "No description")[:100] + "..."
                    } for model in data.get("models", [])
                ]
            }
        
        except requests.RequestException as e:
            click.echo(f"Error searching models: {e}")
            return {"total_models": 0, "models": []}
    
    def interactive_model_search(self, initial_keyword: Optional[str] = None):
        """
        Interactive model search with pagination and selection
        
        :param initial_keyword: Optional initial search keyword
        """
        keyword = initial_keyword or click.prompt("Enter search keyword (or 'exit' to quit)")
        
        if keyword.lower() == 'exit':
            return None
        
        page = 1
        while True:
            results = self.search_models(keyword, page)
            
            if not results['models']:
                click.echo("No models found. Try a different keyword.")
                break
            
            click.echo(f"\nPage {page} - Total Models: {results['total_models']}")
            click.echo("-" * 50)
            
            for i, model in enumerate(results['models'], 1):
                global_index = (page-1)*10 + i
                click.echo(f"{global_index}. {model['name']}")
                click.echo(f"   Downloads: {model['downloads']}")
                click.echo(f"   Task: {model['task'] or 'Unknown'}")
                click.echo(f"   Description: {model['description']}\n")
            
            action = click.prompt(
                "Enter:\n"
                "- Model number to select\n"
                "- 'next' for next page\n"
                "- 'prev' for previous page\n"
                "- 'new' to search again\n"
                "- 'exit' to quit",
                default='next'
            )
            
            if action == 'exit':
                return None
            
            if action == 'new':
                return self.interactive_model_search()
            
            if action == 'next':
                page += 1
                continue
            
            if action == 'prev' and page > 1:
                page -= 1
                continue
            
            try:
                model_index = int(action)
                if 1 <= model_index <= len(results['models']):
                    selected_model = results['models'][model_index - 1]
                    click.echo(f"Selected Model: {selected_model['name']}")
                    return selected_model['name']
            except ValueError:
                click.echo("Invalid input. Try again.")
        
        return None

    def list_available_models(self, task_filter: Optional[str] = None) -> List[str]:
        """
        List available models, optionally filtered by task
        
        :param task_filter: Optional task filter
        :return: List of model names
        """
        try:
            response = requests.get(
                self.SEARCH_URL,
                params={"filter": task_filter} if task_filter else {},
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            
            return [model.get("modelId") for model in data.get("models", [])]
        
        except requests.RequestException as e:
            click.echo(f"Error listing models: {e}")
            return []

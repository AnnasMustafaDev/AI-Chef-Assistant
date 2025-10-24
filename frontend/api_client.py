import requests
import os
from typing import List, Dict, Optional
from langchain_community.llms import Together
from config import ENDPOINTS

class APIClient:
    def __init__(self):
        # Initialize the Together AI model
        self.model = self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize and return the LLM once"""
        return Together(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            temperature=0.7,
            max_tokens=1024,
            together_api_key=os.getenv('TOGETHER_API_KEY')
        )

    def get_recipe(self, ingredients: List[str]) -> Optional[Dict]:
        """Generate a recipe based on available ingredients using Gemini API."""
        try:
            # First try to get recipe from backend
            # response = requests.post(
            #     ENDPOINTS['recipe'],
            #     json={'ingredients': ingredients}
            # )
            # if response.status_code == 200:
            #     return response.json()

            # If backend fails, use Together AI as fallback
            prompt = f"""<s>[INST] As a chef, create a recipe using these ingredients: {', '.join(ingredients)}
            If not all ingredients are available, suggest alternatives.
            Format your response as a JSON structure with title, description, instructions list, and missing_ingredients list.
            Be creative but precise. [/INST]</s>"""
            
            recipe_text = self.model.invoke(prompt)
            
            # Parse the response into a structured format
            recipe = {
                'title': 'Generated Recipe',  # You would extract this from response
                'description': recipe_text[:200],  # First 200 chars as description
                'instructions': [recipe_text],  # Full text as instructions
                'ingredients': ingredients,
                'missing_ingredients': []
            }
            return recipe
        except Exception as e:
            print(f"Error generating recipe: {e}")
            return None

    def get_cooking_help(self, question: str) -> Optional[str]:
        """Get cooking tips and help using Gemini API."""
        try:
            prompt = f"""<s>[INST] As a cooking chef (Hamza)assistant, help with this question: {question}
            , if there is no question, then greet accordingly,Provide practical, clear advice including any relevant tips or alternatives. [/INST]</s>"""
            
            return self.model.invoke(prompt)
        except Exception as e:
            print(f"Error getting cooking help: {e}")
            return None

    def initialize_recipe(self):
        """Initialize a new recipe session."""
        try:
            response = requests.post(ENDPOINTS['initialize'])
            return response.json()
        except Exception as e:
            return {'error': str(e)}

    def get_grocery_list(self, recipe_text: str) -> Dict:
        """Get grocery list for a recipe."""
        try:
            response = requests.post(
                ENDPOINTS['grocery_list'],
                json={'recipe_text': recipe_text}
            )
            return response.json()
        except Exception as e:
            return {'error': str(e)}

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')

# API Endpoints
ENDPOINTS = {
    'initialize': f"{API_BASE_URL}/initialize",
    'recipe': f"{API_BASE_URL}/recipe",
    'grocery_list': f"{API_BASE_URL}/grocery-list"
}

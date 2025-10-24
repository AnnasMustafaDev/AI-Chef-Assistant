from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from app.database.database import get_db
from app.services.recipe_service import RecipeAssistantService
from app.models.models import Recipe, GroceryList

router = APIRouter()
recipe_service = RecipeAssistantService(faiss_index_path="pakistani_recipes_faiss")

@router.post("/initialize")
async def initialize_service(pdf_path: Optional[str] = None, recreate: bool = False):
    try:
        recipe_service.pdf_path = pdf_path
        recipe_service.initialize_vector_db(recreate=recreate)
        return {"message": "Recipe service initialized successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recipe")
async def get_recipe(query: str, db: Session = Depends(get_db)):
    try:
        # Get recipe from AI service
        recipe_data = recipe_service.get_recipe(query)
        
        if "error" in recipe_data:
            raise HTTPException(status_code=404, detail=recipe_data["error"])
        
        # Save recipe to database
        recipe = Recipe(
            name=query,
            ingredients=json.dumps(recipe_data.get("ingredients", [])),
            instructions=json.dumps(recipe_data.get("instructions", [])),
            cooking_tips=json.dumps(recipe_data.get("cooking_tips", [])),
            serving_suggestions=json.dumps(recipe_data.get("serving_suggestions", []))
        )
        db.add(recipe)
        db.commit()
        
        return recipe_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/grocery-list")
async def update_grocery_list(items: List[str], user_id: str, db: Session = Depends(get_db)):
    try:
        grocery_list = db.query(GroceryList).filter(GroceryList.user_id == user_id).first()
        if not grocery_list:
            grocery_list = GroceryList(user_id=user_id, items=json.dumps([]))
        
        current_items = json.loads(grocery_list.items)
        current_items.extend(items)
        grocery_list.items = json.dumps(list(set(current_items)))  # Remove duplicates
        
        db.add(grocery_list)
        db.commit()
        
        return {"message": "Grocery list updated successfully", "items": json.loads(grocery_list.items)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/grocery-list/{user_id}")
async def get_grocery_list(user_id: str, db: Session = Depends(get_db)):
    grocery_list = db.query(GroceryList).filter(GroceryList.user_id == user_id).first()
    if not grocery_list:
        return {"items": []}
    return {"items": json.loads(grocery_list.items)}

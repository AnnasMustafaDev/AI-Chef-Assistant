from sqlalchemy import Column, Integer, String, ForeignKey, Table, ARRAY
from sqlalchemy.orm import relationship
from app.database.database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    ingredients = Column(String)  # Stored as JSON string
    instructions = Column(String)
    cooking_tips = Column(String)
    serving_suggestions = Column(String)

class GroceryList(Base):
    __tablename__ = "grocery_lists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)  # We'll add proper user management later
    items = Column(String)  # Stored as JSON string

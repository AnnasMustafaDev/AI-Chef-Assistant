import streamlit as st
from api_client import APIClient
import json

def load_ingredients():
    try:
        with open('frontend/data/ingredients.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading ingredients: {e}")
        return []

def load_favorites():
    try:
        with open('frontend/data/favorites.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading favorites: {e}")
        return []

def save_favorites(favorites):
    try:
        with open('frontend/data/favorites.json', 'w') as f:
            json.dump(favorites, f)
    except Exception as e:
        print(f"Error saving favorites: {e}")

def show():
    st.title("Recipe Assistant 👨‍🍳")
    
    # Initialize API client
    api_client = APIClient()
    
    # Mode selection
    mode = st.radio("Select Mode", ["Recipe Generator", "Cooking Assistant"])
    
    if mode == "Recipe Generator":
        ingredients = load_ingredients()
        if not ingredients:
            st.warning("Please add ingredients in the Ingredients Manager first!")
            return
            
        st.write("Available ingredients:", ", ".join(ingredients))
        
        if st.button("Generate Recipe"):
            with st.spinner("Generating recipe..."):
                recipe = api_client.get_recipe(ingredients)
                if recipe:
                    st.subheader(recipe['title'])
                    st.write(recipe['description'])
                    st.write("Instructions:")
                    for idx, step in enumerate(recipe['instructions'], 1):
                        st.write(f"{idx}. {step}")
                        
                    # Save to favorites option
                    if st.button("Save to Favorites"):
                        favorites = load_favorites()
                        if recipe not in favorites:
                            favorites.append(recipe)
                            save_favorites(favorites)
                            st.success("Recipe saved to favorites!")
                        else:
                            st.info("Recipe already in favorites!")
                else:
                    st.error("Failed to generate recipe. Please try again.")
                    
    else:  # Cooking Assistant mode
        st.subheader("Cooking Assistant")
        question = st.text_input("Ask for cooking tips, substitutions, or techniques")
        
        if question:
            with st.spinner("Getting help..."):
                tips = api_client.get_cooking_help(question)
                if tips:
                    st.write(tips)
                else:
                    st.error("Failed to get cooking help. Please try again.")

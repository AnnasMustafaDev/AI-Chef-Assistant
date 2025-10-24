import streamlit as st
import json

def load_ingredients():
    try:
        with open('frontend/data/ingredients.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading ingredients: {e}")
        return []

def save_ingredients(ingredients):
    try:
        with open('frontend/data/ingredients.json', 'w') as f:
            json.dump(ingredients, f)
    except Exception as e:
        print(f"Error saving ingredients: {e}")

def show():
    st.title("Ingredients Manager 🥗")
    
    # Load existing ingredients
    ingredients = load_ingredients()
    
    # Add new ingredient
    col1, col2 = st.columns([3, 1])
    with col1:
        new_ingredient = st.text_input("Add new ingredient")
    with col2:
        if st.button("Add"):
            if new_ingredient and new_ingredient not in ingredients:
                ingredients.append(new_ingredient)
                save_ingredients(ingredients)
                st.success(f"Added {new_ingredient}")
    
    # Display ingredients
    if ingredients:
        st.subheader("Your Ingredients")
        for idx, ingredient in enumerate(ingredients):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"• {ingredient}")
            with col2:
                if st.button("Remove", key=f"remove_{idx}"):
                    ingredients.pop(idx)
                    save_ingredients(ingredients)
                    st.rerun()
    else:
        st.info("No ingredients added yet. Add some ingredients to get started!")

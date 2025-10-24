import streamlit as st
import json
# from api_client import APIClient

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
    st.title("Favorite Recipes ⭐")
    
    # Load favorite recipes
    favorites = load_favorites()
    
    if not favorites:
        st.info("You haven't saved any favorite recipes yet!")
        return
        
    # Display favorites
    for idx, recipe in enumerate(favorites):
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.subheader(recipe['title'])
                st.write(recipe['description'])
                if st.button("View Details", key=f"view_{idx}"):
                    st.session_state.selected_recipe = recipe
                    st.session_state.page = "Recipe Assistant"
                    st.rerun()
            with col2:
                if st.button("Remove", key=f"remove_{idx}"):
                    favorites.pop(idx)
                    save_favorites(favorites)
                    st.rerun()

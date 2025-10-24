import streamlit as st
from api_client import APIClient

def show():
    st.title("Recipe Generator")
    
    # Input for ingredients
    st.subheader("Enter Your Ingredients")
    ingredients_text = st.text_area(
        "List your ingredients (one per line)",
        height=150,
        help="Enter each ingredient on a new line"
    )
    
    if st.button("Generate Recipe", type="primary"):
        if ingredients_text.strip():
            ingredients = [ing.strip() for ing in ingredients_text.split('\n') if ing.strip()]
            
            with st.spinner("Generating your recipe..."):
                response = APIClient.get_recipe(ingredients)
                
                if 'error' in response:
                    st.error(f"Error: {response['error']}")
                else:
                    st.success("Recipe generated successfully!")
                    
                    # Display the recipe
                    st.subheader("Your Recipe")
                    st.write(response.get('recipe', ''))
                    
                    # Add to grocery list button
                    if st.button("Generate Grocery List"):
                        with st.spinner("Generating grocery list..."):
                            grocery_response = APIClient.get_grocery_list(response.get('recipe', ''))
                            if 'error' in grocery_response:
                                st.error(f"Error: {grocery_response['error']}")
                            else:
                                st.subheader("Grocery List")
                                for item in grocery_response.get('grocery_list', []):
                                    st.write(f"• {item}")
        else:
            st.warning("Please enter at least one ingredient")

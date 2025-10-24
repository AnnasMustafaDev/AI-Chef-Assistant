import streamlit as st
from api_client import APIClient

def show():
    st.title("Grocery List Generator")
    
    # Input for recipe text
    st.subheader("Enter Your Recipe")
    recipe_text = st.text_area(
        "Paste your recipe here",
        height=300,
        help="Paste the complete recipe text here"
    )
    
    if st.button("Generate Grocery List", type="primary"):
        if recipe_text.strip():
            with st.spinner("Generating grocery list..."):
                client = APIClient()
                response = client.get_grocery_list(recipe_text)
                
                if 'error' in response:
                    st.error(f"Error: {response['error']}")
                else:
                    st.success("Grocery list generated successfully!")
                    
                    # Display the grocery list
                    st.subheader("Your Grocery List")
                    for item in response.get('grocery_list', []):
                        st.write(f"• {item}")
        else:
            st.warning("Please enter a recipe")
#     if st.button("Generate Grocery List", type="primary"):
#         if recipe_text.strip():
#             with st.spinner("Generating grocery list..."):
#                 response = RecipeApiClient.get_grocery_list(recipe_text)
                
#                 if 'error' in response:
#                     st.error(f"Error: {response['error']}")
#                 else:
#                     st.success("Grocery list generated successfully!")
                    
#                     # Display the grocery list
#                     st.subheader("Your Grocery List")
#                     for item in response.get('grocery_list', []):
#                         st.write(f"• {item}")
#         else:
#             st.warning("Please enter a recipe")

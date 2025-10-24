import streamlit as st
from my_pages import recipe_assistant_page, grocery_list_page, ingredients_page, favorites_page
import config

st.set_page_config(
    page_title="HomeChef",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.sidebar.title("HomeChef 🍳")
    
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "Ingredients Manager"
    
    # Navigation dropdown
    st.session_state.page = st.sidebar.selectbox(
        "Choose a page",
        ["Ingredients Manager", "Recipe Assistant", "Grocery List", "Favorites"],
        index=["Ingredients Manager", "Recipe Assistant", "Grocery List", "Favorites"].index(st.session_state.page)
    )
    
    # Page routing
    if st.session_state.page == "Ingredients Manager":
        ingredients_page.show()
    elif st.session_state.page == "Recipe Assistant":
        recipe_assistant_page.show()
    elif st.session_state.page == "Grocery List":
        grocery_list_page.show()
    elif st.session_state.page == "Favorites":
        favorites_page.show()

if __name__ == "__main__":
    main()

# import streamlit as st
# from pages import recipe_assistant_page, grocery_list_page, ingredients_page, favorites_page
# import config

# st.set_page_config(
#     page_title="HomeChef",
#     page_icon="🍳",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# def main():
#     st.sidebar.title("HomeChef 🍳")
    
#     # Initialize session state
#     if 'page' not in st.session_state:
#         st.session_state.page = "Ingredients Manager"
    
#     # Navigation
#     st.session_state.page = st.sidebar.selectbox(
#         "Choose a page",
#         ["Ingredients Manager", "Recipe Assistant", "Grocery List", "Favorites"],
#         index=["Ingredients Manager", "Recipe Assistant", "Grocery List", "Favorites"].index(st.session_state.page)
#     )
    
#     # Page routing
#     if st.session_state.page == "Ingredients Manager":
#         ingredients_page.show()
#     elif st.session_state.page == "Recipe Assistant":
#         recipe_assistant_page.show()
#     elif st.session_state.page == "Grocery List":
#         grocery_list_page.show()
#     elif st.session_state.page == "Favorites":
#         favorites_page.show()

# if __name__ == "__main__":
#     main()

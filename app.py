from pages.home import render_home
from pages.create_quiz import render_create_quiz
from pages.flash_cards import render_flash_cards
from pages.settings import render_settings
from pages.about import render_about

import streamlit as st
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide"
) 
# Define pages in order
PAGES = ["Home", "Create Quiz", "Flash Cards", "Settings", "About"]

# Initialize session state for current page
if "current_page" not in st.session_state:
    st.session_state.current_page = 0


def get_current_page_index():
    """Get the current page index from session state."""
    return st.session_state.current_page






# Page render functions mapping
PAGE_RENDERERS = {
    0: "render_home",
    1: "render_create_quiz",
    2: "render_flash_cards",
    3: "render_settings",
    4: "render_about",
}


def main():
    """Main function to render the application."""
    with st.sidebar:
        current_page_index = get_current_page_index()
        
        for i, page in enumerate(PAGES):
            is_current = (i == current_page_index)
            
            if is_current:
                st.button(f"{page}", key=f"nav_{page}_current", use_container_width=True)
            else:
                if st.button(page, key=f"nav_{page}", use_container_width=True):
                    st.session_state.current_page = i
                    st.rerun()
        
        st.divider()
        st.caption("v1.0.0")
    
    # Render the current page content using function mapping
    page_index = get_current_page_index()
    render_functions = {
        0: render_home,
        1: render_create_quiz,
        2: render_flash_cards,
        3: render_settings,
        4: render_about,
    }
    
    if page_index in render_functions:
        render_functions[page_index]()
    
    # Render navigation buttons at the bottom
    st.markdown("---")


if __name__ == "__main__":
    main()

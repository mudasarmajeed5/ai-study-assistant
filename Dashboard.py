import streamlit as st
from helpers.db import get_all_summaries, get_summary_by_id, init_db

init_db()

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎓 AI Study Assistant")
st.markdown("---")
st.markdown("### 📚 Select a Summary")

summaries = get_all_summaries()
if not summaries:
    st.info("No saved summaries yet. Go to Home and create one!")
else:
    summary_dict = {title: sid for sid, title in summaries}
    selected = st.session_state.get("selected_summary_title")
    
    # Display summary cards in 3 columns
    cols = st.columns(3)
    for idx, title in enumerate(summary_dict.keys()):
        with cols[idx % 3].container(border=True):
            # Show selected status
            if title == selected:
                st.markdown(f"✅ **{title}** (Selected)")
                button_label = "🔄 Switch"
            else:
                st.markdown(f"📖 {title}")
                button_label = "Select"
            
            # Handle card click
            if st.button(button_label, key=f"card_{idx}", use_container_width=True):
                summary_id = summary_dict[title]
                content = get_summary_by_id(summary_id)
                st.session_state["selected_summary"] = content
                st.session_state["selected_summary_title"] = title
                st.session_state["selected_summary_id"] = summary_id
                st.rerun()

import streamlit as st

def handle_item_removal(category, name):
    if category in st.session_state.save_file:
        updated_category = st.session_state.save_file[category].copy()
        updated_category.pop(name, None)
        st.session_state.save_file[category] = updated_category
        st.rerun()
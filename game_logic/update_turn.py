import streamlit as st

def update_turn():
    updated_save = st.session_state.save_file.copy()
    updated_save['turn'] += 1
    st.session_state.save_file = updated_save
    st.rerun()
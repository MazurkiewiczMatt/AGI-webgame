import streamlit as st
import json

def main_menu():
    st.title("AGI Wargame")

    col1, col2 = st.columns(2)

    with col1:
        st.write("""
    #### ⚔️ Enter the War Room ⚔️
    You are invited to take command of an organization in pursuit of the first **general superintelligence**.  
    Rival powers hunt for the same godlike spark…  
    Will you seize the future before it devours us all?
    """)

    with col2:
        if st.button("New Game"):
            st.session_state.router = "new_game"
            st.rerun()

        file = st.file_uploader("Load Game:", type="json")
        if file is not None:
            try:
                data = json.loads(file.read())
                st.session_state.save_file = data
                st.session_state.router = "main_game"
                st.rerun()
            except Exception as e:
                st.error(f"Error loading file: {e}")
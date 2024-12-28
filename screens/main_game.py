import streamlit as st
import json

from .inventory import employees_expander,compute_expander,assets_expander, datasets_expander
from game_logic import update_turn

def main_game():
    header()
    overview()
    col1, col2 = st.columns([2, 1])
    with col1:
        compute_expander()
        employees_expander()
        datasets_expander()
        assets_expander()

def header():
    with st.container():
        col1, col2, col3 = st.columns([4, 1, 1])
        with col1:
            st.markdown(f"### {st.session_state.save_file['username']} Dashboard")
        with col2:
            json_data = json.dumps(st.session_state.save_file, indent=2)
            st.download_button(
                label="Save Game",
                data=json_data,
                file_name="save_file.json",
                mime="application/json"
            )
        with col3:
            if st.button("Logout"):
                st.session_state.save_file = None
                st.rerun()

def overview():
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            turn = st.session_state.save_file['turn']
            st.write(f"Y{1+turn//4}Q{1+turn%4} (Turn {1+turn})")
        with col2:
            if st.button("Next turn"):
                update_turn()
        with col3:
            st.write(
                f"**USD:** {st.session_state.save_file.get('USD', 0)}"
            )
        with col4:
            st.write(
                f"**BTC:** {st.session_state.save_file.get('BTC', 0)}"
            )


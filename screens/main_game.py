import streamlit as st
import json

from .inventory import employees_expander, compute_expander, assets_expander, datasets_expander, exchange_gui
from game_logic import update_turn

def main_game():
    header()
    overview()
    col1, col2 = st.columns([2, 1])
    with col1:
        with st.container(border=True):
            usd_per_pflops = st.session_state.save_file['world_state'].get('USD_per_PFLOPs', 2_000)
            st.write(f"**Electricity Cost (USD per PFLOPs):** ${usd_per_pflops:,}")

        exchange_gui()

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
            usd = f"{st.session_state.save_file.get('USD', 0):,.2f}"
            st.write(f"**USD:** ${usd}")
        with col4:
            btc = f"{st.session_state.save_file.get('BTC', 0):,.4f}"
            st.write(f"**BTC:** {btc}")
        if turn > 0:
            with st.container(border=True):
                st.markdown(st.session_state.save_file.get('update_log')[turn])
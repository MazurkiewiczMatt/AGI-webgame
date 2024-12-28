import streamlit as st

def handle_item_removal(category, name):
    if category in st.session_state.save_file:
        updated_category = st.session_state.save_file[category].copy()
        updated_category.pop(name, None)
        st.session_state.save_file[category] = updated_category
        st.rerun()


def convert_currency(amount, from_currency, to_currency):
    updated_save = st.session_state.save_file.copy()
    if from_currency == "USD" and to_currency == "BTC":
        rate = updated_save['world_state'].get('USD_to_BTC', 100_000)
        if updated_save.get('USD', 0) >= amount:
            updated_save['USD'] -= amount
            updated_save['BTC'] += amount / rate
    elif from_currency == "BTC" and to_currency == "USD":
        rate = updated_save['world_state'].get('USD_to_BTC', 100_000)
        if updated_save.get('BTC', 0) >= amount:
            updated_save['BTC'] -= amount
            updated_save['USD'] += amount * rate
    st.session_state.save_file = updated_save
    st.rerun()
import streamlit as st

from game_logic import create_save_file

def new_game():
    st.title("New Game")
    username = st.text_input("The name of your organization:")

    org_types = {
        "University": "**Recommended for new players.** You start the game as a director of a research lab at a university, with steady quarterly funding and good starting expertise.",
        "Private venture": "**Challenging yet rewarding.** You begin as a private venture, with high starting investments and ambitious growth potential.",
        "DarkWeb cell": "**High risk, high reward.** Starting with bitcoin reserves, you gain unique options in the black market."
    }

    with st.container(border=True):
        col1, col2 = st.columns([1, 3])
        with col1:
            org_type = st.radio("Starting point:", org_types.keys())
        with col2:
            st.markdown(org_types[org_type])

    archetypes = {
        "The Maker": "As an engineer of tangible things, you start the game with **20 robotics data points**.",
        "The ASCII Artist": "The alphabet is your canvas. You start the game with **20 text data points**.",
        "The Producer": "You're crafting compelling visual narratives. You start the game with **20 video data points**.",
        "The Superuser": "Excelling in computation, you start the game with **double the initial PFLOPs budget**.",
        "The Hedonist": "Your thirst knows no limit. You start the game with **40 video data points (porn)**."
    }

    with st.container(border=True):
        col1, col2 = st.columns([1, 3])
        with col1:
            archetype = st.radio("Archetype:", archetypes.keys())
        with col2:
            st.markdown(archetypes[archetype])

    is_form_filled = username.strip() != "" and org_type is not None and archetype is not None

    if st.button("Start Game", disabled=not is_form_filled):
        st.session_state.save_file = create_save_file(username, org_type, archetype)
        st.session_state.router = "main_game"
        st.rerun()

    if not is_form_filled:
        st.write("*(Complete the form to proceed).*")

import streamlit as st

from screens import main_menu, new_game, main_game

if "router" not in st.session_state:
    st.session_state.router = "main_menu"

def main():
    if "save_file" not in st.session_state or st.session_state.save_file is None:
        if st.session_state.router not in ("main_menu", "new_game"):
            st.session_state.router = "main_menu"
            st.rerun()

    # Router
    if st.session_state.router == "main_menu":
        main_menu()
    elif st.session_state.router == "new_game":
        new_game()
    elif st.session_state.router == "main_game":
        main_game()
    else:
        # Fallback
        st.warning("Page not found.")
        if "save_file" not in st.session_state or st.session_state.save_file is None:
            if st.button("Back to main menu"):
                st.session_state.router = "main_menu"
                st.rerun()
        else:
            if st.button("Back to game"):
                st.session_state.router = "main_game"
                st.rerun()

if __name__ == "__main__":
    main()

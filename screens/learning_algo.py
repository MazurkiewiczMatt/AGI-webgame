import streamlit as st
from game_logic import commence_development



def learning_algo():
    save_file = st.session_state.save_file
    employees = save_file.get('employees', {})

    # Initialize selected in session state if not already present
    if 'selected' not in st.session_state:
        st.session_state.selected = {employee: False for employee in employees}

    # Filter out employees who are already allocated
    available_employees = {e: details for e, details in employees.items() if not details.get('allocated')}

    expertises = {employee: employees[employee]['parameters'].get('expertise', 0) for employee in available_employees}

    with st.container(border=True):
        algo_name = st.text_input("Name your learning algorithm:")
        modalities = st.slider("Modalities", min_value=1, max_value=5, value=2)

        # Calculate total expertise based on selected employees
        total_expertise = sum(
            [expertises[employee] for employee in st.session_state.selected if st.session_state.selected[employee]]
        )
        st.write(f"Total expertise: {total_expertise}")
        st.write(f"Multiplier: {total_expertise} * d{6 - modalities}")
        st.divider()
        st.write("Expertise allocation:")

        if available_employees:
            for employee, details in available_employees.items():
                with st.container(border=True):
                    col1, col2 = st.columns([1, 5])
                    with col1:
                        # Use the session state to store checkbox values
                        if st.checkbox(
                            "Allocate",
                            value=st.session_state.selected.get(employee, False),
                            key=f"allocate_{employee}",
                        ):
                            if not st.session_state.selected[employee]:
                                st.session_state.selected[employee] = True
                                st.rerun()
                        else:
                            if st.session_state.selected[employee]:
                                st.session_state.selected[employee] = False
                                st.rerun()
                    with col2:
                        st.write(f"**{details.get('name', employee)}**")
                        parameters = details.get('parameters', {})
                        expertise = parameters.get('expertise', 'N/A')
                        price_per_turn = parameters.get('price_per_turn', None)
                        markdown_text = f"*{details.get('description', 'No description available.')}*"
                        if price_per_turn:
                            markdown_text += f"  \nPrice per Turn: {price_per_turn}"
                        markdown_text += f"  \nExpertise: {expertise}"
                        st.markdown(markdown_text)
        else:
            st.write("No employees available.")

    # Commence development button only appears if total expertise > 0
    if total_expertise > 0 and algo_name.strip() != "":
        if st.button("Commence Development"):
            commence_development(algo_name, modalities, employees, st.session_state.selected, save_file)

    if st.button("Back to game"):
        st.session_state.router = "main_game"
        st.rerun()

import uuid  # For generating unique task identifiers
import streamlit as st

def commence_development(algo_name, modalities, employees, selected, save_file):
    """
    Handles the logic for commencing development.
    Adds a task to save_file['tasks'] and updates employee allocation status.
    """
    # Generate a unique task ID
    task_id = str(uuid.uuid4())
    current_turn = save_file.get("turn", 0)  # Get the current turn

    # Calculate total expertise of selected employees
    total_expertise = sum(
        employees[employee]['parameters'].get('expertise', 0)
        for employee in selected if selected[employee]
    )

    # Add task to save_file['tasks']
    save_file['tasks'][task_id] = {
        "name": algo_name,
        "type": "learning_algo",
        "modalities": modalities,
        "total_expertise": total_expertise,
        "employees": [employee for employee in selected if selected[employee]],
        "start_turn": current_turn,
        "end_turn": current_turn + 1,  # End turn is current turn + 1
    }

    # Mark selected employees as allocated with the task ID
    for employee in selected:
        if selected[employee]:
            save_file['employees'][employee]['allocated'] = task_id

    # Reset selection and navigate back to the main game
    st.session_state.selected = {employee: False for employee in employees}
    st.session_state.router = "main_game"
    st.rerun()
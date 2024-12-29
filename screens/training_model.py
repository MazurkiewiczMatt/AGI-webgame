import streamlit as st
import uuid  # For generating unique task identifiers


def training_model():
    """
    Menu for starting the training of an AI model.
    Allows the user to select one learning algorithm, modalities, datasets, and compute resources.
    """

    save_file = st.session_state.save_file

    st.markdown("### Train an AI Model")
    if st.button("Back to game"):
        st.session_state.router = "main_game"
        st.rerun()

    # Retrieve available learning algorithms, datasets, and compute resources
    learning_algos = {
        task_id: details
        for task_id, details in save_file.get('assets', {}).items()
        if details['type'] == 'learning_algo'
    }
    datasets = save_file.get('datasets', {})
    compute_resources = {
        compute_id: details
        for compute_id, details in save_file.get('compute', {}).items()
        if not details.get('allocated')
    }

    if not learning_algos:
        st.warning("No learning algorithms available. Develop one before training an AI model.")
        return

    if not compute_resources:
        st.warning("No available compute resources. Free some up or acquire new ones.")
        return

    model_name = st.text_input("Name your AI model:")

    if model_name == "":
        st.warning("Please enter a name for the AI model.")
        return

    # Select a learning algorithm
    algo_id = st.selectbox(
        "Select a learning algorithm:",
        options=list(learning_algos.keys()),
        format_func=lambda x: learning_algos[x]['name']
    )

    if not algo_id:
        st.warning("Please select a learning algorithm.")
        return

    algo_details = learning_algos[algo_id]
    max_modalities = algo_details['parameters']['modalities']

    # Select modalities
    selected_modalities = st.multiselect(
        "Select modalities:",
        options=["text", "video", "robotics"],
        default=[],
        max_selections=max_modalities
    )

    if not selected_modalities:
        st.warning("Select at least one modality.")
        return

    # Filter datasets by selected modalities
    available_datasets = {
        dataset_id: details
        for dataset_id, details in datasets.items()
        if any(modality in details['parameters'] for modality in selected_modalities)
    }

    selected_datasets = st.multiselect(
        "Select datasets:",
        options=list(available_datasets.keys()),
        format_func=lambda x: available_datasets[x]['name']
    )

    if not selected_datasets:
        st.warning("Select at least one dataset.")
        return

    # Select compute resource
    compute_id = st.multiselect(
        "Select compute resource:",
        options=list(compute_resources.keys()),
        format_func=lambda x: compute_resources[x]['name']
    )

    if compute_id == []:
        st.warning("Please select a compute resource.")
        return

    # Select training duration
    training_duration = st.number_input(
        "Training duration (turns):",
        min_value=1,
        max_value=10,
        value=2
    )

    # Confirm and add the task
    if st.button("Start Training"):
        task_id = str(uuid.uuid4())
        current_turn = save_file.get("turn", 0)

        # Add the training task to save_file['tasks']
        save_file['tasks'][task_id] = {
            "name": f"{model_name}",
            "type": "training",
            "learning_algo": algo_id,
            "modalities": selected_modalities,
            "datasets": selected_datasets,
            "compute": compute_id,
            "start_turn": current_turn,
            "end_turn": current_turn + training_duration,  # Example duration of 2 turns
            "AI_expertise": save_file.get("AI_expertise", 0),
            "duration": training_duration,
        }

        # Mark compute resource as allocated
        for compute_id_elements in compute_id:
            save_file['compute'][compute_id_elements]['allocated'] = task_id

        st.success("Training task started successfully!")
        st.session_state.router = "main_game"
        st.rerun()


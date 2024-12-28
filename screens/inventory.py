import streamlit as st

from game_logic import handle_item_removal


def display_employee(name, details, button_text=None, button_action=None):
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{details.get('name', name)}**")
        with col2:
            if button_text and button_action:
                if st.button(button_text, key=f"employee_{name}"):
                    button_action('employees', name)
        parameters = details.get('parameters', {})
        expertise = parameters.get('expertise', 'N/A')
        price_per_turn = parameters.get('price_per_turn', None)
        markdown_text = f"*{details.get('description', 'No description available.')}*"
        if price_per_turn:
            markdown_text += f"  \nPrice per Turn: {price_per_turn}"
        markdown_text += f"  \nExpertise: {expertise}"
        st.markdown(markdown_text)


def display_asset(name, details, button_text=None, button_action=None):
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{details.get('name', name)}**")
        with col2:
            if button_text and button_action:
                if st.button(button_text, key=f"asset_{name}"):
                    button_action('assets', name)
        parameters = details.get('parameters', {})
        price_per_turn = parameters.get('price_per_turn', None)
        markdown_text = f"*{details.get('description', 'No description available.')}*"
        if price_per_turn:
            markdown_text += f"  \nPrice per Turn: {price_per_turn}"
        st.markdown(markdown_text)


def display_compute(name, details, button_text=None, button_action=None):
    with st.container(border=True):
        col1, col2 = st.columns([3, 2])
        with col1:
            st.write(f"**{details.get('name', name)}**")
        with col2:
            if button_text and button_action:
                if st.button(button_text, key=f"compute_{name}"):
                    button_action('compute', name)
        parameters = details.get('parameters', {})
        pflops = parameters.get('PFLOPs', 'N/A')
        price_per_turn = parameters.get('price_per_turn', None)
        markdown_text = f"*{details.get('description', 'No description available.')}*"
        if price_per_turn:
            markdown_text += f"  \nPrice per Turn: {price_per_turn}"
        markdown_text += f"  \nPFLOPs: {pflops}"
        st.markdown(markdown_text)


def display_dataset(name, details, button_text=None, button_action=None):
    modalities = {
        "robotics": "Robotics",
        "text": "Text",
        "video": "Video"
    }

    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        parameters = details.get('parameters', {})
        with col1:
            tags = parameters.get('tags', [])
            if "porn" not in tags:
                st.write(f"**{details.get('name', name)}**")
            else:
                st.write(f"**(18+) {details.get('name', name)}**")
        with col2:
            if button_text and button_action:
                if st.button(button_text, key=f"dataset_{name}"):
                    button_action('datasets', name)
        price_per_turn = parameters.get('price_per_turn', None)
        markdown_text = f"*{details.get('description', 'No description available.')}*"
        if price_per_turn:
            markdown_text += f"  \nPrice per Turn: {price_per_turn}"

        for key, value in modalities.items():
            if key in parameters:
                markdown_text += f"  \n{value}: {parameters[key]}"

        st.markdown(markdown_text)



def employees_expander():
    with st.expander("Employees"):
        employees = st.session_state.save_file.get('employees', {})
        if employees:
            for employee, details in list(employees.items()):
                display_employee(employee, details, "Fire", handle_item_removal)
        else:
            st.write("No employees yet.")


def assets_expander():
    with st.expander("Assets"):
        assets = st.session_state.save_file.get('assets', {})
        if assets:
            for asset, details in list(assets.items()):
                display_asset(asset, details, "Discard", handle_item_removal)
        else:
            st.write("No assets yet.")


def compute_expander():
    with st.expander("Compute Resources"):
        compute = st.session_state.save_file.get('compute', {})
        if compute:
            for resource, details in list(compute.items()):
                display_compute(resource, details, "Decommission", handle_item_removal)
        else:
            st.write("No compute resources yet.")


def datasets_expander():
    with st.expander("Datasets"):
        datasets = st.session_state.save_file.get('datasets', {})
        if datasets:
            for dataset, details in list(datasets.items()):
                display_dataset(dataset, details, "Delete", handle_item_removal)
        else:
            st.write("No datasets yet.")

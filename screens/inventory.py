import streamlit as st

def display_employee(name, details, button_text=None, button_action=None):
    with st.container(border=True):
        st.write(f"**{details.get('name', name)}:** {details.get('description', 'No description available.')} | Expertise: {details.get('parameters', {}).get('expertise', 'N/A')} | Cost per Turn: {details.get('parameters', {}).get('price_per_turn', 'N/A')}")
        if button_text and button_action:
            if st.button(button_text, key=f"employee_{name}"):
                button_action(name)

def display_asset(name, details, button_text=None, button_action=None):
    with st.container(border=True):
        st.write(f"**{details.get('name', name)}:** {details.get('description', 'No description available.')} | Type: {details.get('type', 'Unknown type')} | Cost per Turn: {details.get('parameters', {}).get('price_per_turn', 'N/A')}")
        if button_text and button_action:
            if st.button(button_text, key=f"asset_{name}"):
                button_action(name)

def display_compute(name, details, button_text=None, button_action=None):
    with st.container(border=True):
        st.write(f"**{details.get('name', name)}:** {details.get('description', 'No description available.')} | PFLOPs: {details.get('parameters', {}).get('PFLOPs', 'N/A')}")
        if button_text and button_action:
            if st.button(button_text, key=f"compute_{name}"):
                button_action(name)

def handle_item_removal(category, name):
    if category in st.session_state.save_file:
        updated_category = st.session_state.save_file[category].copy()
        updated_category.pop(name, None)
        st.session_state.save_file[category] = updated_category
        st.rerun()

def employees_expander():
    with st.expander("Employees"):
        employees = st.session_state.save_file.get('employees', {})
        if employees:
            for employee, details in list(employees.items()):
                display_employee(employee, details, "Remove", lambda name: handle_item_removal('employees', name))
        else:
            st.write("No employees yet.")

def assets_expander():
    with st.expander("Assets"):
        assets = st.session_state.save_file.get('assets', {})
        if assets:
            for asset, details in list(assets.items()):
                display_asset(asset, details, "Remove", lambda name: handle_item_removal('assets', name))
        else:
            st.write("No assets yet.")

def compute_expander():
    with st.expander("Compute Resources"):
        compute = st.session_state.save_file.get('compute', {})
        if compute:
            for resource, details in list(compute.items()):
                display_compute(resource, details, "Remove", lambda name: handle_item_removal('compute', name))
        else:
            st.write("No compute resources yet.")

# The functions above define the expanders and are not invoked directly in this file.

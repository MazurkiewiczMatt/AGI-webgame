import streamlit as st

def update_turn():
    updated_save = st.session_state.save_file.copy()

    # Increment the turn counter
    updated_save['turn'] += 1

    # Calculate changes in USD
    usd_change = 0
    breakdown = {"funding": 0, "employees": 0, "other": 0}

    # Update funding effects on USD
    for asset_key, asset in updated_save.get('assets', {}).items():
        if asset.get('type') == 'funding' and 'price_per_turn' in asset['parameters']:
            change = -asset['parameters']['price_per_turn']  # Negate to interpret correctly
            usd_change += change
            breakdown["funding"] += change
        elif 'price_per_turn' in asset['parameters']:
            change = -asset['parameters']['price_per_turn']  # Negate to interpret correctly
            usd_change += change
            breakdown["other"] += change

    # Update employee costs on USD
    for employee_key, employee in updated_save.get('employees', {}).items():
        if 'price_per_turn' in employee['parameters']:
            change = -employee['parameters']['price_per_turn']  # Negate to interpret correctly
            usd_change += change
            breakdown["employees"] += change

    # Apply USD changes to the save file
    updated_save['USD'] += usd_change

    # Create a log entry for this turn
    log_entry = (f"**Turn {updated_save['turn']}:**  \n"
                 f"USD Change: **{usd_change}** "
                 f"(Funding: {breakdown['funding']}, Employees: {breakdown['employees']}, Other: {breakdown['other']})")

    # Append to the update log
    updated_save['update_log'][updated_save['turn']] = log_entry

    # Save the updated state and rerun
    st.session_state.save_file = updated_save
    st.rerun()

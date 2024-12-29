import streamlit as st
import random

def update_turn():
    updated_save = st.session_state.save_file.copy()

    updated_save['turn'] += 1

    usd_change = 0
    breakdown = {"funding": 0, "employees": 0, "compute": 0, "other": 0}

    for asset_key, asset in updated_save.get('assets', {}).items():
        if asset.get('type') == 'funding' and 'price_per_turn' in asset['parameters']:
            change = -asset['parameters']['price_per_turn']
            usd_change += change
            breakdown["funding"] += change
        elif 'price_per_turn' in asset['parameters']:
            change = -asset['parameters']['price_per_turn']
            usd_change += change
            breakdown["other"] += change

    for employee_key, employee in updated_save.get('employees', {}).items():
        if 'price_per_turn' in employee['parameters']:
            change = -employee['parameters']['price_per_turn']
            usd_change += change
            breakdown["employees"] += change

    for compute_key, compute in updated_save.get('compute', {}).items():
        compute_cost = 0
        if 'price_per_turn' in compute['parameters']:
            compute_cost += -compute['parameters']['price_per_turn']
        if 'PFLOPs' in compute['parameters']:
            compute_cost += -(compute['parameters']['PFLOPs'] * updated_save['world_state']['USD_per_PFLOPs'])
        usd_change += compute_cost
        breakdown["compute"] += compute_cost

    updated_save['USD'] += usd_change

    updated_save['world_state']['USD_per_PFLOPs'] = int(updated_save['world_state']['USD_per_PFLOPs'] * (1 + random.uniform(-0.01, 0.01)))

    btc_change_factor = random.uniform(-0.05, 0.06)
    updated_save['world_state']['USD_to_BTC'] = int(updated_save['world_state']['USD_to_BTC'] * (1 + btc_change_factor))

    log_entry = (f"**Turn {updated_save['turn']}**  \n"
                 f"Cashflow: $**{usd_change:,.2f}** "
                 f"(Funding: {breakdown['funding']}, Employees: {breakdown['employees']}, Compute: {breakdown['compute']}, Other: {breakdown['other']})")

    if abs(btc_change_factor) > 0.04:
        percentage_change = round(btc_change_factor * 100, 2)
        log_entry += f"  \nBitcoin exchange rate changed by {percentage_change}%"

    finished_tasks = []
    if st.session_state.save_file['tasks']:
        for task_id, task in st.session_state.save_file['tasks'].items():
            if task['end_turn'] == st.session_state.save_file['turn']+1:
                if task['type'] == "learning_algo":
                    name = task['name']
                    modalities = task['modalities']
                    multiplier = task['total_expertise'] * random.randint(1,6-modalities)
                    updated_save['assets'][task_id] = {
                        'name': name,
                        'description': f"Learning algorithm with {multiplier}x multiplier and {modalities} modalities.",
                        'type': 'learning_algo',
                        'parameters': {
                            'multiplier': multiplier,
                            'modalities': modalities,
                        },
                    }
                    log_entry += f"  \nFinished developing learning algorithm **{name}** ({multiplier}x, {modalities} modalities)"
                    for employee in updated_save['employees']:
                        if 'allocated' in updated_save['employees'][employee] and updated_save['employees'][employee]['allocated']==task_id:
                            updated_save['employees'][employee].pop('allocated', None)

                finished_tasks.append(task_id)

    for finished_task in finished_tasks:
        updated_save['tasks'].pop(finished_task, None)


    updated_save['update_log'][updated_save['turn']] = log_entry

    st.session_state.save_file = updated_save
    st.rerun()

import streamlit as st
import random

def update_turn():
    updated_save = st.session_state.save_file.copy()

    updated_save['turn'] += 1

    usd_change = 0
    breakdown = {"funding": 0, "employees": 0, "compute": 0, "other": 0}

    if updated_save["deployed_model"] not in updated_save["models"].keys():
        updated_save["deployed_model"] = None

    for asset_key, asset in updated_save.get('assets', {}).items():
        if asset.get('type') == 'funding' and 'price_per_turn' in asset['parameters']:
            change = -asset['parameters']['price_per_turn']
            usd_change += change
            breakdown["funding"] += change
        elif 'price_per_turn' in asset['parameters']:
            change = -asset['parameters']['price_per_turn']
            usd_change += change
            breakdown["other"] += change

    expertise_change = 0

    for employee_key, employee in updated_save.get('employees', {}).items():
        if 'price_per_turn' in employee['parameters']:
            change = -employee['parameters']['price_per_turn']
            usd_change += change
            breakdown["employees"] += change
        if employee.get('allocated', None) is None:
            expertise_change += employee['parameters']['expertise']

    for compute_key, compute in updated_save.get('compute', {}).items():
        compute_cost = 0
        if 'price_per_turn' in compute['parameters']:
            compute_cost += -compute['parameters']['price_per_turn']
        if 'PFLOPs' in compute['parameters']:
            if ('allocated' in compute and compute['allocated'] is not None):
                compute_cost += -(compute['parameters']['PFLOPs'] * updated_save['world_state']['USD_per_PFLOPs'])
        usd_change += compute_cost
        breakdown["compute"] += compute_cost

    updated_save['USD'] += usd_change

    updated_save['world_state']['USD_per_PFLOPs'] = int(updated_save['world_state']['USD_per_PFLOPs'] * (1 + random.uniform(-0.01, 0.01)))

    btc_change_factor = random.uniform(-0.05, 0.06)
    updated_save['world_state']['USD_to_BTC'] = int(updated_save['world_state']['USD_to_BTC'] * (1 + btc_change_factor))

    log_entry = (f"**Turn {updated_save['turn']}**  \n"
                 f"Cashflow: \$**{usd_change:,.2f}** "
                 f"(Funding: {breakdown['funding']}, Employees: {breakdown['employees']}, Compute: {breakdown['compute']}, Other: {breakdown['other']})")

    if updated_save["deployed_model"] is not None:
        capabilities = updated_save["models"][updated_save["deployed_model"]]["capabilities"]
        name = updated_save["models"][updated_save["deployed_model"]]["name"]
        no_cap = len(capabilities)
        earned = no_cap**3 * 5000
        updated_save['USD'] += earned
        log_entry += f"  \nDeployed model **{name}** ({no_cap} capabilities) earned \$**{earned:,.2f}** ( \${usd_change+earned:,.2f} total change)"
    if abs(btc_change_factor) > 0.04:
        percentage_change = round(btc_change_factor * 100, 2)
        log_entry += f"  \nBitcoin exchange rate changed by {percentage_change}%"

    if expertise_change > 0:
        updated_save['AI_expertise'] += expertise_change
        log_entry += f"  \nIdle researchers produced {expertise_change:,} knowledge."

    finished_tasks = []
    if updated_save['tasks']:
        for task_id, task in updated_save['tasks'].items():
            if task['end_turn'] == updated_save['turn']:
                if task['type'] == "learning_algo":
                    name = task['name']
                    modalities = task['modalities']
                    multiplier = task['total_expertise'] * random.randint(1,6-modalities)
                    updated_save['assets'][task_id] = {
                        'name': name,
                        'description': f"Learning algorithm developed at {updated_save['username']}.",
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
                elif task['type'] == "training":
                    training_name = task.get("name")
                    training_learning_algo = task.get("learning_algo")
                    training_multiplier = updated_save["assets"][training_learning_algo]["parameters"]['multiplier']
                    training_modalities = task.get("modalities")
                    training_datasets = task.get("datasets")
                    training_compute = task.get("compute")
                    training_AI_expertise = task.get("AI_expertise")
                    training_duration = task.get("duration")

                    capabilities = []

                    compute_total = 0
                    for compute in training_compute:
                        compute_total += updated_save["compute"][compute]["parameters"]["PFLOPs"]

                    log_entry += f"  \nFinished training {training_name}, using {compute_total:,} PFLOPs over {training_duration:,} turns."

                    for modality in training_modalities:
                        modality_datapoints = 0
                        for dataset in training_datasets:
                            if modality in updated_save["datasets"][dataset]["parameters"]:
                                modality_datapoints += updated_save["datasets"][dataset]["parameters"][modality]
                        modality_total = modality_datapoints*training_AI_expertise*training_duration*training_multiplier
                        log_entry += f"  \nWith {modality_datapoints} data points in {modality}, it got score of {modality_total:,} in that domain."
                        if modality == "text":
                            if modality_total > 10**3:
                                capabilities.append("Sentiment analysis")
                            if modality_total > 10**6:
                                capabilities.append("Correct syntax")
                            if modality_total > 10**9:
                                capabilities.append("Context awareness")
                            if modality_total > 10**12:
                                capabilities.append("Programming")
                        elif modality == "video":
                            if modality_total > 10**3:
                                capabilities.append("Semantic segmentation")
                            if modality_total > 10**6:
                                capabilities.append("Image generation")
                            if modality_total > 10**9:
                                capabilities.append("Temporal coherence")
                            if modality_total > 10**12:
                                capabilities.append("Short form content")
                        elif modality == "robotics":
                            if modality_total > 10**3:
                                capabilities.append("Position estimation")
                            if modality_total > 10**6:
                                capabilities.append("Basic robot arm control")
                            if modality_total > 10**9:
                                capabilities.append("Quadruped basic motion")
                            if modality_total > 10**12:
                                capabilities.append("Autonomous operation")


                    updated_save['models'][task_id] = {
                        'name': training_name,
                        'capabilities': capabilities,
                    }

                    for compute in updated_save['compute']:
                        if 'allocated' in updated_save['compute'][compute] and updated_save['compute'][compute]['allocated']==task_id:
                            updated_save['compute'][compute].pop('allocated', None)
                finished_tasks.append(task_id)

        for finished_task in finished_tasks:
            updated_save['tasks'].pop(finished_task, None)


    updated_save['update_log'][updated_save['turn']] = log_entry

    st.session_state.save_file = updated_save
    st.rerun()

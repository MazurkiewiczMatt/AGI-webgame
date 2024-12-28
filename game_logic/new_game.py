def create_save_file(username, org_type, archetype):
    org_types = {
        "University": {
            "USD": 500_000,
            "compute": {
                "university_supercomputer": {
                    "name": "University Supercomputer",
                    "description": "Handles extensive calculations for research",
                    "type": "compute",
                    "parameters": {"PFLOPs": 20}
                }
            },
            "assets": {
                "university_funding": {
                    "name": "University Funding",
                    "description": "Financial support for the organization",
                    "type": "funding",
                    "parameters": {"price_per_turn": -300_000}
                }
            },
            "employees": {
                "grad_students": {
                    "name": "Grad Students",
                    "description": "Talented researchers working on ML projects",
                    "type": "researcher",
                    "parameters": {"expertise": 100, "price_per_turn": 125_000}
                }
            }
        },
        "Private venture": {
            "USD": 3_000_000,
            "compute": {
                "h100_cluster": {
                    "name": "H100 Cluster",
                    "description": "High-performance computing setup",
                    "type": "compute",
                    "parameters": {"PFLOPs": 20}
                }
            },
            "employees": {
                "early_employees": {
                    "name": "Early Employees",
                    "description": "Initial ML researchers",
                    "type": "researcher",
                    "parameters": {"expertise": 50, "price_per_turn": 125_000}
                }
            }
        },
        "DarkWeb cell": {
            "USD": 10_000,
            "BTC": 20,
            "compute": {
                "hijacked_crypto_miners": {
                    "name": "Hijacked Crypto Miners",
                    "description": "Compromised systems for computational tasks",
                    "type": "compute",
                    "parameters": {"PFLOPs": 20}
                }
            },
            "assets": {
                "darknet_contacts": {
                    "name": "DarkNet Contacts",
                    "description": "Access to illicit marketplaces and resources",
                    "type": "influence",
                    "parameters": {"effect": "market_access"}
                }
            }
        }
    }

    archetypes = {
        "The Maker": {
            "datasets": {
                "diy_robotics_dataset": {
                    "name": "DIY Robotics Dataset",
                    "description": "Initial dataset for robotics models",
                    "type": "dataset",
                    "parameters": {"robotics": 20}
                }
            }
        },
        "The ASCII Artist": {
            "datasets": {
                "starting_text_dataset": {
                    "name": "Starting Text Dataset",
                    "description": "Initial corpus for training LLMs",
                    "type": "dataset",
                    "parameters": {"text": 20}
                }
            }
        },
        "The Producer": {
            "datasets": {
                "starting_video_dataset": {
                    "name": "Starting Video Dataset",
                    "description": "Collection of videos for multimedia training",
                    "type": "dataset",
                    "parameters": {"video": 20}
                }
            }
        },
        "The Superuser": {
            "compute": {
                "extra_starting_compute": {
                    "name": "Extra Starting Compute",
                    "description": "Boost in initial computational power",
                    "type": "compute",
                    "parameters": {"PFLOPs": 20}
                }
            }
        },
        "The Hedonist": {
            "datasets": {
                "adult_movies_collection": {
                    "name": "Adult Movies Collection",
                    "description": "Extensive collection of mature content",
                    "type": "dataset",
                    "parameters": {"video": 40, "tags": ["porn"]}
                }
            }
        }
    }

    # Initialize an empty save_file
    save_file = {
        "username": username,
        "org_type": org_type,
        "archetype": archetype,
        "USD": 0,
        "BTC": 0,
        "compute": {},
        "assets": {},
        "employees": {},
        "datasets": {},
        "turn": 0,
        "update_log": {},  # key = turn number; value = update message (multiline markdown string)
    }

    # Fetch dictionaries from org_types and archetypes
    org_data = org_types.get(org_type, {})
    archetype_data = archetypes.get(archetype, {})

    # Add up resources from org_data
    save_file["USD"] += org_data.get("USD", 0)
    save_file["BTC"] += org_data.get("BTC", 0)
    save_file["compute"].update(org_data.get("compute", {}))
    save_file["assets"].update(org_data.get("assets", {}))
    save_file["employees"].update(org_data.get("employees", {}))

    # Add up resources from archetype_data
    save_file["datasets"].update(archetype_data.get("datasets", {}))
    if "compute" in archetype_data:
        save_file["compute"].update(archetype_data["compute"])

    return save_file

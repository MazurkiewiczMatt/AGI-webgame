def create_save_file(username, org_type, archetype):
    org_types = {
        "University": {
            "USD": 2_000_000,
            "compute": {
                "University supercomputer": {"PFLOPs": 20}
            },
            "assets": {
                "University funding": {
                    "type": "funding",
                    "price_per_turn": -8_000_000
                }
            },
            "employees": {
                "Grad students": {
                    "expertise": 100,
                    "price_per_turn": 125_000
                }
            }
        },
        "Private venture": {
            "USD": 100_000_000,
            "compute": {
                "H100 cluster": {"PFLOPs": 20}
            },
            "employees": {
                "Early employees": {
                    "expertise": 50,
                    "price_per_turn": 125_000
                }
            }
        },
        "DarkWeb cell": {
            "USD": 100_000,
            "BTC": 100,
            "compute": {
                "Hijacked crypto miners": {"PFLOPs": 20}
            },
            "assets": {
                "DarkNet contacts": {
                    "type": "influence",
                    "description": "More items available on black market."
                }
            }
        }
    }

    archetypes = {
        "The Maker": {
            "datasets": {
                "DIY robotics dataset": {"robotics": 20}
            }
        },
        "The ASCII Artist": {
            "datasets": {
                "Starting text dataset": {"text": 20}
            }
        },
        "The Producer": {
            "datasets": {
                "Starting video dataset": {"video": 20}
            }
        },
        "The Superuser": {
            "compute": {
                "Extra starting compute": {"PFLOPs": 20}
            }
        },
        "The Hedonist": {
            "datasets": {
                "Adult movies collection": {"video": 40, "tags": ["porn"]}
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
        "time_in_game": 0,
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

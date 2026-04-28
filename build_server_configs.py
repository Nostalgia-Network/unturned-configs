#!/usr/bin/env python3

import json
import os

from typing import Dict, Any


########## Variable Definitions ##########

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
CONFIGS_DIR = os.path.join(PROJECT_ROOT, 'Configs')
OVERLAY_DIR = os.path.join(PROJECT_ROOT, 'Overlays')
DEFAULT_CONFIG = os.path.join(CONFIGS_DIR, 'default.json')
NETWORK_BASE_OVERLAY = os.path.join(OVERLAY_DIR, 'network.json')


########## Function Definitions ##########

# Recursively update a dictionary with another dictionary's values, preserving existing keys
def deep_update(base: Dict[str, Any], overlay: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in overlay.items():
        if key in base:
            if isinstance(value, dict) and isinstance(base[key], dict):
                deep_update(base[key], value)
            else:
                # For non-dict values (including lists), replace entirely
                base[key] = value
        else:
            base[key] = value
    return base


########## Main Logic ##########

# Iterate over all overlay files ending in _overlay.json
for filename in os.listdir(OVERLAY_DIR):
    if filename.endswith('_overlay.json'):
        # Extract the server name from the filename (assumes format: servername_overlay.json)
        server_name = filename.replace('_overlay.json', '')

        server_overlay = os.path.join(OVERLAY_DIR, filename)
        target_config = os.path.join(CONFIGS_DIR, f"{server_name}.json")

        # Load the default configuration as the running configuration
        with open(DEFAULT_CONFIG, 'r') as f:
            config_data = json.load(f)

        # Load the network configuration overlay and update the running configuration
        with open(NETWORK_BASE_OVERLAY, 'r') as f:
            network_data = json.load(f)
            deep_update(config_data, network_data)

        # Load the server configuration overlay (if it exists) and update the running configuration again
        if os.path.exists(server_overlay):
            with open(server_overlay, 'r') as f:
                server_data = json.load(f)
                deep_update(config_data, server_data)

        # Delete the existing target configuration if it exists
        if os.path.exists(target_config):
            os.remove(target_config)

        # Write the updated configuration
        with open(target_config, 'w') as f:
            json.dump(config_data, f, indent=4)

        print(f"Finished building server configuration: {target_config}")
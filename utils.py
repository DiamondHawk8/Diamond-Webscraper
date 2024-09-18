# utils.py

import yaml
import logging


def load_config(file_path='config.yaml'):
    """
    Loads configuration settings from the specified YAML file.

    Args:
        file_path (str): The path to the YAML configuration file.

    Returns:
        dict: A dictionary containing the configuration settings.

    Raises:
        FileNotFoundError: If the specified file path does not exist.
        yaml.YAMLError: If there is an issue parsing the YAML file.
    """
    try:
        # Open and read the YAML file
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError as fnf_error:
        logging.error(f"Config file not found: {fnf_error}")
        raise  # Re-raise the error after logging
    except yaml.YAMLError as yaml_error:
        logging.error(f"Error parsing YAML file: {yaml_error}")
        raise  # Re-raise the error after logging

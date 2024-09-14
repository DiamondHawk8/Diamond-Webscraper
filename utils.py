import yaml


def load_config(file_path='config.yaml'):
    """
    Loads configuration settings from the specified YAML file.

    Args:
        file_path (str): The path to the YAML configuration file.

    Returns:
        dict: A dictionary containing the configuration settings.

    Error Handling:
        - Handle file I/O errors (e.g., file not found).
        - Log parsing errors if the YAML file structure is invalid.
    """
    with open(file_path, 'r') as file:
        try:
            config = yaml.safe_load(file)
        except yaml.YAMLError as e:
            # Log error and handle appropriately
            pass  # Replace with error handling
        except FileNotFoundError:
            # Log error and handle appropriately
            pass  # Replace with error handling

    return config

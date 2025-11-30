"""
Configuration loader for Secret Santa application.
Handles loading of yearly topics and character data.
"""
import json
import os
from typing import Dict, List, Any


def load_config() -> Dict[str, Any]:
    """
    Load the main configuration file.
    
    Returns:
        Dictionary containing configuration data (year, topic, characters_file)
    """
    config_path = os.path.join(os.path.dirname(__file__), "../config.json")
    try:
        with open(config_path, "r", encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found at {config_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding configuration JSON: {e}")


def load_characters() -> List[Dict[str, str]]:
    """
    Load characters from the configured characters file.
    
    Returns:
        List of dictionaries containing character data (name, photo_url)
    """
    config = load_config()
    characters_file = config.get("characters_file", "simpsons_characters.json")
    characters_path = os.path.join(os.path.dirname(__file__), characters_file)
    
    try:
        with open(characters_path, "r", encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Characters file not found at {characters_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding characters JSON: {e}")


def get_current_topic() -> str:
    """
    Get the current year's topic name.
    
    Returns:
        String containing the topic name (e.g., "The Simpsons")
    """
    config = load_config()
    return config.get("topic", "Secret Santa")


def get_current_year() -> int:
    """
    Get the current configured year.
    
    Returns:
        Integer representing the year
    """
    config = load_config()
    return config.get("year", 2025)

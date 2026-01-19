import json
from pathlib import Path

def load_preferences(filepath: Path) -> dict:
    """Load saved preferences from JSON file"""
    if not filepath.exists():
        return {}
    
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def save_preferences(filepath: Path, preferences: dict) -> None:
    """Save preferences to JSON file"""
    try:
        with open(filepath, 'w') as f:
            json.dump(preferences, f, indent=2)
    except IOError as e:
        print(f"Warning: Could not save preferences: {e}")
import os
import json
import re
from typing import Dict, List, Any, Union
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CharacterValidationError(Exception):
    """Custom exception for character validation errors."""
    pass

def validate_input(value: str, valid_options: List[str]) -> bool:
    """
    Validate if an input value is in the list of valid options (case-insensitive).
    
    Args:
        value: The input value to validate
        valid_options: List of valid options
    
    Returns:
        bool: True if valid, False otherwise
    """
    return value.strip().title() in [opt.strip().title() for opt in valid_options]

def validate_character_data(character_data: Dict[str, Any]) -> bool:
    """
    Validate character data structure and content.
    
    Args:
        character_data: Dictionary containing character information
    
    Returns:
        bool: True if valid
        
    Raises:
        CharacterValidationError: If validation fails
    """
    required_fields = {
        'name': str,
        'race': str,
        'class': str,
        'alignment': str,
        'stats': dict,
        'background': str
    }

    # Check required fields and their types
    for field, field_type in required_fields.items():
        if field not in character_data:
            raise CharacterValidationError(f"Missing required field: {field}")
        if not isinstance(character_data[field], field_type):
            raise CharacterValidationError(f"Invalid type for {field}: expected {field_type.__name__}")

    # Validate stats
    if 'stats' in character_data:
        required_stats = ['strength', 'dexterity', 'constitution', 
                         'intelligence', 'wisdom', 'charisma']
        for stat in required_stats:
            if stat not in character_data['stats']:
                raise CharacterValidationError(f"Missing stat: {stat}")
            if not (3 <= character_data['stats'][stat] <= 20):
                raise CharacterValidationError(f"Invalid value for {stat}: must be between 3 and 20")

    return True

def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to be safe for all operating systems.
    
    Args:
        filename: The filename to sanitize
    
    Returns:
        str: Sanitized filename
    """
    # Remove invalid characters and convert spaces to underscores
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    sanitized = sanitized.strip().replace(' ', '_').lower()
    
    # Ensure the filename isn't empty or a reserved name
    if not sanitized or sanitized in ['con', 'prn', 'aux', 'nul', 'com1', 'com2', 'com3', 'com4']:
        sanitized = f"character_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    return sanitized

def save_character(character_data: Dict[str, Any], filepath: Union[str, Path]) -> str:
    """
    Save character data to a JSON file.
    
    Args:
        character_data: Dictionary containing character information
        filepath: Path to save the file
        
    Returns:
        str: Path to the saved file
        
    Raises:
        IOError: If file cannot be saved
    """
    try:
        # Validate character data before saving
        validate_character_data(character_data)
        
        # Ensure directory exists
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Save the file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(character_data, f, indent=4, ensure_ascii=False)
        
        logger.info(f"Character saved successfully to {filepath}")
        return str(filepath)
    
    except Exception as e:
        logger.error(f"Error saving character: {str(e)}")
        raise

def load_character(filepath: Union[str, Path]) -> Dict[str, Any]:
    """
    Load character data from a JSON file.
    
    Args:
        filepath: Path to the character file
        
    Returns:
        dict: Character data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        JSONDecodeError: If file is not valid JSON
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            character_data = json.load(f)
        
        # Validate loaded data
        validate_character_data(character_data)
        return character_data
    
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {filepath}: {str(e)}")
        raise ValueError(f"Invalid character file format: {str(e)}")
    except Exception as e:
        logger.error(f"Error loading character: {str(e)}")
        raise

def format_character_output(character_data: Dict[str, Any], format_type: str = 'text') -> str:
    """
    Format character data for display in various formats.
    
    Args:
        character_data: Dictionary containing character information
        format_type: Output format ('text', 'markdown', or 'html')
    
    Returns:
        str: Formatted character information
    """
    try:
        validate_character_data(character_data)
        
        if format_type == 'markdown':
            return f"""# {character_data['name']}
## Basic Information
- **Race:** {character_data['race']}
- **Class:** {character_data['class']}
- **Alignment:** {character_data['alignment']}

## Stats
{_format_stats_markdown(character_data['stats'])}

## Background
{character_data['background']}
"""
        elif format_type == 'html':
            return f"""<h1>{character_data['name']}</h1>
<h2>Basic Information</h2>
<ul>
    <li><strong>Race:</strong> {character_data['race']}</li>
    <li><strong>Class:</strong> {character_data['class']}</li>
    <li><strong>Alignment:</strong> {character_data['alignment']}</li>
</ul>
<h2>Background</h2>
<p>{character_data['background']}</p>
"""
        else:  # default to text
            return f"""Character Name: {character_data['name']}
Race: {character_data['race']}
Class: {character_data['class']}
Alignment: {character_data['alignment']}

Stats:
{_format_stats_text(character_data['stats'])}

Background:
{character_data['background']}
"""
    except Exception as e:
        logger.error(f"Error formatting character output: {str(e)}")
        raise

def _format_stats_text(stats: Dict[str, int]) -> str:
    """Helper function to format stats in text format."""
    return '\n'.join(f"{stat.title()}: {value}" for stat, value in stats.items())

def _format_stats_markdown(stats: Dict[str, int]) -> str:
    """Helper function to format stats in markdown format."""
    return '\n'.join(f"- **{stat.title()}:** {value}" for stat, value in stats.items())

def get_modifier(stat_value: int) -> int:
    """
    Calculate ability modifier from stat value.
    
    Args:
        stat_value: The ability score value
        
    Returns:
        int: The ability modifier
    """
    return (stat_value - 10) // 2

if __name__ == "__main__":
    # Example usage
    test_character = {
        "name": "Test Character",
        "race": "Elf",
        "class": "Wizard",
        "alignment": "Neutral Good",
        "stats": {
            "strength": 10,
            "dexterity": 15,
            "constitution": 12,
            "intelligence": 16,
            "wisdom": 13,
            "charisma": 11
        },
        "background": "Test background"
    }
    
    # Test validation
    try:
        validate_character_data(test_character)
        print("Character validation successful!")
    except CharacterValidationError as e:
        print(f"Validation error: {str(e)}")
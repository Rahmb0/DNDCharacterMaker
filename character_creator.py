# character_creator.py

import os
import json
import argparse
from typing import Dict, Optional
from dotenv import load_dotenv
from src.character_generator import generate_character
from src.utils import validate_input

# Constants
VALID_RACES = ["Dragonborn", "Dwarf", "Elf", "Gnome", "Half-Elf", "Half-Orc", "Halfling", "Human", "Tiefling"]
VALID_CLASSES = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"]
VALID_ALIGNMENTS = ["Lawful Good", "Neutral Good", "Chaotic Good", "Lawful Neutral", "True Neutral", 
                    "Chaotic Neutral", "Lawful Evil", "Neutral Evil", "Chaotic Evil"]
VALID_BACKSTORY_DEPTHS = ["brief", "moderate", "detailed"]

def get_user_input(prompt: str, valid_options: list, error_message: str) -> str:
    """Get and validate user input against a list of valid options."""
    while True:
        user_input = input(prompt).strip().title()
        if user_input in valid_options:
            return user_input
        print(f"Error: {error_message}")
        print(f"Valid options: {', '.join(valid_options)}")

def save_character(character: Dict, filename: Optional[str] = None) -> str:
    """Save character to JSON file and return the filename."""
    if not filename:
        filename = f"{character['name'].lower().replace(' ', '_')}"
    
    # Ensure the data directory exists
    os.makedirs("data/characters", exist_ok=True)
    filepath = f"data/characters/{filename}.json"
    
    try:
        with open(filepath, "w") as f:
            json.dump(character, f, indent=4)
        return filepath
    except IOError as e:
        raise IOError(f"Failed to save character: {e}")

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="D&D Character Creator")
    parser.add_argument("--race", choices=VALID_RACES, help="Character race")
    parser.add_argument("--class", dest="class_type", choices=VALID_CLASSES, help="Character class")
    parser.add_argument("--alignment", choices=VALID_ALIGNMENTS, help="Character alignment")
    parser.add_argument("--backstory", choices=VALID_BACKSTORY_DEPTHS, default="moderate", 
                       help="Backstory detail level")
    return parser.parse_args()

def main():
    """Main function to run the character creator."""
    try:
        # Load environment variables
        if not load_dotenv():
            raise EnvironmentError("Failed to load .env file")
        
        if not os.getenv("OPENAI_API_KEY"):
            raise EnvironmentError("OPENAI_API_KEY not found in environment variables")

        print("\n=== Welcome to the D&D Character Creator! ===\n")

        # Parse command line arguments
        args = parse_arguments()

        # Get character details either from arguments or user input
        race = args.race or get_user_input(
            "Enter character race: ",
            VALID_RACES,
            "Invalid race selected."
        )

        class_type = args.class_type or get_user_input(
            "Enter character class: ",
            VALID_CLASSES,
            "Invalid class selected."
        )

        alignment = args.alignment or get_user_input(
            "Enter character alignment: ",
            VALID_ALIGNMENTS,
            "Invalid alignment selected."
        )

        backstory_depth = args.backstory or get_user_input(
            "Enter backstory depth (brief/moderate/detailed): ",
            VALID_BACKSTORY_DEPTHS,
            "Invalid backstory depth selected."
        )

        # Generate character
        print("\nGenerating character...")
        character = generate_character(race, class_type, alignment, backstory_depth)

        # Display character
        print("\nGenerated Character:")
        print(json.dumps(character, indent=4))

        # Save character
        save_option = input("\nWould you like to save this character? (yes/no): ").lower()
        if save_option in ['y', 'yes']:
            filename = input("Enter filename (press Enter for auto-generated name): ").strip()
            saved_path = save_character(character, filename)
            print(f"\nCharacter saved successfully to: {saved_path}")

    except KeyboardInterrupt:
        print("\n\nCharacter creation cancelled.")
        return 1
    except Exception as e:
        print(f"\nError: {str(e)}")
        return 1

    print("\nThank you for using the D&D Character Creator!")
    return 0

if __name__ == "__main__":
    exit(main())
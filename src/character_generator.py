import os
import json
import logging
from typing import Dict, List, Optional
import openai
from .utils import validate_input

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CharacterGenerationError(Exception):
    """Custom exception for character generation errors."""
    pass

class CharacterGenerator:
    """Handles D&D character generation using OpenAI's API."""
    
    # Class constants
    VALID_RACES = ["Dragonborn", "Dwarf", "Elf", "Gnome", "Half-Elf", "Half-Orc", "Halfling", "Human", "Tiefling"]
    VALID_CLASSES = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"]
    VALID_ALIGNMENTS = ["Lawful Good", "Neutral Good", "Chaotic Good", "Lawful Neutral", "True Neutral", "Chaotic Neutral", "Lawful Evil", "Neutral Evil", "Chaotic Evil"]
    
    def __init__(self):
        """Initialize the character generator with API configuration."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "2000"))
        
        if not self.api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        openai.api_key = self.api_key

    def generate_character(self, race: str, class_type: str, alignment: str, 
                         backstory_depth: str = "moderate", level: int = 1) -> Dict:
        """Generate a complete D&D character with all necessary attributes."""
        try:
            # Validate inputs
            self._validate_inputs(race, class_type, alignment, level)
            
            # Generate character components
            character = {
                "basic_info": self._generate_basic_info(race, class_type, alignment),
                "stats": self._generate_stats(class_type),
                "background": self._generate_background(backstory_depth),
                "equipment": self._generate_equipment(class_type, level),
                "features": self._generate_features(race, class_type, level)
            }
            
            # Add spells if character is a spellcaster
            if self._is_spellcaster(class_type):
                character["spells"] = self._generate_spells(class_type, level)
            
            return self._format_character(character)
            
        except Exception as e:
            logger.error(f"Error generating character: {str(e)}")
            raise CharacterGenerationError(f"Failed to generate character: {str(e)}")

    def _validate_inputs(self, race: str, class_type: str, alignment: str, level: int) -> None:
        """Validate all input parameters."""
        if not validate_input(race, self.VALID_RACES):
            raise ValueError(f"Invalid race. Must be one of: {', '.join(self.VALID_RACES)}")
        if not validate_input(class_type, self.VALID_CLASSES):
            raise ValueError(f"Invalid class. Must be one of: {', '.join(self.VALID_CLASSES)}")
        if not validate_input(alignment, self.VALID_ALIGNMENTS):
            raise ValueError(f"Invalid alignment. Must be one of: {', '.join(self.VALID_ALIGNMENTS)}")
        if not 1 <= level <= 20:
            raise ValueError("Level must be between 1 and 20")

    def _generate_basic_info(self, race: str, class_type: str, alignment: str) -> Dict:
        """Generate basic character information including name and personality."""
        prompt = self._create_prompt("basic_info", {
            "race": race,
            "class": class_type,
            "alignment": alignment
        })
        
        response = self._call_openai_api(prompt)
        return json.loads(response)

    def _generate_stats(self, class_type: str) -> Dict:
        """Generate appropriate ability scores based on class."""
        base_stats = self._roll_stats()
        optimized_stats = self._optimize_stats_for_class(base_stats, class_type)
        return optimized_stats

    def _generate_background(self, depth: str) -> Dict:
        """Generate character background and personality traits."""
        prompt = self._create_prompt("background", {"depth": depth})
        response = self._call_openai_api(prompt)
        return json.loads(response)

    def _generate_equipment(self, class_type: str, level: int) -> List:
        """Generate appropriate equipment based on class and level."""
        prompt = self._create_prompt("equipment", {
            "class": class_type,
            "level": level
        })
        response = self._call_openai_api(prompt)
        return json.loads(response)

    def _generate_features(self, race: str, class_type: str, level: int) -> Dict:
        """Generate racial and class features."""
        prompt = self._create_prompt("features", {
            "race": race,
            "class": class_type,
            "level": level
        })
        response = self._call_openai_api(prompt)
        return json.loads(response)

    def _generate_spells(self, class_type: str, level: int) -> Optional[Dict]:
        """Generate spell list for spellcasting classes."""
        if not self._is_spellcaster(class_type):
            return None
            
        prompt = self._create_prompt("spells", {
            "class": class_type,
            "level": level
        })
        response = self._call_openai_api(prompt)
        return json.loads(response)

    def _call_openai_api(self, prompt: str) -> str:
        """Make API call to OpenAI."""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content
        except openai.error.OpenAIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise CharacterGenerationError(f"API error: {str(e)}")

    @staticmethod
    def _is_spellcaster(class_type: str) -> bool:
        """Determine if a class is a spellcaster."""
        return class_type in ["Wizard", "Cleric", "Bard", "Druid", "Sorcerer", "Warlock", "Paladin", "Ranger"]

    @staticmethod
    def _create_prompt(prompt_type: str, params: Dict) -> str:
        """Create appropriate prompt based on type and parameters."""
        # Load prompt templates from file or define them here
        prompts = {
            "basic_info": "Generate a D&D character with race: {race}, class: {class}, alignment: {alignment}...",
            "background": "Create a {depth} backstory for a D&D character...",
            "equipment": "List appropriate equipment for a level {level} {class}...",
            "features": "List features for a level {level} {race} {class}...",
            "spells": "Generate appropriate spells for a level {level} {class}..."
        }
        return prompts[prompt_type].format(**params)

    def _format_character(self, character: Dict) -> Dict:
        """Format and validate the final character data."""
        # Add any final formatting or validation here
        return character

if __name__ == "__main__":
    generator = CharacterGenerator()
    character = generator.generate_character(
        race="Elf",
        class_type="Wizard",
        alignment="Neutral Good",
        backstory_depth="moderate",
        level=1
    )
    print(json.dumps(character, indent=2))
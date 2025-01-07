import unittest
from unittest.mock import patch, Mock
from src.character_generator import (
    generate_character,
    generate_stats,
    generate_equipment,
    generate_spells
)

class TestCharacterGenerator(unittest.TestCase):
    """Test suite for character generation functionality."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.valid_races = ["Elf", "Dwarf", "Human", "Halfling"]
        self.valid_classes = ["Fighter", "Wizard", "Rogue", "Cleric"]
        self.valid_alignments = ["Lawful Good", "Chaotic Neutral", "True Neutral"]
        
        self.test_character_params = {
            "race": "Elf",
            "class_type": "Wizard",
            "alignment": "Neutral Good",
            "backstory_depth": "moderate"
        }

    @patch('src.character_generator.openai.ChatCompletion.create')
    def test_generate_character_basic(self, mock_openai):
        """Test basic character generation with all valid parameters."""
        # Mock OpenAI response
        mock_openai.return_value = Mock(
            choices=[Mock(message=Mock(content='''
            {
                "name": "Thalanil Moonweaver",
                "race": "Elf",
                "class": "Wizard",
                "level": 1,
                "alignment": "Neutral Good",
                "background": "Sage",
                "stats": {
                    "strength": 8,
                    "dexterity": 14,
                    "constitution": 12,
                    "intelligence": 16,
                    "wisdom": 13,
                    "charisma": 10
                }
            }
            '''))]
        )

        character = generate_character(**self.test_character_params)
        
        self.assertIsInstance(character, dict)
        self.assertIn('name', character)
        self.assertIn('stats', character)
        self.assertEqual(character['race'], 'Elf')
        self.assertEqual(character['class'], 'Wizard')

    def test_character_stats_validation(self):
        """Test that generated character stats meet D&D 5e requirements."""
        stats = generate_stats(self.test_character_params['class_type'])
        
        # Test stat range
        for stat_value in stats.values():
            self.assertGreaterEqual(stat_value, 3)
            self.assertLessEqual(stat_value, 18)
        
        # Test total stats are within reasonable range
        total_stats = sum(stats.values())
        self.assertGreaterEqual(total_stats, 60)  # Minimum reasonable total
        self.assertLessEqual(total_stats, 80)     # Maximum reasonable total

    def test_class_specific_requirements(self):
        """Test that characters meet their class-specific requirements."""
        test_cases = [
            ("Wizard", "intelligence"),
            ("Rogue", "dexterity"),
            ("Fighter", "strength"),
            ("Cleric", "wisdom")
        ]

        for class_type, primary_stat in test_cases:
            with self.subTest(class_type=class_type):
                character = generate_character(
                    race="Human",
                    class_type=class_type,
                    alignment="Neutral"
                )
                self.assertGreaterEqual(character['stats'][primary_stat], 12)

    def test_invalid_inputs(self):
        """Test error handling for invalid inputs."""
        invalid_test_cases = [
            {"race": "InvalidRace", "class_type": "Wizard", "alignment": "Neutral Good"},
            {"race": "Elf", "class_type": "InvalidClass", "alignment": "Neutral Good"},
            {"race": "Elf", "class_type": "Wizard", "alignment": "InvalidAlignment"},
            {"race": "", "class_type": "Wizard", "alignment": "Neutral Good"},
        ]

        for invalid_params in invalid_test_cases:
            with self.subTest(params=invalid_params):
                with self.assertRaises(ValueError):
                    generate_character(**invalid_params)

    @patch('src.character_generator.openai.ChatCompletion.create')
    def test_backstory_depth(self, mock_openai):
        """Test different backstory depth levels."""
        depths = ["brief", "moderate", "detailed"]
        
        for depth in depths:
            with self.subTest(depth=depth):
                params = {**self.test_character_params, "backstory_depth": depth}
                character = generate_character(**params)
                self.assertIn('backstory', character)
                
                if depth == "brief":
                    self.assertLess(len(character['backstory'].split()), 100)
                elif depth == "detailed":
                    self.assertGreater(len(character['backstory'].split()), 200)

    def test_equipment_generation(self):
        """Test equipment generation based on class."""
        test_cases = [
            ("Wizard", ["spellbook", "component pouch"]),
            ("Fighter", ["armor", "weapon"]),
            ("Rogue", ["thieves' tools"]),
            ("Cleric", ["holy symbol"])
        ]

        for class_type, expected_items in test_cases:
            with self.subTest(class_type=class_type):
                equipment = generate_equipment(class_type)
                for item in expected_items:
                    self.assertTrue(
                        any(item.lower() in eq.lower() for eq in equipment),
                        f"Expected {item} in {class_type}'s equipment"
                    )

    def test_spell_generation(self):
        """Test spell generation for spellcasting classes."""
        spellcasting_classes = ["Wizard", "Cleric", "Bard"]
        non_spellcasting_classes = ["Fighter", "Rogue", "Barbarian"]

        # Test spellcasting classes
        for class_type in spellcasting_classes:
            with self.subTest(class_type=class_type):
                spells = generate_spells(class_type, level=1)
                self.assertIsInstance(spells, dict)
                self.assertIn('cantrips', spells)
                self.assertIn('level_1', spells)

        # Test non-spellcasting classes
        for class_type in non_spellcasting_classes:
            with self.subTest(class_type=class_type):
                spells = generate_spells(class_type, level=1)
                self.assertEqual(spells, {})

    def test_character_consistency(self):
        """Test that generated characters maintain internal consistency."""
        character = generate_character(**self.test_character_params)
        
        # Test alignment-personality consistency
        if "Evil" in character['alignment']:
            self.assertNotIn("altruistic", character['traits'].lower())
        
        # Test race-attribute consistency
        if character['race'] == "Elf":
            self.assertGreaterEqual(character['stats']['dexterity'], 10)

if __name__ == '__main__':
    unittest.main(verbosity=2)
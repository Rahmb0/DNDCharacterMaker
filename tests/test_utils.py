import unittest
from unittest.mock import patch
import os
import json
from src.utils import (
    validate_input,
    sanitize_filename,
    load_character,
    save_character,
    validate_character_data
)

class TestUtils(unittest.TestCase):
    """Test suite for utility functions used in the D&D Character Creator."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.valid_character = {
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
            }
        }
        self.test_dir = "test_data"
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        """Clean up test fixtures after each test method."""
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)

    def test_validate_input(self):
        """Test input validation for character attributes."""
        test_cases = [
            # (input, valid_options, expected_result, should_raise)
            ("Elf", ["Elf", "Human", "Dwarf"], True, False),
            ("Elephant", ["Elf", "Human", "Dwarf"], False, False),
            ("", ["Elf", "Human", "Dwarf"], False, True),
            ("   Elf   ", ["Elf", "Human", "Dwarf"], True, False),  # Test whitespace
            ("elf", ["Elf", "Human", "Dwarf"], True, False),  # Test case-insensitive
        ]

        for input_val, valid_options, expected, should_raise in test_cases:
            if should_raise:
                with self.assertRaises(ValueError):
                    validate_input(input_val, valid_options)
            else:
                result = validate_input(input_val, valid_options)
                self.assertEqual(result, expected)

    def test_sanitize_filename(self):
        """Test filename sanitization."""
        test_cases = [
            ("Test Character", "test_character"),
            ("Test@#$%Character", "test_character"),
            ("   Spaces   ", "spaces"),
            ("../path/traversal", "path_traversal"),
            ("Com1", "character"),  # Windows reserved name
            ("", "character"),  # Empty string
        ]

        for input_name, expected in test_cases:
            result = sanitize_filename(input_name)
            self.assertEqual(result, expected)
            self.assertTrue(result.isalnum() or '_' in result)

    def test_save_and_load_character(self):
        """Test character saving and loading functionality."""
        filename = os.path.join(self.test_dir, "test_character.json")
        
        # Test saving
        save_character(self.valid_character, filename)
        self.assertTrue(os.path.exists(filename))
        
        # Test loading
        loaded_character = load_character(filename)
        self.assertEqual(loaded_character, self.valid_character)
        
        # Test loading non-existent file
        with self.assertRaises(FileNotFoundError):
            load_character("nonexistent.json")

    def test_validate_character_data(self):
        """Test character data validation."""
        # Test valid character
        self.assertTrue(validate_character_data(self.valid_character))
        
        # Test missing required fields
        invalid_characters = [
            {},  # Empty dictionary
            {"name": "Test"},  # Missing required fields
            {**self.valid_character, "stats": None},  # Invalid stats
            {**self.valid_character, "alignment": "Invalid"},  # Invalid alignment
        ]
        
        for invalid_char in invalid_characters:
            with self.assertRaises(ValueError):
                validate_character_data(invalid_char)

    @patch('src.utils.validate_input')
    def test_input_validation_integration(self, mock_validate):
        """Test integration with input validation."""
        mock_validate.return_value = True
        
        # Test character creation with mocked validation
        test_data = {
            "name": "Test Character",
            "race": "Elf",
            "class": "Wizard",
            "alignment": "Neutral Good"
        }
        
        self.assertTrue(validate_character_data(test_data))
        mock_validate.assert_called()

    def test_error_handling(self):
        """Test error handling in utility functions."""
        # Test file permission error
        with patch('builtins.open', side_effect=PermissionError):
            with self.assertRaises(PermissionError):
                save_character(self.valid_character, "test.json")

        # Test JSON decode error
        with patch('json.loads', side_effect=json.JSONDecodeError("Test error", "", 0)):
            with self.assertRaises(ValueError):
                load_character("test.json")

if __name__ == '__main__':
    unittest.main(verbosity=2)
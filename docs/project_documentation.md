# Project Documentation for DND Character Creator

## Overview

The DND Character Creator is a tool designed to assist players and Dungeon Masters in generating detailed and imaginative characters for Dungeons & Dragons campaigns. By leveraging the OpenAI API, this project automates the creation of character names, backstories, abilities, and traits, making it easier to bring characters to life.

## Features

- **AI-Generated Character Details**: Automatically generates character names, backstories, abilities, and traits.
- **Customizable Parameters**: Allows users to adjust race, class, alignment, and other key attributes.
- **Creative Backstories**: Provides rich, lore-friendly backstories tailored to specific campaign settings.
- **User-Friendly Interface**: Offers easy-to-use prompts and configurations for a seamless experience.

## Project Structure

The project is organized into several key directories and files:

- **Root Directory**:
  - `README.md`: Main documentation file for the project.
  - `LICENSE`: License information for the project.
  - `.env.example`: Example environment variables file.
  - `requirements.txt`: List of dependencies for the project.
  - `character_creator.py`: Main script to run the character creator.

- **Data Directory**:
  - `data/sample_characters.json`: Contains sample character data in JSON format.

- **Documentation Directory**:
  - `docs/project_documentation.md`: Additional documentation providing detailed information about the project.

- **Source Directory**:
  - `src/__init__.py`: Marks the src directory as a Python package.
  - `src/character_generator.py`: Contains the logic for generating character details.
  - `src/utils.py`: Contains utility functions that support the main character generation logic.

- **Tests Directory**:
  - `tests/test_character_generator.py`: Unit tests for the character generation logic.
  - `tests/test_utils.py`: Unit tests for the utility functions.

## Installation

To set up the DND Character Creator, follow these steps:

1. Clone the repository from GitHub.
2. Install the required dependencies using pip.
3. Set up your OpenAI API key in a `.env` file.

## Usage

To use the DND Character Creator:

1. Run the main script `character_creator.py`.
2. Follow the prompts to enter character details and preferences.
3. View and save the generated character details for future use.

## Contributing

Contributions to the DND Character Creator are welcome. To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. Please refer to the `LICENSE` file for more details.

## Acknowledgments

- Special thanks to OpenAI for providing the API that powers the character generation.
- Gratitude to the Dungeons & Dragons community for their inspiration and creativity.
# DND Character Creator

Welcome to the DND Character Creator! This project leverages the power of the OpenAI API to help you create detailed and imaginative characters for your Dungeons & Dragons campaigns. Whether you're a seasoned Dungeon Master or a first-time player, this tool will simplify the process of bringing your characters to life.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Example Output](#example-output)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features
- **AI-Generated Character Details**: 
  - Character names based on race and background
  - Rich, detailed backstories
  - Balanced ability scores and traits
  - Personality traits, ideals, bonds, and flaws
- **Customizable Parameters**: 
  - Choose from all official D&D 5e races and classes
  - Select background and alignment
  - Set custom ability score generation methods
- **Campaign Integration**: 
  - Generate characters that fit your campaign setting
  - Create NPCs with specific roles and motivations
  - Include relevant faction affiliations
- **Export Options**:
  - Save as JSON for programmatic use
  - Export to PDF character sheets
  - Plain text format for easy sharing

---

## Project Structure

The project is structured as follows:

```
dnd-character-creator/
├── README.md
├── LICENSE
├── .env.example
├── requirements.txt
├── character_creator.py
├── data/
│   └── sample_characters.json
├── docs/
│   └── project_documentation.md
├── src/
│   ├── __init__.py
│   ├── character_generator.py
│   ├── utils.py
└── tests/
    ├── test_character_generator.py
    └── test_utils.py
```

- `README.md`: Main documentation file for the project.
- `LICENSE`: License information for the project.
- `.env.example`: Example environment variables file.
- `requirements.txt`: List of dependencies for the project.
- `character_creator.py`: Main script to run the character creator.
- `data/`: Directory for storing sample character data and other resources.
- `docs/`: Directory for additional documentation.
- `src/`: Directory for source code.
- `tests/`: Directory for unit tests.

---

## Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Basic understanding of D&D 5e mechanics

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/dnd-character-creator.git
   cd dnd-character-creator
   ```

2. **Create and Activate Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On Unix or MacOS
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

## Usage

### Basic Usage
```bash
python character_creator.py
```

### Advanced Options
```bash
python character_creator.py --race elf --class wizard --level 5 --alignment "lawful good"
```

### Configuration Options
| Option | Description | Default |
|--------|-------------|---------|
| `--level` | Character starting level | 1 |
| `--method` | Ability score generation method | "standard array" |
| `--detail` | Backstory detail level (1-5) | 3 |

---

## Example Output

**Character Name**: Kaelith Moonshadow  
**Race**: Elf  
**Class**: Rogue  
**Alignment**: Chaotic Neutral  
**Backstory**: Kaelith grew up in the shadowy streets of Neverwinter, mastering the art of stealth and deception. A chance encounter with a mysterious artifact set her on a path to uncover secrets that could reshape the Forgotten Realms.

---

## Contributing

We welcome contributions! Please follow these steps:

1. **Fork and Clone**:
   ```bash
   git fork https://github.com/your-username/dnd-character-creator.git
   ```

2. **Create Feature Branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Commit Changes**:
   ```bash
   git commit -m 'Add amazing feature'
   ```

4. **Push and Create PR**:
   ```bash
   git push origin feature/amazing-feature
   ```

### Development Guidelines
- Follow PEP 8 style guide
- Add unit tests for new features
- Update documentation as needed
- Maintain compatibility with Python 3.8+

## Troubleshooting

Common issues and solutions:
- **API Key Issues**: Ensure your `.env` file is properly configured
- **Dependencies**: Try `pip install --upgrade -r requirements.txt`
- **Generation Fails**: Check your internet connection and API quota

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- OpenAI for their incredible API.
- The Dungeons & Dragons community for endless inspiration and creativity.
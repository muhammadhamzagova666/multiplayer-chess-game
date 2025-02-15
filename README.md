# Python Multiplayer Chess

> A feature-rich and extensible Python chess game with local, online, and AI modes.

[![Pygame](https://img.shields.io/badge/pygame-2.0+-blue.svg)](https://www.pygame.org/)
[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)

## Overview

Python Multiplayer Chess is a comprehensive chess game implemented in Python using the Pygame library. It supports local multiplayer, online gameplay, and an AI opponent powered by the Stockfish chess engine. The project aims to provide a clean, modular, and extensible codebase, making it suitable for both playing and learning about game development.

### Key Features

*   **Local Multiplayer:** Play against a friend on the same computer.
*   **Online Gameplay:** Challenge other players online.
*   **AI Opponent:** Test your skills against the Stockfish chess engine.
*   **Customizable Timers:** Set time limits for games.
*   **User Preferences:** Customize the game's appearance and behavior.
*   **Clean and Modular Codebase:** Easy to understand and extend.

### Target Audience

*   Chess enthusiasts looking for a digital version of the game.
*   Python developers interested in game development.
*   Students learning about AI and game programming.

### Unique Selling Points

*   **Multi-Mode Gameplay:** Offers local, online, and AI modes in one application.
*   **Extensible Architecture:** Designed for easy modification and addition of new features.
*   **Well-Documented Code:** Includes detailed comments and documentation to aid understanding.
*   **Stockfish Integration:** Provides a strong AI opponent for challenging gameplay.

## Technology Stack

*   [Python 3.6+](https://www.python.org/)
*   [Pygame 2.0+](https://www.pygame.org/)
*   [Stockfish](https://stockfishchess.org/) (for AI opponent)

## Installation & Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/muhammadhamzagova666/multiplayer-chess-game.git
    cd multiplayer-chess-game
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    Create a `requirements.txt` file with the following content:

    ```txt
    pygame>=2.0
    # Add any other dependencies here
    ```

3.  **Configure Stockfish (Optional):**

    *   Download and install the Stockfish chess engine for your operating system from the [Stockfish website](https://stockfishchess.org/).
    *   Update the path to the Stockfish executable in `res/stockfish/path.txt`.  The game provides instructions for setting this up, as seen in loader.py.

    *   **Example `res/stockfish/path.txt` (Linux):**

        ```txt
        /usr/games/stockfish
        ```

    *   **Example `res/stockfish/path.txt` (Windows):**

        ```txt
        C:\\Stockfish\\stockfish.exe
        ```

4.  **Run the game:**

    ```bash
    python Source/pychess.py
    ```

## Usage Guide

*   **Main Menu:** Use the main menu to select game modes (Local, Online, AI), configure preferences, and adjust timer settings.
*   **Local Multiplayer:** Select "Local" from the main menu and start playing.
*   **Online Gameplay:**
    1.  Select "Online" from the main menu.
    2.  Enter the server address and port.
    3.  Connect to the server and wait for an opponent.
*   **AI Opponent:** Select "AI" from the main menu to play against Stockfish.
*   **Preferences:** Customize game settings such as sound, board orientation, and move highlighting via the preferences menu.

## Project Structure

```
PyChessMP/
├── Multiplayer Chess Game Project Proposal.docx
├── Multiplayer Chess Game Project Proposal.pdf
├── Multiplayer Chess Game Project Report.docx
├── Source/
│   ├── chess/
│   │   ├── __init__.py
│   │   ├── lib/
│   │   │   ├── __init__.py
│   │   │   ├── core.py       # Core chess logic (move generation, validation)
│   │   │   ├── gui.py        # Pygame-based GUI implementation
│   │   │   └── utils.py      # Utility functions (encoding, decoding, board setup)
│   │   ├── multiplayer.py  # Local multiplayer game logic
│   │   ├── online.py       # Online game logic
│   │   └── onlinelib/      # Networking utilities for online play
│   ├── ext/
│   │   └── pyBox.py        # Custom text box for user input
│   ├── menus/
│   │   ├── __init__.py
│   │   ├── online.py       # Online menu implementation
│   │   ├── pref.py         # Preferences menu implementation
│   │   └── timer.py        # Timer menu implementation
│   ├── pychess.py          # Main application entry point
│   ├── res/
│   │   ├── Asimov.otf      # Font file
│   │   ├── img/            # Image resources
│   │   ├── preferences.txt # User preferences file
│   │   ├── sounds/         # Sound resources
│   │   └── texts/          # Text resources (instructions, messages)
│   ├── server.py           # Server-side code for online play
│   └── tools/
│       ├── loader.py       # Resource loading module
│       ├── sound.py        # Sound management module
│       └── utils.py        # General utility functions
├── tools/
│   ├── loader.py
│   └── sound.py
└── README.md
```

*   **`Source/chess/lib/core.py`**: Contains the core chess logic, including move generation, validation, and game state management.
*   **`Source/chess/lib/gui.py`**: Implements the graphical user interface using Pygame.
*   **`Source/chess/lib/utils.py`**: Provides utility functions for encoding moves, initializing the board, and other helper tasks.
*   **`Source/pychess.py`**: The main entry point of the application, responsible for initializing Pygame, loading resources, and managing the main game loop.
*   **menus**: Contains the implementation of the various menus in the game, such as the online menu, preferences menu, and timer menu.
*   **res**: Stores all the resources used by the game, including images, sounds, fonts, and text files.
*   **tools**: Contains helper modules for loading resources and managing sound.

## Configuration & Environment Variables

*   **`res/preferences.txt`**: Stores user preferences such as sound settings, board orientation, and move highlighting.  See pref.py for how these preferences are managed.
*   **`res/stockfish/path.txt`**: Specifies the path to the Stockfish executable.
*   **Environment Variables (for online play):**

    ```bash
    CHESS_SERVER_HOST=localhost
    CHESS_SERVER_PORT=5000
    ```

## Deployment Guide

Instructions for deploying the project (e.g., Docker, Kubernetes, cloud services).  CI/CD integration steps if applicable.

## Testing & Debugging

*   **Unit Tests:**  (Example using `pytest`)

    ```bash
    pip install pytest
    pytest tests/
    ```

*   **Debugging Tips:**
    *   Enable debug mode in the preferences menu.
    *   Check the console output for error messages.
    *   Use the built-in move validation to verify move legality.

## Performance Optimization

*   **Surface Caching:** Pygame surfaces are cached to improve rendering performance.  See loader.py.
*   **Efficient Move Generation:** The core chess engine uses optimized algorithms for move generation.

## Security Best Practices

*   Input validation is performed on all user inputs.
*   The online gameplay uses secure socket connections.

## Contributing Guidelines

We welcome contributions to multiplayer-chess-game! Please follow these guidelines:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Write clear and concise commit messages.
4.  Submit a pull request with a detailed description of your changes.

## Documentation

*   Reference
*   Contribution Guidelines
*   Stockfish Setup

## Roadmap

*   Implement a more sophisticated AI opponent.
*   Add support for different chess variants.
*   Improve the user interface and add more customization options.
*   Implement a rating system for online players.

## FAQ

**Q: How do I configure Stockfish?**

A: Download the Stockfish engine for your operating system and update the path in `res/stockfish/path.txt`.  See also the Stockfish setup instructions in mac.txt and other files in that directory.

**Q: Can I play the game offline?**

A: Yes, you can play local multiplayer and against the AI opponent offline.

## Acknowledgments

*   The [Pygame](https://www.pygame.org/) library.
*   The [Stockfish](https://stockfishchess.org/) chess engine developers.
*   All contributors to this project.

## Contact Information

*   GitHub: [muhammadhamzagova666](https://github.com/muhammadhamzagova666)

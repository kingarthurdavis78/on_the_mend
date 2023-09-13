# On the Mend - README

## Project Overview

**On the Mend** is a Python-based game project created using the Pygame library. This game features a top-down shooter style with elements of survival and teamwork. Players control characters tasked with fending off waves of zombies while collecting items and upgrading their equipment.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Getting Started](#getting-started)
3. [Gameplay](#gameplay)
4. [Controls](#controls)
5. [Contributing](#contributing)
6. [License](#license)

## Project Structure <a name="project-structure"></a>

The project consists of the following main components:

- `game_logic.py`: Contains the game logic and classes for Bob (the player character), zombies, guns, items, and more.

- `main.py`: The main script that initializes the game, manages player input, and handles the game loop.

- `assets`: A directory containing audio files (`*.mp3`) for in-game music.

- `README.md`: This documentation file.

## Getting Started

To play **On the Mend**, follow these steps:

1. Ensure you have Python and Pygame installed on your system.

2. Clone or download the project repository from [GitHub](https://github.com/your-github-repo/on-the-mend).

3. Open a terminal or command prompt and navigate to the project directory.

4. Run the game using the following command:

   ```bash
   python main.py <keyboard_count> <controller_count>
   ```

   - `<keyboard_count>`: The number of players using the keyboard (0 or 1).
   - `<controller_count>`: The number of players using game controllers.

   Example:

   ```bash
   python main.py 2 1
   ```

5. Enjoy the game and survive as long as possible!

## Gameplay

**On the Mend** offers exciting gameplay where players must cooperate to survive against waves of zombies. Here are some key features and objectives:

- Players control characters (Bobs) who can collect items, shoot zombies, and revive fallen teammates.

- Zombies spawn periodically, and players must eliminate them to progress through the game's levels.

- Items such as weapons and health packs can be found on the ground and collected to enhance your abilities and stay alive.

- The game's difficulty increases over time, providing an ever-greater challenge.

- The game can be won by achieving a specific goal, but it's also possible to lose if all players are eliminated.

## Controls

- **Keyboard Players:**

  - Movement: Arrow keys
  - Shoot: Spacebar
  - Sprint: Shift key
  - Revive Teammate: R key

- **Controller Players:**

  - Controller-specific buttons for movement, shooting, sprinting, and reviving.

Please note that specific controls may vary depending on your controller configuration.

Enjoy playing **On the Mend** and have fun surviving the zombie apocalypse! If you encounter any issues or have suggestions for improvement, please feel free to contribute or report them on the project's GitHub repository.

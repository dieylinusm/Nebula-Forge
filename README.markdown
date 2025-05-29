# Nebula Forge

Nebula Forge is a unique 2D crafting-strategy game set in a procedurally generated starfield. As a cosmic navigator, you collect resources (Quarks, Plasma, Neutrinos) to craft tools like Shields and Pulses, which help you survive dynamic hazards and explore the grid-based nebula. Balance resource management and strategic tool use to maximize your score in this innovative survival adventure.

## Features
- **Dynamic Starfield**: Navigate a 10x10 grid with procedurally generated resources and hazards.
- **Crafting System**: Combine resources to craft Shields (for protection) or Pulses (to clear hazards).
- **Strategic Survival**: Use tools wisely to avoid hazards and keep exploring.
- **Minimalist Visuals**: Clean, cosmic-themed graphics optimized for browser-based play with Pygame.

## Installation
1. Ensure Python 3.8+ and Pygame are installed:
   ```bash
   pip install pygame
   ```
2. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/nebula-forge.git
   ```
3. Run the game:
   ```bash
   python nebula_forge.py
   ```

## How to Play
- **Objective**: Collect resources to craft tools, avoid hazards, and maximize your score by surviving and exploring.
- **Controls**:
  - Arrow keys: Move the player up, down, left, or right.
  - S: Craft a Shield (requires 2 Quarks, 1 Plasma).
  - P: Craft a Pulse (requires 2 Plasma, 1 Neutrino).
  - U: Use a Pulse to clear adjacent hazards.
- **Mechanics**:
  - Collect resources (purple squares) to gain Quarks, Plasma, or Neutrinos.
  - Hazards (red squares) end the game unless you have a Shield.
  - Crafting/using tools and collecting resources earn points.
- **Game Over**: Hitting a hazard without a Shield ends the game. Press R to restart.

## Browser Compatibility
Nebula Forge is designed for Pyodide compatibility, ensuring smooth performance in browser environments without local file I/O or network dependencies.

## Contributing
Contributions are welcome! Please fork the repository and submit pull requests with your improvements. Adhere to PEP 8 standards and include relevant tests.

## Sponsor
Support the development of Nebula Forge by becoming a GitHub Sponsor! Your contributions help fuel this cosmic adventure.

[Become a Sponsor](https://github.com/sponsors/yourusername)

## License
MIT License. See [LICENSE](LICENSE) for details.
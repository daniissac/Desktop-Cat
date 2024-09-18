# Desktop-Cat

<img src="idling.gif" alt="demo"/>

A desktop kitty that sleeps, wanders around, and keeps you company on your screen.

## Features
- PyQt6-based application for a smooth, modern UI experience
- Randomly chooses actions: idling, sleeping, and walking
- Smooth animations with sprite management
- Stays on top of other windows
- Moves around the screen with collision detection

## Requirements
- Python 3.6+
- PyQt6

## Installation and Setup

1. Clone the repository:
   ```
   git clone https://github.com/daniissac/desktop-cat.git
   cd desktop-cat
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```
   pip install PyQt6
   ```

## Run Instructions
After activating the virtual environment, run the following command in the project root directory:
```
python main.py
```

## Improvements and Future Features
- Add interactivity with mouse events (e.g., petting, feeding)
- Implement more complex behaviors and animations
- Add sound effects
- Create a settings menu to customize the cat's behavior and appearance
- Extend to a full desktop pet program with multiple pets and activities

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
[MIT License](LICENSE)

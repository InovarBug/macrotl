
# Skill Rotation Macro for Throne and Liberty (macrotl)

This script provides a customizable skill rotation macro for the game Throne and Liberty, with support for multiple profiles, a recording feature, logging, and hotkeys for profile switching.

## Installation

1. Ensure you have Python 3.7+ installed on your system.
2. Install the required libraries:
   ```
   pip install pynput pyautogui
   ```
3. Download `skill_rotation_macro.py` and `config.json` to the same directory.

## Usage

1. Run the script:
   ```
   python skill_rotation_macro.py
   ```
2. The default activation key is F1. Hold it to start the skill rotation.
3. Press 'r' to start/stop recording a new skill sequence.
4. Press keys 1-5 to switch between or create new profiles.

## Configuration

Edit `config.json` to customize:
- Activation key
- Skill sequence and cooldowns
- Multiple profiles

## Features

- Customizable skill rotation
- Multiple profiles support
- Recording mode for easy skill sequence creation
- Configurable activation key and skill cooldowns
- Logging system for debugging and usage tracking
- Hotkeys (1-5) for quick profile switching

## Logging

The script creates a `macro_log.txt` file in the same directory, which logs various events and actions for debugging purposes.

## Caution

Use macros responsibly and in accordance with the game's terms of service.

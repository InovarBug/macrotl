
# Skill Rotation Macro for Throne and Liberty (macrotl)

This script provides a customizable skill rotation macro for the game Throne and Liberty, with support for multiple profiles, a recording feature, logging, hotkeys for profile switching, a graphical user interface, and a basic AI learning system.

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
2. Use the graphical interface to:
   - Switch between profiles
   - Set activation keys
   - Record skill sequences
   - Start and stop the macro
   - Adjust cooldowns dynamically
   - Start and stop AI learning
   - Start AI-controlled macro

## Features

- Customizable skill rotation
- Multiple profiles support
- Recording mode for easy skill sequence creation
- Configurable activation key and skill cooldowns
- Dynamic cooldown adjustment
- Logging system for debugging and usage tracking
- Graphical user interface for easy configuration and control
- Basic AI learning system:
  - Learns skill rotation patterns from user gameplay
  - Can execute learned patterns automatically

## AI Learning

1. Click "Start AI Learning" and play the game normally.
2. The AI will learn your skill rotation patterns.
3. Click "Stop AI Learning" when you're done.
4. Click "Start AI Macro" to let the AI execute the learned patterns.

## Logging

The script creates a `macro_log.txt` file in the same directory, which logs various events and actions for debugging purposes.

## Caution

Use macros responsibly and in accordance with the game's terms of service. The AI feature is experimental and may not perfectly replicate human gameplay.


import time
import json
import logging
from pynput import keyboard
import pyautogui
import tkinter as tk
from tkinter import ttk, messagebox
import random
from collections import defaultdict
import cv2
import numpy as np
from PIL import ImageGrab
import traceback
import sys

class SkillRotationMacro:
    def __init__(self):
        try:
            self.running = False
            self.recording = False
            self.learning = False
            self.current_profile = "default"
            self.current_ai_profile = "PVE"  # Default to PVE
            self.profiles = {}
            self.ai_profiles = {"PVE": defaultdict(lambda: {"count": 0, "last_use": 0, "cooldown": 1.0}),
                                "PVP": defaultdict(lambda: {"count": 0, "last_use": 0, "cooldown": 1.0})}
            self.last_action = None
            self.last_action_time = None
            self.auto_detect_mode = False
            self.setup_logging()
            self.load_config()
            self.setup_gui()
        except Exception as e:
            self.log_error("Error during initialization", e)
            raise

    def setup_logging(self):
        try:
            logging.basicConfig(filename='macro_log.txt', level=logging.INFO,
                                format='%(asctime)s - %(levelname)s - %(message)s')
            self.logger = logging.getLogger(__name__)
        except Exception as e:
            print(f"Error setting up logging: {e}")
            raise

    def log_error(self, message, error):
        error_details = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
        self.logger.error(f"{message}: {error_details}")
        messagebox.showerror("Error", f"{message}

Details: {str(error)}")

    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                self.profiles = config.get('profiles', {})
                if not self.profiles:
                    self.profiles['default'] = {
                        'activation_key': 'f1',
                        'skills': []
                    }
                self.current_profile = config.get('current_profile', 'default')
            self.logger.info("Configuration loaded successfully")
        except FileNotFoundError:
            self.logger.warning("Config file not found. Using default settings.")
            self.profiles['default'] = {
                'activation_key': 'f1',
                'skills': []
            }
        except json.JSONDecodeError as e:
            self.log_error("Error decoding config file", e)
            raise
        except Exception as e:
            self.log_error("Error loading configuration", e)
            raise

    def save_config(self):
        try:
            config = {
                'current_profile': self.current_profile,
                'profiles': self.profiles
            }
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)
            self.logger.info("Configuration saved successfully")
        except Exception as e:
            self.log_error("Error saving configuration", e)

    def setup_gui(self):
        try:
            self.root = tk.Tk()
            self.root.title("Skill Rotation Macro")
            self.root.geometry("500x400")

            # ... [rest of the GUI setup code] ...

            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        except Exception as e:
            self.log_error("Error setting up GUI", e)
            raise

    def on_closing(self):
        try:
            self.save_config()
            self.root.destroy()
        except Exception as e:
            self.log_error("Error during application closing", e)
        finally:
            sys.exit(0)

    # ... [rest of the methods with try-except blocks] ...

    def run(self):
        try:
            self.logger.info("Macro started")
            with keyboard.Listener(on_press=self.on_key_press) as listener:
                self.root.mainloop()
        except Exception as e:
            self.log_error("Error in main loop", e)
        finally:
            self.on_closing()

if __name__ == "__main__":
    try:
        macro = SkillRotationMacro()
        macro.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        logging.error(f"Fatal error: {e}")
        sys.exit(1)

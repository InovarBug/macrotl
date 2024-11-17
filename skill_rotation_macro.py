
import time
import json
from pynput import keyboard
import pyautogui

class SkillRotationMacro:
    def __init__(self):
        self.running = False
        self.activation_key = 'f1'  # Default activation key
        self.skills = []
        self.load_config()

    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                self.activation_key = config.get('activation_key', self.activation_key)
                self.skills = config.get('skills', [])
        except FileNotFoundError:
            print("Config file not found. Using default settings.")

    def on_press(self, key):
        try:
            if key.char == self.activation_key:
                self.running = True
                self.rotate_skills()
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            if key.char == self.activation_key:
                self.running = False
        except AttributeError:
            pass

    def rotate_skills(self):
        while self.running:
            for skill in self.skills:
                if not self.running:
                    break
                pyautogui.press(skill['key'])
                time.sleep(skill['cooldown'])

    def run(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

if __name__ == "__main__":
    macro = SkillRotationMacro()
    macro.run()

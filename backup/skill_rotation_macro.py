
import time
import json
from pynput import keyboard
import pyautogui

class SkillRotationMacro:
    def __init__(self):
        self.running = False
        self.recording = False
        self.current_profile = "default"
        self.profiles = {}
        self.load_config()

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
        except FileNotFoundError:
            print("Config file not found. Using default settings.")
            self.profiles['default'] = {
                'activation_key': 'f1',
                'skills': []
            }

    def save_config(self):
        config = {
            'current_profile': self.current_profile,
            'profiles': self.profiles
        }
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)

    def on_press(self, key):
        try:
            if key.char == self.profiles[self.current_profile]['activation_key']:
                if self.recording:
                    self.stop_recording()
                else:
                    self.running = True
                    self.rotate_skills()
            elif key.char == 'r':  # Start/stop recording
                self.toggle_recording()
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            if key.char == self.profiles[self.current_profile]['activation_key']:
                self.running = False
        except AttributeError:
            pass

    def rotate_skills(self):
        while self.running:
            for skill in self.profiles[self.current_profile]['skills']:
                if not self.running:
                    break
                pyautogui.press(skill['key'])
                time.sleep(skill['cooldown'])

    def toggle_recording(self):
        if self.recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        self.recording = True
        self.recorded_skills = []
        print("Recording started. Press skills in the order you want them to be used.")

    def stop_recording(self):
        self.recording = False
        self.profiles[self.current_profile]['skills'] = self.recorded_skills
        self.save_config()
        print("Recording stopped. New skill rotation saved.")

    def on_press_record(self, key):
        if self.recording:
            try:
                self.recorded_skills.append({'key': key.char, 'cooldown': 1.0})
                print(f"Recorded key: {key.char}")
            except AttributeError:
                pass

    def run(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            with keyboard.Listener(on_press=self.on_press_record) as record_listener:
                listener.join()

if __name__ == "__main__":
    macro = SkillRotationMacro()
    macro.run()


import time
import json
import logging
from pynput import keyboard
import pyautogui

class SkillRotationMacro:
    def __init__(self):
        self.running = False
        self.recording = False
        self.current_profile = "default"
        self.profiles = {}
        self.setup_logging()
        self.load_config()

    def setup_logging(self):
        logging.basicConfig(filename='macro_log.txt', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

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
            self.logger.error("Config file not found. Using default settings.")
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
        self.logger.info("Configuration saved successfully")

    def on_press(self, key):
        try:
            if key.char == self.profiles[self.current_profile]['activation_key']:
                if self.recording:
                    self.stop_recording()
                else:
                    self.running = True
                    self.logger.info(f"Macro activated for profile: {self.current_profile}")
                    self.rotate_skills()
            elif key.char == 'r':  # Start/stop recording
                self.toggle_recording()
            elif key.char in ['1', '2', '3', '4', '5']:  # Switch profiles
                self.switch_profile(int(key.char))
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            if key.char == self.profiles[self.current_profile]['activation_key']:
                self.running = False
                self.logger.info("Macro deactivated")
        except AttributeError:
            pass

    def rotate_skills(self):
        while self.running:
            for skill in self.profiles[self.current_profile]['skills']:
                if not self.running:
                    break
                pyautogui.press(skill['key'])
                self.logger.debug(f"Pressed key: {skill['key']}")
                time.sleep(skill['cooldown'])

    def toggle_recording(self):
        if self.recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        self.recording = True
        self.recorded_skills = []
        self.logger.info("Recording started")
        print("Recording started. Press skills in the order you want them to be used.")

    def stop_recording(self):
        self.recording = False
        self.profiles[self.current_profile]['skills'] = self.recorded_skills
        self.save_config()
        self.logger.info("Recording stopped. New skill rotation saved.")
        print("Recording stopped. New skill rotation saved.")

    def on_press_record(self, key):
        if self.recording:
            try:
                self.recorded_skills.append({'key': key.char, 'cooldown': 1.0})
                self.logger.debug(f"Recorded key: {key.char}")
                print(f"Recorded key: {key.char}")
            except AttributeError:
                pass

    def switch_profile(self, profile_number):
        profile_name = f"profile_{profile_number}"
        if profile_name in self.profiles:
            self.current_profile = profile_name
            self.logger.info(f"Switched to profile: {profile_name}")
            print(f"Switched to profile: {profile_name}")
        else:
            self.profiles[profile_name] = {
                'activation_key': 'f1',
                'skills': []
            }
            self.current_profile = profile_name
            self.save_config()
            self.logger.info(f"Created and switched to new profile: {profile_name}")
            print(f"Created and switched to new profile: {profile_name}")

    def run(self):
        self.logger.info("Macro started")
        print("Macro started. Press 1-5 to switch/create profiles.")
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            with keyboard.Listener(on_press=self.on_press_record) as record_listener:
                listener.join()

if __name__ == "__main__":
    macro = SkillRotationMacro()
    macro.run()

import json
import time
import keyboard
import threading

class SkillRotationMacro:
    def __init__(self):
        self.running = False
        self.recording = False
        self.config = self.load_config()
        self.current_profile = list(self.config['profiles'].keys())[0] if self.config['profiles'] else 'default'
        self.skills = self.config['profiles'].get(self.current_profile, {}).get('skills', [])
        self.recorded_skills = []
        self.last_key_time = 0

    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'profiles': {'default': {'skills': []}}}

    def save_config(self):
        with open('config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def toggle_macro(self):
        self.running = not self.running
        if self.running:
            threading.Thread(target=self.run_macro, daemon=True).start()

    def run_macro(self):
        while self.running:
            for skill in self.skills:
                if self.running:
                    keyboard.press_and_release(skill['key'])
                    time.sleep(skill['cooldown'])
                else:
                    break

    def load_profile(self, profile_name):
        if profile_name in self.config['profiles']:
            self.current_profile = profile_name
            self.skills = self.config['profiles'][self.current_profile]['skills']

    def start_recording(self):
        self.recording = True
        self.recorded_skills = []
        self.last_key_time = time.time()
        keyboard.on_press(self.on_key_press)

    def stop_recording(self):
        self.recording = False
        keyboard.unhook_all()

    def on_key_press(self, event):
        if self.recording:
            current_time = time.time()
            cooldown = round(current_time - self.last_key_time, 2)
            self.recorded_skills.append({'key': event.name, 'cooldown': cooldown})
            self.last_key_time = current_time

    def save_recorded_profile(self, profile_name):
        self.config['profiles'][profile_name] = {'skills': self.recorded_skills}
        self.save_config()
        self.load_profile(profile_name)

    def update_skill(self, profile_name, skill_index, key, cooldown):
        self.config['profiles'][profile_name]['skills'][skill_index] = {'key': key, 'cooldown': cooldown}
        self.save_config()
        if profile_name == self.current_profile:
            self.skills = self.config['profiles'][self.current_profile]['skills']

    def create_profile(self, profile_name):
        self.config['profiles'][profile_name] = {'skills': []}
        self.save_config()

if __name__ == "__main__":
    print("Este arquivo não deve ser executado diretamente. Por favor, execute gui.py para usar a interface gráfica.")

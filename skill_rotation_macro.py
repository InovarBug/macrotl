
import time
import json
import logging
from pynput import keyboard
import pyautogui
import tkinter as tk
from tkinter import ttk, messagebox

class SkillRotationMacro:
    def __init__(self):
        self.running = False
        self.recording = False
        self.current_profile = "default"
        self.profiles = {}
        self.setup_logging()
        self.load_config()
        self.setup_gui()

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

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Skill Rotation Macro")
        self.root.geometry("400x300")

        self.profile_var = tk.StringVar(value=self.current_profile)
        self.activation_key_var = tk.StringVar(value=self.profiles[self.current_profile]['activation_key'])

        ttk.Label(self.root, text="Current Profile:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Combobox(self.root, textvariable=self.profile_var, values=list(self.profiles.keys())).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.root, text="Switch Profile", command=self.switch_profile_gui).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(self.root, text="Activation Key:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(self.root, textvariable=self.activation_key_var).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(self.root, text="Set Key", command=self.set_activation_key).grid(row=1, column=2, padx=5, pady=5)

        ttk.Button(self.root, text="Start Recording", command=self.start_recording_gui).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(self.root, text="Stop Recording", command=self.stop_recording_gui).grid(row=2, column=1, padx=5, pady=5)

        self.skill_listbox = tk.Listbox(self.root, width=40, height=10)
        self.skill_listbox.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
        self.update_skill_listbox()

        ttk.Button(self.root, text="Start Macro", command=self.start_macro_gui).grid(row=4, column=0, padx=5, pady=5)
        ttk.Button(self.root, text="Stop Macro", command=self.stop_macro_gui).grid(row=4, column=1, padx=5, pady=5)

    def update_skill_listbox(self):
        self.skill_listbox.delete(0, tk.END)
        for skill in self.profiles[self.current_profile]['skills']:
            self.skill_listbox.insert(tk.END, f"Key: {skill['key']}, Cooldown: {skill['cooldown']}")

    def switch_profile_gui(self):
        new_profile = self.profile_var.get()
        if new_profile in self.profiles:
            self.current_profile = new_profile
            self.activation_key_var.set(self.profiles[self.current_profile]['activation_key'])
            self.update_skill_listbox()
            self.logger.info(f"Switched to profile: {new_profile}")
            messagebox.showinfo("Profile Switched", f"Switched to profile: {new_profile}")
        else:
            messagebox.showerror("Error", "Profile not found")

    def set_activation_key(self):
        new_key = self.activation_key_var.get()
        self.profiles[self.current_profile]['activation_key'] = new_key
        self.save_config()
        self.logger.info(f"Activation key set to: {new_key}")
        messagebox.showinfo("Activation Key Set", f"Activation key set to: {new_key}")

    def start_recording_gui(self):
        self.recording = True
        self.recorded_skills = []
        self.logger.info("Recording started")
        messagebox.showinfo("Recording Started", "Press skills in the order you want them to be used.")

    def stop_recording_gui(self):
        if self.recording:
            self.recording = False
            self.profiles[self.current_profile]['skills'] = self.recorded_skills
            self.save_config()
            self.update_skill_listbox()
            self.logger.info("Recording stopped. New skill rotation saved.")
            messagebox.showinfo("Recording Stopped", "New skill rotation saved.")
        else:
            messagebox.showinfo("Not Recording", "Recording was not in progress.")

    def start_macro_gui(self):
        self.running = True
        self.logger.info(f"Macro activated for profile: {self.current_profile}")
        messagebox.showinfo("Macro Started", f"Macro activated for profile: {self.current_profile}")
        self.root.after(100, self.rotate_skills)

    def stop_macro_gui(self):
        self.running = False
        self.logger.info("Macro deactivated")
        messagebox.showinfo("Macro Stopped", "Macro deactivated")

    def rotate_skills(self):
        if self.running:
            for skill in self.profiles[self.current_profile]['skills']:
                if not self.running:
                    break
                pyautogui.press(skill['key'])
                self.logger.debug(f"Pressed key: {skill['key']}")
                self.root.after(int(skill['cooldown'] * 1000), self.rotate_skills)
                return
        self.root.after(100, self.rotate_skills)

    def on_key_press(self, key):
        if self.recording:
            try:
                self.recorded_skills.append({'key': key.char, 'cooldown': 1.0})
                self.logger.debug(f"Recorded key: {key.char}")
            except AttributeError:
                pass

    def run(self):
        self.logger.info("Macro started")
        with keyboard.Listener(on_press=self.on_key_press) as listener:
            self.root.mainloop()

if __name__ == "__main__":
    macro = SkillRotationMacro()
    macro.run()

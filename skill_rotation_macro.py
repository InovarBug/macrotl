
import time
import json
import logging
from collections import defaultdict
import tkinter as tk
from tkinter import ttk, messagebox
import random

class SkillRotationMacro:
    def __init__(self):
        self.running = False
        self.recording = False
        self.learning = False
        self.current_profile = "default"
        self.current_ai_profile = "PVE"
        self.profiles = {"default": {}}
        self.ai_profiles = {"PVE": defaultdict(lambda: {"count": 0, "last_use": 0, "cooldown": 1.0, "priority": 1}),
                            "PVP": defaultdict(lambda: {"count": 0, "last_use": 0, "cooldown": 1.0, "priority": 1})}
        self.ai_settings = {"PVE": {"aggression": 5, "defense": 5}, "PVP": {"aggression": 5, "defense": 5}}
        self.setup_logging()
        self.setup_gui()

    def setup_logging(self):
        logging.basicConfig(filename='macro_log.txt', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Skill Rotation Macro")
        self.root.geometry("800x600")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        self.setup_profiles_tab()
        self.setup_ai_settings_tab()
        self.setup_recording_tab()
        self.setup_visualization_tab()

    def setup_profiles_tab(self):
        profiles_frame = ttk.Frame(self.notebook)
        self.notebook.add(profiles_frame, text='Profiles')

        ttk.Label(profiles_frame, text="Current Profile:").grid(row=0, column=0, padx=5, pady=5)
        self.profile_var = tk.StringVar(value=self.current_profile)
        profile_combo = ttk.Combobox(profiles_frame, textvariable=self.profile_var, values=list(self.profiles.keys()))
        profile_combo.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(profiles_frame, text="Switch Profile", command=self.switch_profile_gui).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(profiles_frame, text="Activation Key:").grid(row=1, column=0, padx=5, pady=5)
        self.activation_key_var = tk.StringVar(value=self.profiles[self.current_profile].get('activation_key', ''))
        ttk.Entry(profiles_frame, textvariable=self.activation_key_var).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(profiles_frame, text="Set Key", command=self.set_activation_key).grid(row=1, column=2, padx=5, pady=5)

    def setup_ai_settings_tab(self):
        ai_frame = ttk.Frame(self.notebook)
        self.notebook.add(ai_frame, text='AI Settings')

        for i, profile in enumerate(["PVE", "PVP"]):
            ttk.Label(ai_frame, text=f"{profile} Settings").grid(row=i*3, column=0, columnspan=2, padx=5, pady=5)
            
            ttk.Label(ai_frame, text="Aggression:").grid(row=i*3+1, column=0, padx=5, pady=5)
            aggression_scale = ttk.Scale(ai_frame, from_=1, to=10, orient=tk.HORIZONTAL, 
                                         value=self.ai_settings[profile]["aggression"])
            aggression_scale.grid(row=i*3+1, column=1, padx=5, pady=5)
            
            ttk.Label(ai_frame, text="Defense:").grid(row=i*3+2, column=0, padx=5, pady=5)
            defense_scale = ttk.Scale(ai_frame, from_=1, to=10, orient=tk.HORIZONTAL, 
                                      value=self.ai_settings[profile]["defense"])
            defense_scale.grid(row=i*3+2, column=1, padx=5, pady=5)

        ttk.Button(ai_frame, text="Save AI Settings", 
                   command=lambda: self.save_ai_settings(aggression_scale.get(), defense_scale.get(), None)).grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    def setup_recording_tab(self):
        recording_frame = ttk.Frame(self.notebook)
        self.notebook.add(recording_frame, text='Recording')

        ttk.Button(recording_frame, text="Start Recording", command=self.start_recording_gui).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(recording_frame, text="Stop Recording", command=self.stop_recording_gui).grid(row=0, column=1, padx=5, pady=5)

        self.recorded_skills_list = tk.Listbox(recording_frame, width=40, height=10)
        self.recorded_skills_list.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def setup_visualization_tab(self):
        viz_frame = ttk.Frame(self.notebook)
        self.notebook.add(viz_frame, text='Visualization')

        self.canvas = tk.Canvas(viz_frame, width=400, height=400)
        self.canvas.pack()

        ttk.Button(viz_frame, text="Start Macro", command=self.start_macro_gui).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(viz_frame, text="Stop Macro", command=self.stop_macro_gui).pack(side=tk.RIGHT, padx=5, pady=5)

    def switch_profile_gui(self):
        new_profile = self.profile_var.get()
        if new_profile in self.profiles:
            self.current_profile = new_profile
            self.activation_key_var.set(self.profiles[self.current_profile].get('activation_key', ''))
            self.logger.info(f"Switched to profile: {new_profile}")
            messagebox.showinfo("Profile Switched", f"Switched to profile: {new_profile}")
        else:
            self.logger.error(f"Profile not found: {new_profile}")
            messagebox.showerror("Error", "Profile not found")

    def set_activation_key(self):
        new_key = self.activation_key_var.get()
        self.profiles[self.current_profile]['activation_key'] = new_key
        self.save_config()
        self.logger.info(f"Activation key set to: {new_key}")
        messagebox.showinfo("Activation Key Set", f"Activation key set to: {new_key}")

    def save_ai_settings(self, pve_aggression, pve_defense, pvp_aggression, pvp_defense, window):
        self.ai_settings["PVE"]["aggression"] = pve_aggression
        self.ai_settings["PVE"]["defense"] = pve_defense
        self.ai_settings["PVP"]["aggression"] = pvp_aggression
        self.ai_settings["PVP"]["defense"] = pvp_defense
        self.save_config()
        self.logger.info("AI settings saved")
        messagebox.showinfo("Settings Saved", "AI settings have been updated.")

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
            self.update_recorded_skills_list()
            self.logger.info("Recording stopped. New skill rotation saved.")
            messagebox.showinfo("Recording Stopped", "New skill rotation saved.")
        else:
            messagebox.showinfo("Not Recording", "Recording was not in progress.")

    def update_recorded_skills_list(self):
        self.recorded_skills_list.delete(0, tk.END)
        for skill in self.profiles[self.current_profile].get('skills', []):
            self.recorded_skills_list.insert(tk.END, f"Key: {skill['key']}, Cooldown: {skill['cooldown']}")

    def start_macro_gui(self):
        self.running = True
        self.logger.info(f"Macro activated for profile: {self.current_profile}")
        messagebox.showinfo("Macro Started", f"Macro activated for profile: {self.current_profile}")
        self.root.after(100, self.ai_rotate_skills)

    def stop_macro_gui(self):
        self.running = False
        self.logger.info("Macro deactivated")
        messagebox.showinfo("Macro Stopped", "Macro deactivated")

    def ai_rotate_skills(self):
        if self.running:
            current_time = time.time()
            possible_actions = []
            weights = []

            for key, data in self.ai_profiles[self.current_ai_profile].items():
                if current_time - data["last_use"] >= data["cooldown"]:
                    possible_actions.append(key)
                    weight = data["count"] * (current_time - data["last_use"]) * data["priority"]
                    weights.append(weight)

            if possible_actions:
                next_action = random.choices(possible_actions, weights=weights)[0]
                self.press_key(next_action)
                self.ai_profiles[self.current_ai_profile][next_action]["last_use"] = current_time
                self.visualize_skill_use(next_action)

            self.root.after(100, self.ai_rotate_skills)

    def press_key(self, key):
        # This method would normally use pyautogui.press(key), but for now we'll just log it
        self.logger.info(f"Pressed key: {key}")

    def visualize_skill_use(self, skill):
        self.canvas.delete("all")
        self.canvas.create_text(200, 200, text=f"Used Skill: {skill}", font=("Arial", 24))

    def save_config(self):
        config = {
            'current_profile': self.current_profile,
            'profiles': self.profiles,
            'ai_settings': self.ai_settings
        }
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        self.logger.info("Configuration saved")

    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                self.current_profile = config.get('current_profile', 'default')
                self.profiles = config.get('profiles', {'default': {}})
                self.ai_settings = config.get('ai_settings', {"PVE": {"aggression": 5, "defense": 5}, "PVP": {"aggression": 5, "defense": 5}})
            self.logger.info("Configuration loaded")
        except FileNotFoundError:
            self.logger.warning("Config file not found. Using default settings.")

    def run(self):
        self.load_config()
        self.root.mainloop()

if __name__ == "__main__":
    macro = SkillRotationMacro()
    macro.run()

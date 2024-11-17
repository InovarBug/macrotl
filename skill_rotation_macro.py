
import time
import json
import logging
from pynput import keyboard
import pyautogui
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
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
            self.ai_profiles = {"PVE": defaultdict(lambda: {"count": 0, "last_use": 0, "cooldown": 1.0, "priority": 1}),
                                "PVP": defaultdict(lambda: {"count": 0, "last_use": 0, "cooldown": 1.0, "priority": 1})}
            self.ai_settings = {"PVE": {"aggression": 5, "defense": 5}, "PVP": {"aggression": 5, "defense": 5}}
            self.last_action = None
            self.last_action_time = None
            self.auto_detect_mode = False
            self.setup_logging()
            self.load_config()
            self.setup_gui()
        except Exception as e:
            self.log_error("Error during initialization", e)
            raise

    # ... [previous methods remain unchanged] ...

    def setup_gui(self):
        try:
            self.root = tk.Tk()
            self.root.title("Skill Rotation Macro")
            self.root.geometry("600x500")

            # ... [previous GUI setup remains unchanged] ...

            ttk.Button(self.root, text="AI Settings", command=self.open_ai_settings).grid(row=9, column=0, columnspan=3, padx=5, pady=5)

            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        except Exception as e:
            self.log_error("Error setting up GUI", e)
            raise

    def open_ai_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("AI Settings")

        for profile in ["PVE", "PVP"]:
            ttk.Label(settings_window, text=f"{profile} Settings").grid(row=0, column=profile=="PVP", padx=5, pady=5)
            
            ttk.Label(settings_window, text="Aggression:").grid(row=1, column=profile=="PVP", padx=5, pady=5)
            aggression_scale = ttk.Scale(settings_window, from_=1, to=10, orient=tk.HORIZONTAL, 
                                         value=self.ai_settings[profile]["aggression"])
            aggression_scale.grid(row=2, column=profile=="PVP", padx=5, pady=5)
            
            ttk.Label(settings_window, text="Defense:").grid(row=3, column=profile=="PVP", padx=5, pady=5)
            defense_scale = ttk.Scale(settings_window, from_=1, to=10, orient=tk.HORIZONTAL, 
                                      value=self.ai_settings[profile]["defense"])
            defense_scale.grid(row=4, column=profile=="PVP", padx=5, pady=5)

            ttk.Button(settings_window, text=f"Set {profile} Skill Priorities", 
                       command=lambda p=profile: self.set_skill_priorities(p)).grid(row=5, column=profile=="PVP", padx=5, pady=5)

        ttk.Button(settings_window, text="Save", command=lambda: self.save_ai_settings(
            aggression_scale.get(), defense_scale.get(), settings_window)).grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    def save_ai_settings(self, pve_aggression, pve_defense, pvp_aggression, pvp_defense, window):
        self.ai_settings["PVE"]["aggression"] = pve_aggression
        self.ai_settings["PVE"]["defense"] = pve_defense
        self.ai_settings["PVP"]["aggression"] = pvp_aggression
        self.ai_settings["PVP"]["defense"] = pvp_defense
        self.save_config()
        window.destroy()
        messagebox.showinfo("Settings Saved", "AI settings have been updated.")

    def set_skill_priorities(self, profile):
        for skill in self.ai_profiles[profile]:
            priority = simpledialog.askinteger("Skill Priority", f"Set priority for skill '{skill}' (1-10):", 
                                               minvalue=1, maxvalue=10)
            if priority is not None:
                self.ai_profiles[profile][skill]["priority"] = priority
        self.save_config()
        messagebox.showinfo("Priorities Set", f"Skill priorities for {profile} have been updated.")

    def ai_rotate_skills(self):
        if self.running:
            current_time = time.time()
            possible_actions = []
            weights = []

            for key, data in self.ai_profiles[self.current_ai_profile].items():
                if current_time - data["last_use"] >= data["cooldown"]:
                    possible_actions.append(key)
                    # Calculate weight based on frequency, time since last use, and priority
                    weight = data["count"] * (current_time - data["last_use"]) * data["priority"]
                    
                    # Adjust weight based on aggression/defense settings
                    if self.ai_settings[self.current_ai_profile]["aggression"] > 5:
                        weight *= (self.ai_settings[self.current_ai_profile]["aggression"] / 5)
                    elif self.ai_settings[self.current_ai_profile]["defense"] > 5:
                        weight /= (self.ai_settings[self.current_ai_profile]["defense"] / 5)
                    
                    weights.append(weight)

            if possible_actions:
                next_action = random.choices(possible_actions, weights=weights)[0]
                pyautogui.press(next_action)
                self.logger.debug(f"AI pressed key: {next_action} (Profile: {self.current_ai_profile})")
                self.ai_profiles[self.current_ai_profile][next_action]["last_use"] = current_time

            self.root.after(100, self.ai_rotate_skills)  # Check every 100ms
        else:
            self.root.after(100, self.ai_rotate_skills)

    # ... [rest of the class remains unchanged] ...

if __name__ == "__main__":
    try:
        macro = SkillRotationMacro()
        macro.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        logging.error(f"Fatal error: {e}")
        sys.exit(1)

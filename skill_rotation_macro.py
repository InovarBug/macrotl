
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

import cv2
import numpy as np
from PIL import ImageGrab

# ... [rest of the imports and class definition] ...

class SkillRotationMacro:
    # ... [previous methods] ...

    def detect_pvp_pve(self):
        if self.auto_detect_mode:
            # Capture the screen
            screenshot = np.array(ImageGrab.grab(bbox=(0, 0, 1920, 1080)))
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

            # Define color ranges for PVP and PVE indicators
            lower_pvp = np.array([0, 0, 150])  # Adjusted red color range for PVP
            upper_pvp = np.array([50, 50, 255])
            lower_pve = np.array([0, 150, 0])  # Adjusted green color range for PVE
            upper_pve = np.array([50, 255, 50])

            # Create masks
            mask_pvp = cv2.inRange(screenshot, lower_pvp, upper_pvp)
            mask_pve = cv2.inRange(screenshot, lower_pve, upper_pve)

            # Count non-zero pixels in each mask
            pvp_pixels = cv2.countNonZero(mask_pvp)
            pve_pixels = cv2.countNonZero(mask_pve)

            # Determine the mode based on pixel count and a threshold
            threshold = 2000  # Adjusted threshold
            if pvp_pixels > pve_pixels and pvp_pixels > threshold:
                new_profile = "PVP"
            elif pve_pixels > pvp_pixels and pve_pixels > threshold:
                new_profile = "PVE"
            else:
                new_profile = self.current_ai_profile  # Keep current profile if unsure

            # Switch profile if needed
            if new_profile != self.current_ai_profile:
                self.current_ai_profile = new_profile
                self.logger.info(f"Auto-switched to {new_profile} profile")
                self.ai_profile_var.set(new_profile)

            # Schedule next detection
            self.root.after(2000, self.detect_pvp_pve)  # Check every 2 seconds

    # ... [rest of the class methods] ...

import json
import os

class SkillRotationMacro:
    # ... [previous methods] ...

    def export_ai_profile(self):
        profile_name = self.current_ai_profile
        data = {
            'ai_profile': self.ai_profiles[profile_name],
            'ai_settings': self.ai_settings[profile_name]
        }
        filename = f"{profile_name}_ai_profile.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        self.logger.info(f"AI profile exported to {filename}")
        messagebox.showinfo("Export Successful", f"AI profile exported to {filename}")

    def import_ai_profile(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                profile_name = os.path.splitext(os.path.basename(filename))[0].replace("_ai_profile", "")
                self.ai_profiles[profile_name] = defaultdict(lambda: {"count": 0, "last_use": 0, "cooldown": 1.0, "priority": 1})
                self.ai_profiles[profile_name].update(data['ai_profile'])
                self.ai_settings[profile_name] = data['ai_settings']
                self.logger.info(f"AI profile imported from {filename}")
                messagebox.showinfo("Import Successful", f"AI profile imported from {filename}")
            except Exception as e:
                self.log_error(f"Error importing AI profile from {filename}", e)
                messagebox.showerror("Import Failed", f"Failed to import AI profile: {str(e)}")

    def setup_gui(self):
        # ... [previous GUI setup] ...

        ttk.Button(self.root, text="Export AI Profile", command=self.export_ai_profile).grid(row=10, column=0, padx=5, pady=5)
        ttk.Button(self.root, text="Import AI Profile", command=self.import_ai_profile).grid(row=10, column=1, padx=5, pady=5)

        # ... [rest of GUI setup] ...

# ... [rest of the file] ...

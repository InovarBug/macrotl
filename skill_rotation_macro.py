
import time
import json
import logging
from pynput import keyboard
import pyautogui
import tkinter as tk
from tkinter import ttk, messagebox
import random
from collections import defaultdict

class SkillRotationMacro:
    def __init__(self):
        self.running = False
        self.recording = False
        self.learning = False
        self.current_profile = "default"
        self.current_ai_profile = "PVE"  # Default to PVE
        self.profiles = {}
        self.ai_profiles = {"PVE": defaultdict(lambda: defaultdict(int)),
                            "PVP": defaultdict(lambda: defaultdict(int))}
        self.last_action = None
        self.last_action_time = None
        self.setup_logging()
        self.load_config()
        self.setup_gui()

    # ... [previous methods remain unchanged] ...

    def setup_gui(self):
        # ... [previous GUI setup remains unchanged] ...

        ttk.Label(self.root, text="AI Profile:").grid(row=6, column=0, padx=5, pady=5)
        self.ai_profile_var = tk.StringVar(value=self.current_ai_profile)
        ttk.Combobox(self.root, textvariable=self.ai_profile_var, values=["PVE", "PVP"]).grid(row=6, column=1, padx=5, pady=5)
        ttk.Button(self.root, text="Switch AI Profile", command=self.switch_ai_profile).grid(row=6, column=2, padx=5, pady=5)

        ttk.Button(self.root, text="Start AI Learning", command=self.start_ai_learning).grid(row=7, column=0, padx=5, pady=5)
        ttk.Button(self.root, text="Stop AI Learning", command=self.stop_ai_learning).grid(row=7, column=1, padx=5, pady=5)
        ttk.Button(self.root, text="Start AI Macro", command=self.start_ai_macro).grid(row=7, column=2, padx=5, pady=5)

    def switch_ai_profile(self):
        new_profile = self.ai_profile_var.get()
        if new_profile in self.ai_profiles:
            self.current_ai_profile = new_profile
            self.logger.info(f"Switched to AI profile: {new_profile}")
            messagebox.showinfo("AI Profile Switched", f"Switched to AI profile: {new_profile}")
        else:
            messagebox.showerror("Error", "AI profile not found")

    def start_ai_learning(self):
        self.learning = True
        self.ai_profiles[self.current_ai_profile].clear()
        self.last_action = None
        self.last_action_time = None
        self.logger.info(f"AI learning started for {self.current_ai_profile} profile")
        messagebox.showinfo("AI Learning", f"AI learning mode started for {self.current_ai_profile} profile. Play normally and the AI will learn your skill rotation.")

    def stop_ai_learning(self):
        self.learning = False
        self.logger.info(f"AI learning stopped for {self.current_ai_profile} profile")
        messagebox.showinfo("AI Learning", f"AI learning mode stopped for {self.current_ai_profile} profile. The AI model has been updated.")

    def start_ai_macro(self):
        self.running = True
        self.logger.info(f"AI macro started using {self.current_ai_profile} profile")
        messagebox.showinfo("AI Macro", f"AI-controlled macro started using {self.current_ai_profile} profile. The AI will now attempt to replicate your skill rotation.")
        self.root.after(100, self.ai_rotate_skills)

    def ai_rotate_skills(self):
        if self.running:
            ai_model = self.ai_profiles[self.current_ai_profile]
            if self.last_action is None:
                possible_actions = list(ai_model.keys())
            else:
                possible_actions = list(ai_model[self.last_action].keys())

            if possible_actions:
                next_action = random.choices(
                    possible_actions,
                    weights=[ai_model[self.last_action][action] for action in possible_actions]
                )[0]
                pyautogui.press(next_action)
                self.logger.debug(f"AI pressed key: {next_action} (Profile: {self.current_ai_profile})")
                self.last_action = next_action

            self.root.after(1000, self.ai_rotate_skills)  # Adjust timing as needed
        else:
            self.root.after(100, self.ai_rotate_skills)

    def on_key_press(self, key):
        if self.recording:
            try:
                self.recorded_skills.append({'key': key.char, 'cooldown': 1.0})
                self.logger.debug(f"Recorded key: {key.char}")
            except AttributeError:
                pass

        if self.learning:
            try:
                current_time = time.time()
                if self.last_action is not None:
                    time_diff = current_time - self.last_action_time
                    self.ai_profiles[self.current_ai_profile][self.last_action][key.char] += 1
                    # You could also store timing information here

                self.last_action = key.char
                self.last_action_time = current_time
                self.logger.debug(f"AI learned key press: {key.char} (Profile: {self.current_ai_profile})")
            except AttributeError:
                pass

    # ... [rest of the class remains unchanged] ...

if __name__ == "__main__":
    macro = SkillRotationMacro()
    macro.run()

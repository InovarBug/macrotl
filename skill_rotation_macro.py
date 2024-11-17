
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

class SkillRotationMacro:
    def __init__(self):
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

    # ... [previous methods remain unchanged] ...

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
                    self.ai_profiles[self.current_ai_profile][key.char]["count"] += 1
                    self.ai_profiles[self.current_ai_profile][key.char]["last_use"] = current_time
                    self.ai_profiles[self.current_ai_profile][key.char]["cooldown"] = min(time_diff, self.ai_profiles[self.current_ai_profile][key.char]["cooldown"])

                self.last_action = key.char
                self.last_action_time = current_time
                self.logger.debug(f"AI learned key press: {key.char} (Profile: {self.current_ai_profile})")
            except AttributeError:
                pass

    def ai_rotate_skills(self):
        if self.running:
            current_time = time.time()
            possible_actions = []
            weights = []

            for key, data in self.ai_profiles[self.current_ai_profile].items():
                if current_time - data["last_use"] >= data["cooldown"]:
                    possible_actions.append(key)
                    # Calculate weight based on frequency and time since last use
                    weight = data["count"] * (current_time - data["last_use"])
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
    macro = SkillRotationMacro()
    macro.run()

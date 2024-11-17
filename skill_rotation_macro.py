
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
        self.profiles = {}
        self.ai_model = defaultdict(lambda: defaultdict(int))
        self.last_action = None
        self.last_action_time = None
        self.setup_logging()
        self.load_config()
        self.setup_gui()

    # ... [previous methods remain unchanged] ...

    def setup_gui(self):
        # ... [previous GUI setup remains unchanged] ...

        ttk.Button(self.root, text="Start AI Learning", command=self.start_ai_learning).grid(row=5, column=0, padx=5, pady=5)
        ttk.Button(self.root, text="Stop AI Learning", command=self.stop_ai_learning).grid(row=5, column=1, padx=5, pady=5)
        ttk.Button(self.root, text="Start AI Macro", command=self.start_ai_macro).grid(row=5, column=2, padx=5, pady=5)

    def start_ai_learning(self):
        self.learning = True
        self.ai_model.clear()
        self.last_action = None
        self.last_action_time = None
        self.logger.info("AI learning started")
        messagebox.showinfo("AI Learning", "AI learning mode started. Play normally and the AI will learn your skill rotation.")

    def stop_ai_learning(self):
        self.learning = False
        self.logger.info("AI learning stopped")
        messagebox.showinfo("AI Learning", "AI learning mode stopped. The AI model has been updated.")

    def start_ai_macro(self):
        self.running = True
        self.logger.info("AI macro started")
        messagebox.showinfo("AI Macro", "AI-controlled macro started. The AI will now attempt to replicate your skill rotation.")
        self.root.after(100, self.ai_rotate_skills)

    def ai_rotate_skills(self):
        if self.running:
            if self.last_action is None:
                possible_actions = list(self.ai_model.keys())
            else:
                possible_actions = list(self.ai_model[self.last_action].keys())

            if possible_actions:
                next_action = random.choices(
                    possible_actions,
                    weights=[self.ai_model[self.last_action][action] for action in possible_actions]
                )[0]
                pyautogui.press(next_action)
                self.logger.debug(f"AI pressed key: {next_action}")
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
                    self.ai_model[self.last_action][key.char] += 1
                    # You could also store timing information here

                self.last_action = key.char
                self.last_action_time = current_time
                self.logger.debug(f"AI learned key press: {key.char}")
            except AttributeError:
                pass

    # ... [rest of the class remains unchanged] ...

if __name__ == "__main__":
    macro = SkillRotationMacro()
    macro.run()

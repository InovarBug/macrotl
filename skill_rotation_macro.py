
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
        self.ai_profiles = {"PVE": defaultdict(lambda: defaultdict(int)),
                            "PVP": defaultdict(lambda: defaultdict(int))}
        self.last_action = None
        self.last_action_time = None
        self.auto_detect_mode = False
        self.setup_logging()
        self.load_config()
        self.setup_gui()

    # ... [previous methods remain unchanged] ...

    def setup_gui(self):
        # ... [previous GUI setup remains unchanged] ...

        ttk.Checkbutton(self.root, text="Auto-detect PVP/PVE", variable=tk.BooleanVar(value=self.auto_detect_mode), command=self.toggle_auto_detect).grid(row=8, column=0, columnspan=3, padx=5, pady=5)

    def toggle_auto_detect(self):
        self.auto_detect_mode = not self.auto_detect_mode
        if self.auto_detect_mode:
            self.start_auto_detect()
        else:
            self.stop_auto_detect()

    def start_auto_detect(self):
        self.logger.info("Auto-detect PVP/PVE mode started")
        self.root.after(1000, self.detect_pvp_pve)

    def stop_auto_detect(self):
        self.logger.info("Auto-detect PVP/PVE mode stopped")

    def detect_pvp_pve(self):
        if self.auto_detect_mode:
            # Capture the screen
            screenshot = np.array(ImageGrab.grab(bbox=(0, 0, 1920, 1080)))
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

            # Define color ranges for PVP and PVE indicators
            lower_pvp = np.array([0, 0, 100])  # Red color range for PVP
            upper_pvp = np.array([50, 50, 255])
            lower_pve = np.array([0, 100, 0])  # Green color range for PVE
            upper_pve = np.array([50, 255, 50])

            # Create masks
            mask_pvp = cv2.inRange(screenshot, lower_pvp, upper_pvp)
            mask_pve = cv2.inRange(screenshot, lower_pve, upper_pve)

            # Count non-zero pixels in each mask
            pvp_pixels = cv2.countNonZero(mask_pvp)
            pve_pixels = cv2.countNonZero(mask_pve)

            # Determine the mode based on pixel count
            if pvp_pixels > pve_pixels and pvp_pixels > 1000:  # Adjust threshold as needed
                new_profile = "PVP"
            elif pve_pixels > pvp_pixels and pve_pixels > 1000:  # Adjust threshold as needed
                new_profile = "PVE"
            else:
                new_profile = self.current_ai_profile  # Keep current profile if unsure

            # Switch profile if needed
            if new_profile != self.current_ai_profile:
                self.current_ai_profile = new_profile
                self.logger.info(f"Auto-switched to {new_profile} profile")
                self.ai_profile_var.set(new_profile)

            # Schedule next detection
            self.root.after(5000, self.detect_pvp_pve)  # Check every 5 seconds

    # ... [rest of the class remains unchanged] ...

if __name__ == "__main__":
    macro = SkillRotationMacro()
    macro.run()

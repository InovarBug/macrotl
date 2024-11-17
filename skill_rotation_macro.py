
import time
import json
import logging
from collections import defaultdict
import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import random
import cv2
import numpy as np
from PIL import ImageGrab, ImageTk
import threading

class ToolTip:
    # ... [ToolTip class implementation remains unchanged] ...

class SkillRotationMacro:
    def __init__(self):
        # ... [previous initialization code remains unchanged] ...
        self.detection_interval = 1.0  # Time in seconds between PVP/PVE detections
        self.detection_thread = None
        self.stop_detection = threading.Event()

    # ... [previous methods remain unchanged] ...

    def toggle_auto_detect(self):
        self.auto_detect_mode = self.auto_detect_var.get()
        if self.auto_detect_mode:
            self.start_detection_thread()
        else:
            self.stop_detection_thread()
        self.logger.info(f"Auto-detect PVP/PVE mode: {'ON' if self.auto_detect_mode else 'OFF'}")

    def start_detection_thread(self):
        self.stop_detection.clear()
        self.detection_thread = threading.Thread(target=self.detection_loop)
        self.detection_thread.start()

    def stop_detection_thread(self):
        if self.detection_thread:
            self.stop_detection.set()
            self.detection_thread.join()
            self.detection_thread = None

    def detection_loop(self):
        while not self.stop_detection.is_set():
            self.detect_pvp_pve()
            time.sleep(self.detection_interval)

    def detect_pvp_pve(self):
        try:
            # Capture only a specific region of the screen where the PVP/PVE indicator is likely to be
            screenshot = np.array(ImageGrab.grab(bbox=(0, 0, 300, 300)))
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

            # Use more specific color ranges for PVP and PVE indicators
            lower_pvp = np.array([0, 0, 150])
            upper_pvp = np.array([50, 50, 255])
            lower_pve = np.array([0, 150, 0])
            upper_pve = np.array([50, 255, 50])

            mask_pvp = cv2.inRange(screenshot, lower_pvp, upper_pvp)
            mask_pve = cv2.inRange(screenshot, lower_pve, upper_pve)

            pvp_pixels = cv2.countNonZero(mask_pvp)
            pve_pixels = cv2.countNonZero(mask_pve)

            threshold = 500  # Adjusted threshold

            if pvp_pixels > threshold and pvp_pixels > pve_pixels:
                new_profile = "PVP"
            elif pve_pixels > threshold and pve_pixels > pvp_pixels:
                new_profile = "PVE"
            else:
                return  # No change if unsure

            if new_profile != self.current_ai_profile:
                self.current_ai_profile = new_profile
                self.logger.info(f"Auto-switched to {new_profile} profile")
                self.root.after(0, self.update_profile_display)
        except Exception as e:
            self.logger.error(f"Error in PVP/PVE detection: {str(e)}")

    def update_profile_display(self):
        # Update any UI elements that display the current profile
        self.current_profile_label.config(text=f"Current Profile: {self.current_ai_profile}")

    def on_closing(self):
        self.stop_detection_thread()
        self.save_config()
        self.root.destroy()

    # ... [rest of the class implementation remains unchanged] ...

if __name__ == "__main__":
    macro = SkillRotationMacro()
    macro.run()

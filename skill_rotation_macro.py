
import time
import json
import logging
from collections import defaultdict
import tkinter as tk
from tkinter import ttk, messagebox
import random
import cv2
import numpy as np
from PIL import ImageGrab, ImageTk

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class SkillRotationMacro:
    def __init__(self):
        # ... [previous initialization code] ...
        self.skill_colors = {}
        self.setup_logging()
        self.setup_gui()

    # ... [previous methods] ...

    def setup_profiles_tab(self):
        profiles_frame = ttk.Frame(self.notebook)
        self.notebook.add(profiles_frame, text='Profiles')

        ttk.Label(profiles_frame, text="Current Profile:").grid(row=0, column=0, padx=5, pady=5)
        self.profile_var = tk.StringVar(value=self.current_profile)
        profile_combo = ttk.Combobox(profiles_frame, textvariable=self.profile_var, values=list(self.profiles.keys()))
        profile_combo.grid(row=0, column=1, padx=5, pady=5)
        switch_profile_btn = ttk.Button(profiles_frame, text="Switch Profile", command=self.switch_profile_gui)
        switch_profile_btn.grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(profiles_frame, text="Activation Key:").grid(row=1, column=0, padx=5, pady=5)
        self.activation_key_var = tk.StringVar(value=self.profiles[self.current_profile].get('activation_key', ''))
        activation_key_entry = ttk.Entry(profiles_frame, textvariable=self.activation_key_var)
        activation_key_entry.grid(row=1, column=1, padx=5, pady=5)
        set_key_btn = ttk.Button(profiles_frame, text="Set Key", command=self.set_activation_key)
        set_key_btn.grid(row=1, column=2, padx=5, pady=5)

        # Add tooltips
        ToolTip(switch_profile_btn, "Switch to the selected profile")
        ToolTip(activation_key_entry, "Enter the key that will activate this profile")
        ToolTip(set_key_btn, "Save the entered activation key for this profile")

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

            # Add tooltips
            ToolTip(aggression_scale, f"Set the aggression level for {profile} (1-10)")
            ToolTip(defense_scale, f"Set the defense level for {profile} (1-10)")

        save_ai_btn = ttk.Button(ai_frame, text="Save AI Settings", 
                   command=lambda: self.save_ai_settings(aggression_scale.get(), defense_scale.get(), None))
        save_ai_btn.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        ToolTip(save_ai_btn, "Save the current AI settings for both PVE and PVP")

    def setup_recording_tab(self):
        recording_frame = ttk.Frame(self.notebook)
        self.notebook.add(recording_frame, text='Recording')

        start_rec_btn = ttk.Button(recording_frame, text="Start Recording", command=self.start_recording_gui)
        start_rec_btn.grid(row=0, column=0, padx=5, pady=5)
        stop_rec_btn = ttk.Button(recording_frame, text="Stop Recording", command=self.stop_recording_gui)
        stop_rec_btn.grid(row=0, column=1, padx=5, pady=5)

        self.recorded_skills_list = tk.Listbox(recording_frame, width=40, height=10)
        self.recorded_skills_list.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Add tooltips
        ToolTip(start_rec_btn, "Start recording a new skill sequence")
        ToolTip(stop_rec_btn, "Stop recording and save the skill sequence")
        ToolTip(self.recorded_skills_list, "List of recorded skills in the current sequence")

    def setup_visualization_tab(self):
        # ... [previous visualization setup code] ...

        ToolTip(self.canvas, "Visual representation of skill rotation")
        ToolTip(self.auto_detect_var, "Automatically switch between PVP and PVE profiles based on screen detection")

    # ... [rest of the class implementation] ...

if __name__ == "__main__":
    macro = SkillRotationMacro()
    macro.run()

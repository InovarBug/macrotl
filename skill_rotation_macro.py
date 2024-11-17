
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

class SkillRotationMacro:
    def __init__(self):
        # ... [previous initialization code] ...
        self.skill_colors = {}  # To store unique colors for each skill
        self.setup_logging()
        self.setup_gui()

    # ... [previous methods] ...

    def setup_visualization_tab(self):
        viz_frame = ttk.Frame(self.notebook)
        self.notebook.add(viz_frame, text='Visualization')

        self.canvas = tk.Canvas(viz_frame, width=400, height=400, bg='white')
        self.canvas.pack(pady=10)

        control_frame = ttk.Frame(viz_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(control_frame, text="Start Macro", command=self.start_macro_gui).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Stop Macro", command=self.stop_macro_gui).pack(side=tk.LEFT, padx=5)
        
        self.auto_detect_var = tk.BooleanVar(value=self.auto_detect_mode)
        ttk.Checkbutton(control_frame, text="Auto-detect PVP/PVE", variable=self.auto_detect_var, 
                        command=self.toggle_auto_detect).pack(side=tk.LEFT, padx=5)

        self.current_profile_label = ttk.Label(viz_frame, text=f"Current Profile: {self.current_ai_profile}")
        self.current_profile_label.pack(pady=5)

        self.skill_info_frame = ttk.Frame(viz_frame)
        self.skill_info_frame.pack(fill=tk.X, padx=10, pady=5)

    def visualize_skill_use(self, skill):
        self.canvas.delete("all")
        
        # Create a circular layout for skills
        center_x, center_y = 200, 200
        radius = 150
        num_skills = len(self.ai_profiles[self.current_ai_profile])
        angle_step = 360 / num_skills

        for i, (skill_name, skill_data) in enumerate(self.ai_profiles[self.current_ai_profile].items()):
            angle = i * angle_step
            x = center_x + radius * np.cos(np.radians(angle))
            y = center_y + radius * np.sin(np.radians(angle))
            
            # Assign a unique color to each skill if not already assigned
            if skill_name not in self.skill_colors:
                self.skill_colors[skill_name] = f'#{random.randint(0, 0xFFFFFF):06x}'

            color = self.skill_colors[skill_name]
            
            # Draw skill circle
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=color)
            self.canvas.create_text(x, y, text=skill_name, font=("Arial", 10, "bold"))

            # Highlight the used skill
            if skill_name == skill:
                self.canvas.create_oval(x-25, y-25, x+25, y+25, outline="red", width=3)

        # Update skill info
        for widget in self.skill_info_frame.winfo_children():
            widget.destroy()

        for skill_name, skill_data in self.ai_profiles[self.current_ai_profile].items():
            color = self.skill_colors[skill_name]
            ttk.Label(self.skill_info_frame, text=f"{skill_name}: ", foreground=color).pack(side=tk.LEFT, padx=2)
            ttk.Label(self.skill_info_frame, text=f"Count: {skill_data['count']}, ").pack(side=tk.LEFT)
            ttk.Label(self.skill_info_frame, text=f"Priority: {skill_data['priority']}").pack(side=tk.LEFT, padx=(0, 10))

    def update_profile_display(self):
        self.current_profile_label.config(text=f"Current Profile: {self.current_ai_profile}")

    # ... [rest of the class implementation] ...

if __name__ == "__main__":
    macro = SkillRotationMacro()
    macro.run()

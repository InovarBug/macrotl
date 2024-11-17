
import unittest
import tkinter as tk
from unittest.mock import patch, MagicMock
from skill_rotation_macro import SkillRotationMacro
import os
import json

class TestSkillRotationMacro(unittest.TestCase):
    def setUp(self):
        self.macro = SkillRotationMacro()

    def test_profile_switching(self):
        self.macro.current_profile = "default"
        self.macro.profiles = {"default": {}, "profile1": {}}
        self.macro.profile_var = tk.StringVar(value="profile1")
        self.macro.switch_profile_gui()
        self.assertEqual(self.macro.current_profile, "profile1")

    def test_ai_learning(self):
        self.macro.start_ai_learning()
        self.assertTrue(self.macro.learning)
        self.macro.stop_ai_learning()
        self.assertFalse(self.macro.learning)

    def test_ai_execution(self):
        self.macro.start_ai_macro()
        self.assertTrue(self.macro.running)
        self.macro.stop_macro_gui()
        self.assertFalse(self.macro.running)

    def test_pvp_pve_detection(self):
        self.macro.toggle_auto_detect()
        self.assertTrue(self.macro.auto_detect_mode)
        self.macro.toggle_auto_detect()
        self.assertFalse(self.macro.auto_detect_mode)

    def test_ai_settings(self):
        self.macro.ai_settings = {"PVE": {"aggression": 5, "defense": 5}, "PVP": {"aggression": 5, "defense": 5}}
        self.macro.save_ai_settings(7, 3, 8, 2, None)
        self.assertEqual(self.macro.ai_settings["PVE"]["aggression"], 7)
        self.assertEqual(self.macro.ai_settings["PVE"]["defense"], 3)
        self.assertEqual(self.macro.ai_settings["PVP"]["aggression"], 8)
        self.assertEqual(self.macro.ai_settings["PVP"]["defense"], 2)

    @patch('skill_rotation_macro.messagebox.showinfo')
    def test_export_ai_profile(self, mock_showinfo):
        self.macro.current_ai_profile = "PVE"
        self.macro.ai_profiles = {"PVE": {"skill1": {"count": 5, "last_use": 100, "cooldown": 1.0, "priority": 2}}}
        self.macro.ai_settings = {"PVE": {"aggression": 7, "defense": 3}}
        self.macro.export_ai_profile()
        
        filename = "PVE_ai_profile.json"
        self.assertTrue(os.path.exists(filename))
        
        with open(filename, 'r') as f:
            data = json.load(f)
        
        self.assertEqual(data['ai_profile']['skill1']['count'], 5)
        self.assertEqual(data['ai_settings']['aggression'], 7)
        
        os.remove(filename)

    @patch('skill_rotation_macro.filedialog.askopenfilename')
    @patch('skill_rotation_macro.messagebox.showinfo')
    def test_import_ai_profile(self, mock_showinfo, mock_askopenfilename):
        test_profile = {
            'ai_profile': {"skill1": {"count": 10, "last_use": 200, "cooldown": 2.0, "priority": 3}},
            'ai_settings': {"aggression": 8, "defense": 2}
        }
        
        filename = "test_profile.json"
        with open(filename, 'w') as f:
            json.dump(test_profile, f)
        
        mock_askopenfilename.return_value = filename
        
        self.macro.import_ai_profile()
        
        self.assertEqual(self.macro.ai_profiles['test']['skill1']['count'], 10)
        self.assertEqual(self.macro.ai_settings['test']['aggression'], 8)
        
        os.remove(filename)

    def test_on_key_press(self):
        self.macro.learning = True
        self.macro.current_ai_profile = "PVE"
        mock_key = MagicMock()
        mock_key.char = 'a'
        self.macro.on_key_press(mock_key)
        self.assertIn('a', self.macro.ai_profiles["PVE"])

    def test_ai_rotate_skills(self):
        self.macro.running = True
        self.macro.current_ai_profile = "PVE"
        self.macro.ai_profiles["PVE"] = {"skill1": {"count": 5, "last_use": 0, "cooldown": 1.0, "priority": 2}}
        self.macro.ai_settings["PVE"] = {"aggression": 5, "defense": 5}
        
        with patch('skill_rotation_macro.pyautogui.press') as mock_press:
            self.macro.ai_rotate_skills()
            mock_press.assert_called_once_with("skill1")

if __name__ == '__main__':
    unittest.main()

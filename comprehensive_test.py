
import unittest
from unittest.mock import patch, MagicMock
import json
import os

# Mock the modules that require graphical environment
import sys
sys.modules['tkinter'] = MagicMock()
sys.modules['pynput'] = MagicMock()
sys.modules['pyautogui'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['PIL'] = MagicMock()

from skill_rotation_macro import SkillRotationMacro

class TestSkillRotationMacro(unittest.TestCase):
    def setUp(self):
        self.macro = SkillRotationMacro()

    def test_profile_switching(self):
        self.macro.current_profile = "default"
        self.macro.profiles = {"default": {}, "profile1": {}}
        self.macro.profile_var = MagicMock()
        self.macro.profile_var.get.return_value = "profile1"
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

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('json.dump')
    def test_export_ai_profile(self, mock_json_dump, mock_open):
        self.macro.current_ai_profile = "PVE"
        self.macro.ai_profiles = {"PVE": {"skill1": {"count": 5, "last_use": 100, "cooldown": 1.0, "priority": 2}}}
        self.macro.ai_settings = {"PVE": {"aggression": 7, "defense": 3}}
        self.macro.export_ai_profile()
        
        mock_open.assert_called_once_with("PVE_ai_profile.json", 'w')
        mock_json_dump.assert_called_once()

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='{"ai_profile": {"skill1": {"count": 10, "last_use": 200, "cooldown": 2.0, "priority": 3}}, "ai_settings": {"aggression": 8, "defense": 2}}')
    def test_import_ai_profile(self, mock_open):
        self.macro.import_ai_profile()
        
        self.assertEqual(self.macro.ai_profiles['test']['skill1']['count'], 10)
        self.assertEqual(self.macro.ai_settings['test']['aggression'], 8)

    def test_on_key_press(self):
        self.macro.learning = True
        self.macro.current_ai_profile = "PVE"
        mock_key = MagicMock()
        mock_key.char = 'a'
        self.macro.on_key_press(mock_key)
        self.assertIn('a', self.macro.ai_profiles["PVE"])

    @patch('skill_rotation_macro.pyautogui.press')
    def test_ai_rotate_skills(self, mock_press):
        self.macro.running = True
        self.macro.current_ai_profile = "PVE"
        self.macro.ai_profiles["PVE"] = {"skill1": {"count": 5, "last_use": 0, "cooldown": 1.0, "priority": 2}}
        self.macro.ai_settings["PVE"] = {"aggression": 5, "defense": 5}
        
        self.macro.ai_rotate_skills()
        mock_press.assert_called_once_with("skill1")

if __name__ == '__main__':
    unittest.main()

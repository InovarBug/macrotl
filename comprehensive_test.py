
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

    def test_initialization(self):
        self.assertFalse(self.macro.running)
        self.assertFalse(self.macro.recording)
        self.assertFalse(self.macro.learning)
        self.assertEqual(self.macro.current_profile, "default")
        self.assertEqual(self.macro.current_ai_profile, "PVE")
        self.assertIn("PVE", self.macro.ai_profiles)
        self.assertIn("PVP", self.macro.ai_profiles)

    def test_ai_settings(self):
        self.macro.save_ai_settings(7, 3, 8, 2, None)
        self.assertEqual(self.macro.ai_settings["PVE"]["aggression"], 7)
        self.assertEqual(self.macro.ai_settings["PVE"]["defense"], 3)
        self.assertEqual(self.macro.ai_settings["PVP"]["aggression"], 8)
        self.assertEqual(self.macro.ai_settings["PVP"]["defense"], 2)

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('json.dump')
    def test_save_config(self, mock_json_dump, mock_open):
        self.macro.save_config()
        mock_open.assert_called_once_with('config.json', 'w')
        mock_json_dump.assert_called_once()

    def test_set_skill_priorities(self):
        with patch('tkinter.simpledialog.askinteger', return_value=5):
            self.macro.set_skill_priorities("PVE")
        self.assertEqual(self.macro.ai_profiles["PVE"]["skill1"]["priority"], 5)

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


import unittest
import tkinter as tk
from skill_rotation_macro import SkillRotationMacro

class TestSkillRotationMacro(unittest.TestCase):
    def setUp(self):
        self.macro = SkillRotationMacro()

    def test_profile_switching(self):
        self.macro.current_profile = "default"
        self.macro.switch_profile_gui()
        self.assertNotEqual(self.macro.current_profile, "default")

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
        initial_aggression = self.macro.ai_settings["PVE"]["aggression"]
        self.macro.save_ai_settings(7, 3, 8, 2, None)
        self.assertEqual(self.macro.ai_settings["PVE"]["aggression"], 7)
        self.assertEqual(self.macro.ai_settings["PVE"]["defense"], 3)
        self.assertEqual(self.macro.ai_settings["PVP"]["aggression"], 8)
        self.assertEqual(self.macro.ai_settings["PVP"]["defense"], 2)

if __name__ == '__main__':
    unittest.main()

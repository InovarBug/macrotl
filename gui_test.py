
import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from skill_rotation_macro import SkillRotationMacro

class TestSkillRotationMacroGUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.macro = SkillRotationMacro()

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def test_initial_setup(self):
        self.assertIsNotNone(self.macro.notebook)
        self.assertEqual(self.macro.notebook.index("end"), 4)  # Check if all 4 tabs are present

    def test_profiles_tab(self):
        profiles_tab = self.macro.notebook.nametowidget(self.macro.notebook.tabs()[0])
        self.assertIsNotNone(profiles_tab.winfo_children())
        
        # Test profile switching
        self.macro.profile_var.set("test_profile")
        self.macro.switch_profile_gui()
        self.assertEqual(self.macro.current_profile, "test_profile")

    def test_ai_settings_tab(self):
        ai_tab = self.macro.notebook.nametowidget(self.macro.notebook.tabs()[1])
        self.assertIsNotNone(ai_tab.winfo_children())
        
        # Test saving AI settings
        with patch.object(self.macro, 'save_config') as mock_save:
            self.macro.save_ai_settings(7, 3, 8, 2, None)
            self.assertEqual(self.macro.ai_settings["PVE"]["aggression"], 7)
            self.assertEqual(self.macro.ai_settings["PVE"]["defense"], 3)
            self.assertEqual(self.macro.ai_settings["PVP"]["aggression"], 8)
            self.assertEqual(self.macro.ai_settings["PVP"]["defense"], 2)
            mock_save.assert_called_once()

    def test_recording_tab(self):
        recording_tab = self.macro.notebook.nametowidget(self.macro.notebook.tabs()[2])
        self.assertIsNotNone(recording_tab.winfo_children())
        
        # Test recording functionality
        self.macro.start_recording_gui()
        self.assertTrue(self.macro.recording)
        self.macro.stop_recording_gui()
        self.assertFalse(self.macro.recording)

    def test_visualization_tab(self):
        viz_tab = self.macro.notebook.nametowidget(self.macro.notebook.tabs()[3])
        self.assertIsNotNone(viz_tab.winfo_children())
        
        # Test macro start/stop
        with patch.object(self.macro, 'ai_rotate_skills'):
            self.macro.start_macro_gui()
            self.assertTrue(self.macro.running)
            self.macro.stop_macro_gui()
            self.assertFalse(self.macro.running)

    def test_skill_rotation(self):
        with patch('pyautogui.press') as mock_press:
            self.macro.current_ai_profile = "PVE"
            self.macro.ai_profiles["PVE"] = {"skill1": {"count": 5, "last_use": 0, "cooldown": 1.0, "priority": 2}}
            self.macro.ai_settings["PVE"] = {"aggression": 5, "defense": 5}
            self.macro.running = True
            self.macro.ai_rotate_skills()
            mock_press.assert_called_once_with("skill1")

    def test_error_handling(self):
        with self.assertLogs(level='ERROR') as cm:
            self.macro.log_error("Test error", Exception("Test exception"))
        self.assertIn("Test error", cm.output[0])
        self.assertIn("Test exception", cm.output[0])

if __name__ == '__main__':
    unittest.main()

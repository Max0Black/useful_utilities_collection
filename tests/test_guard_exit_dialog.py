import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import unittest
from PySide6.QtWidgets import QApplication

from useful_utilities_collection.ui.guard_exit_dialog import GuardExitDialog


app = QApplication.instance() or QApplication(sys.argv)


class TestGuardExitDialog(unittest.TestCase):
    def test_dialog_creation_and_buttons(self):
        dialog = GuardExitDialog()
        self.assertEqual(dialog.objectName(), "GuardExitDialog")
        self.assertEqual(dialog.cancel_button.objectName(), "ExitCancelButton")
        self.assertEqual(dialog.quit_button.objectName(), "ExitQuitButton")
        self.assertEqual(dialog.cancel_button.width(), dialog.quit_button.width())


if __name__ == "__main__":
    unittest.main()

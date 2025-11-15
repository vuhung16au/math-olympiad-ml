"""
MathHeart Player - Main Entry Point
"""

import sys
import os

# Add parent directory to path so we can import mathheart_player
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from PyQt6.QtWidgets import QApplication
from mathheart_player.ui.main_window import MainWindow


def main():
    """Main entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("MathHeart Player")
    app.setOrganizationName("MathHeart")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()


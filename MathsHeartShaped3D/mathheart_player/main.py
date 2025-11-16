"""
MathHeart Player - Main Entry Point
"""

import sys
import os
import argparse
import logging

# Add parent directory to path so we can import mathheart_player
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from PyQt6.QtWidgets import QApplication
from mathheart_player.ui.main_window import MainWindow
from mathheart_player.utils.logger import setup_logging


def main():
    """Main entry point."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="MathHeart Player - Media player with 3D heart visualization")
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable DEBUG level console logging'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose INFO messages'
    )
    args = parser.parse_args()
    
    # Setup logging before creating application
    setup_logging(debug_mode=args.debug, verbose_mode=args.verbose)
    logger = logging.getLogger(__name__)
    
    logger.info("Application starting")
    
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("MathHeart Player")
        app.setOrganizationName("MathHeart")
        
        logger.info("QApplication created")
        
        window = MainWindow()
        logger.info("MainWindow created")
        
        window.show()
        logger.info("MainWindow shown - application ready")
        
        exit_code = app.exec()
        logger.info(f"Application exiting with code: {exit_code}")
        
        sys.exit(exit_code)
    except Exception as e:
        logger.critical(f"Critical error during application startup: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()


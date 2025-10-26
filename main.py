#!/usr/bin/env python3
"""
AI Corrector - Main Entry Point

This is the main entry point for the AI Corrector application.
Run this file to start the application.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ui.main_window import App


def main():
    """Main entry point for the application"""
    print("AI Corrector v2.3 - Starting application...")
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()

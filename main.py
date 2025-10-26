#!/usr/bin/env python3
"""
AI Corrector - Main Entry Point
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ui.main_window import App
import customtkinter as ctk
from PIL import Image, ImageTk


def resource_path(relative_path):
    """Get absolute path to resource (works for PyInstaller and normal run)"""
    if hasattr(sys, '_MEIPASS'):
        # Running from PyInstaller bundle
        base_path = sys._MEIPASS
    else:
        # Running from source
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def main():
    """Main entry point for the application"""
    print("AI Corrector v2.3 - Starting application...")

    app = App()

    # --- Set the window icon ---
    try:
        ico_path = resource_path("assets/app_logo.ico")
        png_path = resource_path("assets/app_logo.png")

        if os.path.exists(ico_path):
            app.iconbitmap(ico_path)
        elif os.path.exists(png_path):
            icon_image = ImageTk.PhotoImage(Image.open(png_path))
            app.iconphoto(False, icon_image)
        else:
            print("⚠️ No icon found in assets folder.")
    except Exception as e:
        print(f"Error loading icon: {e}")

    app.mainloop()


if __name__ == "__main__":
    main()

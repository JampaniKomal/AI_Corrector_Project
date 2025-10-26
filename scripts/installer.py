#!/usr/bin/env python3
"""
AI Corrector - Custom Installer
Modern black and white theme installer
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
import os
import shutil
import sys
from pathlib import Path

class Installer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Corrector Installer")
        self.geometry("600x500")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        
        self.install_path = Path(os.path.expanduser("~")) / "AppData" / "Local" / "AICorrector"
        self.is_installing = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="#1C1C1C", corner_radius=0)
        header_frame.pack(fill="x", padx=0, pady=0)
        
        ctk.CTkLabel(
            header_frame,
            text="AI Corrector",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FFFFFF"
        ).pack(pady=20, padx=20, anchor="w")
        
        ctk.CTkLabel(
            header_frame,
            text="v2.3.0 - Custom Installer",
            font=ctk.CTkFont(size=12),
            text_color="#AAAAAA"
        ).pack(pady=(0, 20), padx=20, anchor="w")
        
        # Main content
        content_frame = ctk.CTkFrame(self, fg_color="#000000")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Info text
        info_text = "This will install AI Corrector on your computer.\n\nInstallation Location:"
        ctk.CTkLabel(
            content_frame,
            text=info_text,
            font=ctk.CTkFont(size=13),
            text_color="#FFFFFF",
            justify="left"
        ).pack(anchor="w", pady=(0, 15))
        
        # Path display
        path_frame = ctk.CTkFrame(content_frame, fg_color="#1C1C1C", corner_radius=5)
        path_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            path_frame,
            text=str(self.install_path),
            font=ctk.CTkFont(size=11),
            text_color="#AAAAAA"
        ).pack(padx=15, pady=12, anchor="w")
        
        # Options
        self.create_desktop_var = tk.BooleanVar(value=True)
        
        ctk.CTkCheckBox(
            content_frame,
            text="Create Desktop Shortcut",
            variable=self.create_desktop_var,
            font=ctk.CTkFont(size=12),
            text_color="#FFFFFF",
            border_color="#FFFFFF",
            checkmark_color="#000000",
            fg_color="#FFFFFF"
        ).pack(anchor="w", pady=5)
        
        # Progress bar (hidden initially)
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ctk.CTkProgressBar(
            content_frame,
            variable=self.progress_var,
            fg_color="#1C1C1C",
            progress_color="#FFFFFF",
            height=6,
            corner_radius=3
        )
        
        # Status label
        self.status_label = ctk.CTkLabel(
            content_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="#AAAAAA"
        )
        
        # Buttons frame
        button_frame = ctk.CTkFrame(self, fg_color="#000000")
        button_frame.pack(fill="x", padx=20, pady=20)
        button_frame.grid_columnconfigure(1, weight=1)
        
        self.cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1C1C1C",
            text_color="#FFFFFF",
            hover_color="#333333",
            width=100,
            command=self.cancel_install
        )
        self.cancel_btn.grid(row=0, column=0, padx=5)
        
        self.install_btn = ctk.CTkButton(
            button_frame,
            text="Install",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#FFFFFF",
            text_color="#000000",
            hover_color="#E0E0E0",
            width=150,
            command=self.start_install
        )
        self.install_btn.grid(row=0, column=2, padx=5)
        
        self.protocol("WM_DELETE_WINDOW", self.cancel_install)
        
    def start_install(self):
        if self.is_installing:
            return
        
        self.install_btn.configure(state="disabled")
        self.cancel_btn.configure(state="disabled")
        self.is_installing = True
        
        # Show progress
        self.progress_bar.pack(fill="x", pady=(0, 10))
        self.status_label.pack(anchor="w", pady=(0, 10))
        
        thread = threading.Thread(target=self.run_install, daemon=True)
        thread.start()
        
    def run_install(self):
        try:
            # Get executable path
            if getattr(sys, 'frozen', False):
                exe_source = os.path.join(sys._MEIPASS, "AICorrector.exe")
            else:
                # During development, look for dist folder
                exe_source = os.path.join(os.path.dirname(__file__), "..", "dist", "AICorrector.exe")
            
            if not os.path.exists(exe_source):
                self.after(0, self.show_error, "Could not find AICorrector.exe")
                return
            
            # Create install directory
            self.after(0, self.update_progress, 10, "Creating installation directory...")
            self.install_path.mkdir(parents=True, exist_ok=True)
            
            # Copy executable
            self.after(0, self.update_progress, 30, "Installing application...")
            exe_dest = self.install_path / "AICorrector.exe"
            shutil.copy2(exe_source, exe_dest)
            
            # Create desktop shortcut if requested
            if self.create_desktop_var.get():
                self.after(0, self.update_progress, 70, "Creating shortcuts...")
                self.create_desktop_shortcut()
            
            # Create Start Menu shortcut
            self.after(0, self.update_progress, 85, "Finalizing installation...")
            self.create_startmenu_shortcut()
            
            self.after(0, self.update_progress, 100, "Installation complete!")
            self.after(1000, self.installation_complete)
            
        except Exception as e:
            self.after(0, self.show_error, f"Installation failed: {str(e)}")
            
    def update_progress(self, value, status):
        self.progress_var.set(value / 100)
        self.status_label.configure(text=status)
        
    def show_error(self, message):
        messagebox.showerror("Installation Error", message)
        self.is_installing = False
        self.install_btn.configure(state="normal")
        self.cancel_btn.configure(state="normal")
        
    def installation_complete(self):
        response = messagebox.showinfo(
            "Installation Complete",
            "AI Corrector has been successfully installed!\n\nWould you like to launch it now?"
        )
        if response == "ok":
            os.startfile(self.install_path / "AICorrector.exe")
        self.quit()
        
    def create_desktop_shortcut(self):
        try:
            import win32com.client
            desktop = Path.home() / "Desktop"
            shortcut_path = desktop / "AI Corrector.lnk"
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortcut(str(shortcut_path))
            shortcut.TargetPath = str(self.install_path / "AICorrector.exe")
            shortcut.IconLocation = str(self.install_path / "AICorrector.exe")
            shortcut.save()
        except:
            # Fallback if win32com not available
            pass
            
    def create_startmenu_shortcut(self):
        try:
            import win32com.client
            start_menu = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs"
            shortcut_path = start_menu / "AI Corrector.lnk"
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortcut(str(shortcut_path))
            shortcut.TargetPath = str(self.install_path / "AICorrector.exe")
            shortcut.IconLocation = str(self.install_path / "AICorrector.exe")
            shortcut.save()
        except:
            pass
            
    def cancel_install(self):
        if self.is_installing:
            messagebox.showwarning("Installation in Progress", "Cannot cancel during installation.")
            return
        self.quit()


if __name__ == "__main__":
    app = Installer()
    app.mainloop()

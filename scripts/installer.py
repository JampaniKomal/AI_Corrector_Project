#!/usr/bin/env python3
"""
AI Corrector - Custom Installer
Modern black and white theme installer with wizard steps
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
        self.geometry("700x600")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        
        self.install_path = Path(os.path.expanduser("~")) / "AppData" / "Local" / "AICorrector"
        self.is_installing = False
        self.current_step = 0
        self.steps = ["Welcome", "Installation Options", "Installation", "Finish"]
        
        self.setup_ui()
        self.show_step(0)
        
    def setup_ui(self):
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="#1C1C1C", corner_radius=0)
        self.header_frame.pack(fill="x", padx=0, pady=0)
        
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="AI Corrector",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FFFFFF"
        )
        self.title_label.pack(pady=20, padx=20, anchor="w")
        
        self.step_label = ctk.CTkLabel(
            self.header_frame,
            text="Step 1 of 4 - Welcome",
            font=ctk.CTkFont(size=12),
            text_color="#AAAAAA"
        )
        self.step_label.pack(pady=(0, 20), padx=20, anchor="w")
        
        # Content area
        self.content_frame = ctk.CTkFrame(self, fg_color="#000000")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Buttons frame
        button_frame = ctk.CTkFrame(self, fg_color="#000000")
        button_frame.pack(fill="x", padx=20, pady=20)
        button_frame.grid_columnconfigure(1, weight=1)
        
        self.back_btn = ctk.CTkButton(
            button_frame,
            text="Back",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1C1C1C",
            text_color="#FFFFFF",
            hover_color="#333333",
            width=100,
            command=self.go_back
        )
        self.back_btn.grid(row=0, column=0, padx=5)
        
        self.next_btn = ctk.CTkButton(
            button_frame,
            text="Next",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#FFFFFF",
            text_color="#000000",
            hover_color="#E0E0E0",
            width=100,
            command=self.go_next
        )
        self.next_btn.grid(row=0, column=2, padx=5)
        
        self.protocol("WM_DELETE_WINDOW", self.cancel_install)
        
    def show_step(self, step_num):
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        self.current_step = step_num
        self.step_label.configure(text=f"Step {step_num + 1} of 4 - {self.steps[step_num]}")
        
        if step_num == 0:
            self.show_welcome()
        elif step_num == 1:
            self.show_options()
        elif step_num == 2:
            self.show_installing()
        elif step_num == 3:
            self.show_finish()
        
        # Update button states
        self.back_btn.configure(state="normal" if step_num > 0 else "disabled")
        if step_num == 3:
            self.next_btn.configure(text="Finish", command=self.quit)
        else:
            self.next_btn.configure(text="Next", command=self.go_next)
    
    def show_welcome(self):
        ctk.CTkLabel(
            self.content_frame,
            text="Welcome to AI Corrector Installer",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FFFFFF"
        ).pack(pady=20, anchor="w")
        
        welcome_text = """This wizard will guide you through the installation of AI Corrector.

AI Corrector is an intelligent text correction application that uses advanced T5 Transformer models to provide contextual grammar corrections and spelling translations.

Click 'Next' to continue."""
        
        ctk.CTkLabel(
            self.content_frame,
            text=welcome_text,
            font=ctk.CTkFont(size=13),
            text_color="#CCCCCC",
            justify="left"
        ).pack(pady=20, padx=10, anchor="w")
    
    def show_options(self):
        ctk.CTkLabel(
            self.content_frame,
            text="Installation Options",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FFFFFF"
        ).pack(pady=20, anchor="w")
        
        ctk.CTkLabel(
            self.content_frame,
            text="Installation Location:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#FFFFFF"
        ).pack(pady=(0, 10), anchor="w")
        
        path_frame = ctk.CTkFrame(self.content_frame, fg_color="#1C1C1C", corner_radius=5)
        path_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            path_frame,
            text=str(self.install_path),
            font=ctk.CTkFont(size=11),
            text_color="#AAAAAA"
        ).pack(padx=15, pady=12, anchor="w")
        
        ctk.CTkLabel(
            self.content_frame,
            text="Options:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#FFFFFF"
        ).pack(pady=(20, 10), anchor="w")
        
        self.create_desktop_var = tk.BooleanVar(value=True)
        self.create_startmenu_var = tk.BooleanVar(value=True)
        
        ctk.CTkCheckBox(
            self.content_frame,
            text="Create Desktop Shortcut",
            variable=self.create_desktop_var,
            font=ctk.CTkFont(size=12),
            text_color="#FFFFFF",
            border_color="#FFFFFF",
            checkmark_color="#000000",
            fg_color="#FFFFFF"
        ).pack(anchor="w", pady=5)
        
        ctk.CTkCheckBox(
            self.content_frame,
            text="Create Start Menu Entry",
            variable=self.create_startmenu_var,
            font=ctk.CTkFont(size=12),
            text_color="#FFFFFF",
            border_color="#FFFFFF",
            checkmark_color="#000000",
            fg_color="#FFFFFF"
        ).pack(anchor="w", pady=5)
    
    def show_installing(self):
        ctk.CTkLabel(
            self.content_frame,
            text="Installing AI Corrector",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FFFFFF"
        ).pack(pady=20, anchor="w")
        
        self.status_label = ctk.CTkLabel(
            self.content_frame,
            text="Preparing installation...",
            font=ctk.CTkFont(size=12),
            text_color="#AAAAAA"
        )
        self.status_label.pack(anchor="w", pady=(0, 15))
        
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ctk.CTkProgressBar(
            self.content_frame,
            variable=self.progress_var,
            fg_color="#1C1C1C",
            progress_color="#FFFFFF",
            height=8,
            corner_radius=4
        )
        self.progress_bar.pack(fill="x", pady=20)
        
        self.back_btn.configure(state="disabled")
        self.next_btn.configure(state="disabled")
        
        # Start installation in thread
        thread = threading.Thread(target=self.run_install, daemon=True)
        thread.start()
    
    def show_finish(self):
        ctk.CTkLabel(
            self.content_frame,
            text="Installation Complete!",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FFFFFF"
        ).pack(pady=20, anchor="w")
        
        finish_text = """AI Corrector has been successfully installed.

You can now launch the application from:
• Desktop (if shortcut was created)
• Start Menu
• Installation folder

Click 'Finish' to close this installer."""
        
        ctk.CTkLabel(
            self.content_frame,
            text=finish_text,
            font=ctk.CTkFont(size=13),
            text_color="#CCCCCC",
            justify="left"
        ).pack(pady=20, padx=10, anchor="w")
        
        self.back_btn.configure(state="disabled")
    
    def go_back(self):
        if self.current_step > 0:
            self.show_step(self.current_step - 1)
    
    def go_next(self):
        if self.current_step < len(self.steps) - 1:
            self.show_step(self.current_step + 1)
        
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
                self.after(0, self.update_progress, 60, "Creating desktop shortcut...")
                self.create_desktop_shortcut()
            
            # Create Start Menu shortcut
            if self.create_startmenu_var.get():
                self.after(0, self.update_progress, 80, "Creating Start Menu entry...")
                self.create_startmenu_shortcut()
            
            self.after(0, self.update_progress, 100, "Installation complete!")
            self.after(500, self.on_install_complete)
            
        except Exception as e:
            self.after(0, self.show_error, f"Installation failed: {str(e)}")
    
    def on_install_complete(self):
        self.show_step(3)
        self.back_btn.configure(state="disabled")
        
    def update_progress(self, value, status):
        self.progress_var.set(value / 100)
        self.status_label.configure(text=status)
        
    def show_error(self, message):
        messagebox.showerror("Installation Error", message)
        self.show_step(1)
        
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
        if self.current_step == 2:
            messagebox.showwarning("Cannot Cancel", "Installation is in progress.")
            return
        self.quit()


if __name__ == "__main__":
    app = Installer()
    app.mainloop()

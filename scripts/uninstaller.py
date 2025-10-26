#!/usr/bin/env python3
"""
AI Corrector - Custom Uninstaller
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
import os
import shutil
from pathlib import Path

class Uninstaller(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Corrector Uninstaller")
        self.geometry("700x600")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        
        self.install_path = Path(os.path.expanduser("~")) / "AppData" / "Local" / "AICorrector"
        self.current_step = 0
        self.steps = ["Confirm Uninstall", "Uninstalling", "Complete"]
        
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
            text="Uninstaller",
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
        
        self.cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1C1C1C",
            text_color="#FFFFFF",
            hover_color="#333333",
            width=100,
            command=self.quit
        )
        self.cancel_btn.grid(row=0, column=0, padx=5)
        
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
        
        self.protocol("WM_DELETE_WINDOW", self.quit)
        
    def show_step(self, step_num):
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        self.current_step = step_num
        
        if step_num == 0:
            self.show_confirm()
        elif step_num == 1:
            self.show_uninstalling()
        elif step_num == 2:
            self.show_complete()
        
        # Update button states
        if step_num == 2:
            self.next_btn.configure(text="Finish", command=self.quit)
            self.cancel_btn.configure(state="disabled")
    
    def show_confirm(self):
        ctk.CTkLabel(
            self.content_frame,
            text="Uninstall AI Corrector",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FFFFFF"
        ).pack(pady=20, anchor="w")
        
        confirm_text = """Are you sure you want to uninstall AI Corrector?

The application will be removed from your computer. Your personal files will not be affected.

Installation folder:"""
        
        ctk.CTkLabel(
            self.content_frame,
            text=confirm_text,
            font=ctk.CTkFont(size=13),
            text_color="#CCCCCC",
            justify="left"
        ).pack(pady=(0, 10), padx=10, anchor="w")
        
        path_frame = ctk.CTkFrame(self.content_frame, fg_color="#1C1C1C", corner_radius=5)
        path_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            path_frame,
            text=str(self.install_path),
            font=ctk.CTkFont(size=11),
            text_color="#AAAAAA"
        ).pack(padx=15, pady=12, anchor="w")
        
        # Options
        self.remove_shortcuts_var = tk.BooleanVar(value=True)
        
        ctk.CTkCheckBox(
            self.content_frame,
            text="Remove shortcuts and Start Menu entries",
            variable=self.remove_shortcuts_var,
            font=ctk.CTkFont(size=12),
            text_color="#FFFFFF",
            border_color="#FFFFFF",
            checkmark_color="#000000",
            fg_color="#FFFFFF"
        ).pack(anchor="w", pady=(20, 0))
    
    def show_uninstalling(self):
        ctk.CTkLabel(
            self.content_frame,
            text="Uninstalling AI Corrector",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FFFFFF"
        ).pack(pady=20, anchor="w")
        
        self.status_label = ctk.CTkLabel(
            self.content_frame,
            text="Preparing uninstallation...",
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
        
        self.cancel_btn.configure(state="disabled")
        self.next_btn.configure(state="disabled")
        
        # Start uninstallation in thread
        thread = threading.Thread(target=self.run_uninstall, daemon=True)
        thread.start()
    
    def show_complete(self):
        ctk.CTkLabel(
            self.content_frame,
            text="Uninstallation Complete!",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FFFFFF"
        ).pack(pady=20, anchor="w")
        
        complete_text = """AI Corrector has been successfully uninstalled.

All application files have been removed from your computer.

Click 'Finish' to close this uninstaller."""
        
        ctk.CTkLabel(
            self.content_frame,
            text=complete_text,
            font=ctk.CTkFont(size=13),
            text_color="#CCCCCC",
            justify="left"
        ).pack(pady=20, padx=10, anchor="w")
    
    def go_next(self):
        if self.current_step < len(self.steps) - 1:
            self.show_step(self.current_step + 1)
    
    def run_uninstall(self):
        try:
            # Remove shortcuts if requested
            if self.remove_shortcuts_var.get():
                self.after(0, self.update_progress, 20, "Removing shortcuts...")
                self.remove_desktop_shortcut()
                self.remove_startmenu_shortcut()
            
            # Remove installation folder
            self.after(0, self.update_progress, 60, "Removing application files...")
            if self.install_path.exists():
                shutil.rmtree(self.install_path)
            
            self.after(0, self.update_progress, 100, "Uninstallation complete!")
            self.after(500, self.on_uninstall_complete)
            
        except Exception as e:
            self.after(0, self.show_error, f"Uninstallation failed: {str(e)}")
    
    def on_uninstall_complete(self):
        self.show_step(2)
        self.cancel_btn.configure(state="disabled")
        
    def update_progress(self, value, status):
        self.progress_var.set(value / 100)
        self.status_label.configure(text=status)
        
    def show_error(self, message):
        messagebox.showerror("Uninstallation Error", message)
        self.quit()
    
    def remove_desktop_shortcut(self):
        try:
            desktop = Path.home() / "Desktop"
            shortcut_path = desktop / "AI Corrector.lnk"
            if shortcut_path.exists():
                shortcut_path.unlink()
        except:
            pass
    
    def remove_startmenu_shortcut(self):
        try:
            start_menu = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs"
            shortcut_path = start_menu / "AI Corrector.lnk"
            if shortcut_path.exists():
                shortcut_path.unlink()
        except:
            pass


if __name__ == "__main__":
    app = Uninstaller()
    app.mainloop()

#!/usr/bin/env python3
"""
AI Corrector - Custom Uninstaller
Matches the main application's black/white theme and design language
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import os
import shutil
import winreg
import json
import sys
from pathlib import Path
import threading
import time


# --- THEME DEFINITIONS (Matching main app) ---
DARK_THEME = {
    "BG_COLOR": "#000000",
    "MENU_COLOR": "#1C1C1C",
    "ENTRY_COLOR": "#1C1C1C",
    "TEXT_COLOR": "#FFFFFF",
    "BTN_COLOR": "#FFFFFF",
    "BTN_TEXT_COLOR": "#000000",
    "BTN_HOVER_COLOR": "#E0E0E0",
    "DISABLED_COLOR": "#555555",
    "BORDER_COLOR": "#FFFFFF",
    "PROGRESS_COLOR": "#FFFFFF",
}

LIGHT_THEME = {
    "BG_COLOR": "#EAEAEA",
    "MENU_COLOR": "#F5F5F5",
    "ENTRY_COLOR": "#FFFFFF",
    "TEXT_COLOR": "#000000",
    "BTN_COLOR": "#000000",
    "BTN_TEXT_COLOR": "#FFFFFF",
    "BTN_HOVER_COLOR": "#333333",
    "DISABLED_COLOR": "#AAAAAA",
    "BORDER_COLOR": "#000000",
    "PROGRESS_COLOR": "#000000",
}


class UninstallerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Get installation info
        self.install_dir = os.path.dirname(os.path.abspath(__file__))
        self.install_info = self.load_install_info()
        
        self.APP_NAME = self.install_info.get("app_name", "AI Corrector")
        self.APP_VERSION = self.install_info.get("version", "v2.3.0")
        
        self.current_page = 0
        self.is_uninstalling = False
        
        # Window setup
        self.title(f"Uninstall {self.APP_NAME}")
        self.geometry("500x500")  # 1:1 ratio
        self.resizable(False, False)
        
        # Set theme
        ctk.set_appearance_mode("system")
        self.current_theme = DARK_THEME if ctk.get_appearance_mode() == "Dark" else LIGHT_THEME
        self.configure(fg_color=self.current_theme["BG_COLOR"])
        
        # Create UI
        self.create_pages()
        self.show_page(0)
        
        # Bind window close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def load_install_info(self):
        """Load installation information"""
        info_file = os.path.join(self.install_dir, "install_info.json")
        if os.path.exists(info_file):
            try:
                with open(info_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def create_pages(self):
        """Create all uninstaller pages"""
        # Main container
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=self.current_theme["BG_COLOR"])
        self.main_frame.pack(fill="both", expand=True)
        
        # Pages
        self.pages = []
        self.pages.append(self.create_confirm_page())
        self.pages.append(self.create_uninstalling_page())
        self.pages.append(self.create_complete_page())
        
        # Bottom navigation frame
        self.nav_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=self.current_theme["BG_COLOR"], height=60)
        self.nav_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        
        self.uninstall_btn = ctk.CTkButton(
            self.nav_frame,
            text="Uninstall",
            width=120,
            command=self.start_uninstall,
            fg_color=self.current_theme["BTN_COLOR"],
            text_color=self.current_theme["BTN_TEXT_COLOR"],
            hover_color=self.current_theme["BTN_HOVER_COLOR"],
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.uninstall_btn.pack(side="right", padx=5)
        
        self.cancel_btn = ctk.CTkButton(
            self.nav_frame,
            text="Cancel",
            width=100,
            command=self.on_closing,
            fg_color=self.current_theme["BTN_COLOR"],
            text_color=self.current_theme["BTN_TEXT_COLOR"],
            hover_color=self.current_theme["BTN_HOVER_COLOR"],
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.cancel_btn.pack(side="right", padx=5)
    
    def create_confirm_page(self):
        """Page 0: Confirm uninstallation"""
        page = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=self.current_theme["BG_COLOR"])
        
        # Warning icon
        icon_label = ctk.CTkLabel(
            page,
            text="⚠",
            font=ctk.CTkFont(size=48),
            text_color="orange"
        )
        icon_label.pack(pady=(60, 20))
        
        # Title
        title = ctk.CTkLabel(
            page,
            text=f"Uninstall {self.APP_NAME}?",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.current_theme["TEXT_COLOR"]
        )
        title.pack(pady=(0, 20))
        
        # Description
        desc_text = (
            f"This will remove {self.APP_NAME} {self.APP_VERSION}\n"
            "from your computer.\n\n"
            "All application files, shortcuts, and registry entries\n"
            "will be deleted.\n\n"
            f"Installation folder:\n{self.install_dir}"
        )
        desc = ctk.CTkLabel(
            page,
            text=desc_text,
            font=ctk.CTkFont(size=12),
            text_color=self.current_theme["TEXT_COLOR"],
            justify="center"
        )
        desc.pack(pady=10)
        
        return page
    
    def create_uninstalling_page(self):
        """Page 1: Uninstallation progress"""
        page = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=self.current_theme["BG_COLOR"])
        
        title = ctk.CTkLabel(
            page,
            text="Uninstalling AI Corrector",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.current_theme["TEXT_COLOR"]
        )
        title.pack(pady=(80, 40))
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            page,
            width=400,
            height=20,
            corner_radius=10,
            progress_color=self.current_theme["PROGRESS_COLOR"],
            fg_color=self.current_theme["ENTRY_COLOR"],
            border_width=1,
            border_color=self.current_theme["BORDER_COLOR"]
        )
        self.progress_bar.pack(pady=30)
        self.progress_bar.set(0)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            page,
            text="Preparing uninstallation...",
            font=ctk.CTkFont(size=13),
            text_color=self.current_theme["TEXT_COLOR"]
        )
        self.status_label.pack(pady=10)
        
        return page
    
    def create_complete_page(self):
        """Page 2: Uninstallation complete"""
        page = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=self.current_theme["BG_COLOR"])
        
        # Success icon
        icon_label = ctk.CTkLabel(
            page,
            text="✓",
            font=ctk.CTkFont(size=56),
            text_color="lightgreen"
        )
        icon_label.pack(pady=(80, 20))
        
        # Title
        title = ctk.CTkLabel(
            page,
            text="Uninstallation Complete",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=self.current_theme["TEXT_COLOR"]
        )
        title.pack(pady=(0, 30))
        
        # Description
        desc_text = (
            f"{self.APP_NAME} has been successfully removed\n"
            "from your computer.\n\n"
            "Click Finish to close this window."
        )
        desc = ctk.CTkLabel(
            page,
            text=desc_text,
            font=ctk.CTkFont(size=13),
            text_color=self.current_theme["TEXT_COLOR"],
            justify="center"
        )
        desc.pack(pady=10)
        
        return page
    
    def show_page(self, page_num):
        """Display specific page"""
        # Hide all pages
        for page in self.pages:
            page.pack_forget()
        
        # Show requested page
        self.current_page = page_num
        self.pages[page_num].pack(fill="both", expand=True, before=self.nav_frame)
        
        # Update buttons
        self.update_navigation_buttons()
    
    def update_navigation_buttons(self):
        """Update button states based on current page"""
        if self.current_page == 0:
            # Confirm page
            self.uninstall_btn.configure(text="Uninstall", state="normal")
            self.cancel_btn.configure(state="normal")
        elif self.current_page == 1:
            # Uninstalling page
            self.uninstall_btn.configure(state="disabled")
            self.cancel_btn.configure(state="disabled")
        else:
            # Complete page
            self.uninstall_btn.pack_forget()
            self.cancel_btn.configure(text="Finish", state="normal", command=self.quit)
    
    def start_uninstall(self):
        """Start uninstallation process"""
        self.is_uninstalling = True
        self.show_page(1)
        
        uninstall_thread = threading.Thread(target=self.uninstall_files, daemon=True)
        uninstall_thread.start()
    
    def uninstall_files(self):
        """Uninstall application files (runs in background thread)"""
        try:
            total_steps = 5
            current_step = 0
            
            # Step 1: Remove shortcuts
            self.update_progress(current_step / total_steps, "Removing shortcuts...")
            self.remove_shortcuts()
            current_step += 1
            time.sleep(0.3)
            
            # Step 2: Remove registry entries
            self.update_progress(current_step / total_steps, "Removing registry entries...")
            self.remove_registry_entries()
            current_step += 1
            time.sleep(0.3)
            
            # Step 3: Remove Start Menu folder
            self.update_progress(current_step / total_steps, "Removing Start Menu entries...")
            self.remove_startmenu_folder()
            current_step += 1
            time.sleep(0.3)
            
            # Step 4: Mark files for deletion
            self.update_progress(current_step / total_steps, "Preparing files for deletion...")
            current_step += 1
            time.sleep(0.3)
            
            # Step 5: Create deletion script
            self.update_progress(current_step / total_steps, "Finalizing uninstallation...")
            self.create_deletion_script()
            current_step += 1
            
            # Complete
            self.update_progress(1.0, "Uninstallation complete!")
            self.after(500, self.uninstallation_complete)
            
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Uninstallation Error", f"An error occurred:\n{str(e)}"))
            self.after(0, self.quit)
    
    def update_progress(self, progress, status):
        """Update progress bar and status (thread-safe)"""
        self.after(0, self._update_progress_ui, progress, status)
    
    def _update_progress_ui(self, progress, status):
        """Update UI elements (must be called from main thread)"""
        self.progress_bar.set(progress)
        self.status_label.configure(text=status)
    
    def remove_shortcuts(self):
        """Remove desktop and start menu shortcuts"""
        try:
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            
            # Desktop shortcut
            desktop = shell.SpecialFolders("Desktop")
            desktop_shortcut = os.path.join(desktop, f"{self.APP_NAME}.lnk")
            if os.path.exists(desktop_shortcut):
                os.remove(desktop_shortcut)
        
        except Exception as e:
            print(f"Error removing shortcuts: {e}")
    
    def remove_startmenu_folder(self):
        """Remove Start Menu folder"""
        try:
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            
            start_menu = shell.SpecialFolders("Programs")
            app_folder = os.path.join(start_menu, self.APP_NAME)
            
            if os.path.exists(app_folder):
                shutil.rmtree(app_folder)
        
        except Exception as e:
            print(f"Error removing Start Menu folder: {e}")
    
    def remove_registry_entries(self):
        """Remove registry entries"""
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\AICorrector"
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
        except Exception as e:
            print(f"Error removing registry entries: {e}")
    
    def create_deletion_script(self):
        """Create a batch script to delete installation folder after uninstaller closes"""
        batch_script = os.path.join(os.environ['TEMP'], 'ai_corrector_cleanup.bat')
        
        with open(batch_script, 'w') as f:
            f.write('@echo off\n')
            f.write('timeout /t 2 /nobreak > nul\n')
            f.write(f'rmdir /s /q "{self.install_dir}"\n')
            f.write(f'del "%~f0"\n')
        
        # Schedule the batch file to run
        import subprocess
        subprocess.Popen(['cmd', '/c', batch_script], 
                        creationflags=subprocess.CREATE_NO_WINDOW,
                        shell=False)
    
    def uninstallation_complete(self):
        """Handle uninstallation completion"""
        self.is_uninstalling = False
        self.show_page(2)
    
    def on_closing(self):
        """Handle window close"""
        if self.is_uninstalling:
            return
        self.quit()


def main():
    """Main entry point"""
    app = UninstallerApp()
    app.mainloop()


if __name__ == "__main__":
    main()

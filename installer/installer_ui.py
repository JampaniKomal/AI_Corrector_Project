#!/usr/bin/env python3
"""
AI Corrector - Custom Installer
Matches the main application's black/white theme and design language
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import json
import winreg
import sys
from pathlib import Path
import threading


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


class InstallerApp(ctk.CTk):
    def __init__(self, source_folder=None):
        super().__init__()
        
        # Configuration
        self.APP_NAME = "AI Corrector"
        self.APP_VERSION = "v2.3.0"
        self.source_folder = source_folder or self.get_source_folder()
        self.install_location = os.path.join(os.environ.get('PROGRAMFILES', 'C:\\Program Files'), 'AI Corrector')
        self.current_page = 0
        self.is_installing = False
        
        # Window setup
        self.title(f"{self.APP_NAME} {self.APP_VERSION} - Setup")
        self.geometry("700x500")
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
    
    def get_source_folder(self):
        """Get the folder containing installer files"""
        if hasattr(sys, '_MEIPASS'):
            # Running from PyInstaller bundle
            return sys._MEIPASS
        else:
            # Running from source - go up from installer folder
            return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    def create_pages(self):
        """Create all installer pages"""
        # Main container
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=self.current_theme["BG_COLOR"])
        self.main_frame.pack(fill="both", expand=True)
        
        # Pages
        self.pages = []
        self.pages.append(self.create_welcome_page())
        self.pages.append(self.create_location_page())
        self.pages.append(self.create_options_page())
        self.pages.append(self.create_installing_page())
        self.pages.append(self.create_complete_page())
        
        # Bottom navigation frame
        self.nav_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=self.current_theme["BG_COLOR"], height=60)
        self.nav_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        
        self.back_btn = ctk.CTkButton(
            self.nav_frame,
            text="< Back",
            width=100,
            command=self.go_back,
            fg_color=self.current_theme["BTN_COLOR"],
            text_color=self.current_theme["BTN_TEXT_COLOR"],
            hover_color=self.current_theme["BTN_HOVER_COLOR"],
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.back_btn.pack(side="left", padx=5)
        
        self.next_btn = ctk.CTkButton(
            self.nav_frame,
            text="Next >",
            width=100,
            command=self.go_next,
            fg_color=self.current_theme["BTN_COLOR"],
            text_color=self.current_theme["BTN_TEXT_COLOR"],
            hover_color=self.current_theme["BTN_HOVER_COLOR"],
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.next_btn.pack(side="right", padx=5)
        
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
    
    def create_welcome_page(self):
        """Page 0: Welcome screen"""
        page = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=self.current_theme["BG_COLOR"])
        
        # Large title
        title = ctk.CTkLabel(
            page,
            text=f"Welcome to {self.APP_NAME} Setup",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.current_theme["TEXT_COLOR"]
        )
        title.pack(pady=(60, 20))
        
        # Version
        version = ctk.CTkLabel(
            page,
            text=self.APP_VERSION,
            font=ctk.CTkFont(size=16),
            text_color=self.current_theme["DISABLED_COLOR"]
        )
        version.pack(pady=(0, 40))
        
        # Description
        desc_text = (
            "This wizard will guide you through the installation of\n"
            f"{self.APP_NAME} on your computer.\n\n"
            "AI Corrector uses T5 Transformer models to provide\n"
            "contextual grammar corrections and spelling translation.\n\n"
            "Click Next to continue."
        )
        desc = ctk.CTkLabel(
            page,
            text=desc_text,
            font=ctk.CTkFont(size=13),
            text_color=self.current_theme["TEXT_COLOR"],
            justify="center"
        )
        desc.pack(pady=20)
        
        return page
    
    def create_location_page(self):
        """Page 1: Installation location"""
        page = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=self.current_theme["BG_COLOR"])
        
        title = ctk.CTkLabel(
            page,
            text="Choose Installation Location",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.current_theme["TEXT_COLOR"]
        )
        title.pack(pady=(40, 10), padx=40, anchor="w")
        
        desc = ctk.CTkLabel(
            page,
            text="Setup will install AI Corrector in the following folder.",
            font=ctk.CTkFont(size=13),
            text_color=self.current_theme["TEXT_COLOR"]
        )
        desc.pack(pady=(0, 20), padx=40, anchor="w")
        
        # Location frame
        loc_frame = ctk.CTkFrame(page, fg_color="transparent")
        loc_frame.pack(pady=20, padx=40, fill="x")
        
        self.location_entry = ctk.CTkEntry(
            loc_frame,
            width=450,
            height=35,
            fg_color=self.current_theme["ENTRY_COLOR"],
            text_color=self.current_theme["TEXT_COLOR"],
            border_color=self.current_theme["BORDER_COLOR"],
            border_width=1,
            corner_radius=8,
            font=ctk.CTkFont(size=12)
        )
        self.location_entry.pack(side="left", padx=(0, 10))
        self.location_entry.insert(0, self.install_location)
        
        browse_btn = ctk.CTkButton(
            loc_frame,
            text="Browse...",
            width=100,
            command=self.browse_location,
            fg_color=self.current_theme["BTN_COLOR"],
            text_color=self.current_theme["BTN_TEXT_COLOR"],
            hover_color=self.current_theme["BTN_HOVER_COLOR"],
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        browse_btn.pack(side="left")
        
        # Space required
        space_info = ctk.CTkLabel(
            page,
            text="Space required: ~250 MB",
            font=ctk.CTkFont(size=12),
            text_color=self.current_theme["DISABLED_COLOR"]
        )
        space_info.pack(pady=(30, 0), padx=40, anchor="w")
        
        return page
    
    def create_options_page(self):
        """Page 2: Installation options"""
        page = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=self.current_theme["BG_COLOR"])
        
        title = ctk.CTkLabel(
            page,
            text="Select Additional Tasks",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.current_theme["TEXT_COLOR"]
        )
        title.pack(pady=(40, 10), padx=40, anchor="w")
        
        desc = ctk.CTkLabel(
            page,
            text="Select the additional tasks you would like Setup to perform:",
            font=ctk.CTkFont(size=13),
            text_color=self.current_theme["TEXT_COLOR"]
        )
        desc.pack(pady=(0, 30), padx=40, anchor="w")
        
        # Options frame
        opts_frame = ctk.CTkFrame(page, fg_color="transparent")
        opts_frame.pack(pady=10, padx=60, fill="x")
        
        self.create_desktop_shortcut = tk.BooleanVar(value=True)
        desktop_cb = ctk.CTkCheckBox(
            opts_frame,
            text="Create a desktop shortcut",
            variable=self.create_desktop_shortcut,
            text_color=self.current_theme["TEXT_COLOR"],
            fg_color=self.current_theme["BTN_COLOR"],
            hover_color=self.current_theme["BTN_HOVER_COLOR"],
            font=ctk.CTkFont(size=13)
        )
        desktop_cb.pack(pady=10, anchor="w")
        
        self.create_startmenu_shortcut = tk.BooleanVar(value=True)
        startmenu_cb = ctk.CTkCheckBox(
            opts_frame,
            text="Create a Start Menu folder",
            variable=self.create_startmenu_shortcut,
            text_color=self.current_theme["TEXT_COLOR"],
            fg_color=self.current_theme["BTN_COLOR"],
            hover_color=self.current_theme["BTN_HOVER_COLOR"],
            font=ctk.CTkFont(size=13)
        )
        startmenu_cb.pack(pady=10, anchor="w")
        
        return page
    
    def create_installing_page(self):
        """Page 3: Installation progress"""
        page = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=self.current_theme["BG_COLOR"])
        
        title = ctk.CTkLabel(
            page,
            text="Installing AI Corrector",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.current_theme["TEXT_COLOR"]
        )
        title.pack(pady=(60, 30), padx=40, anchor="w")
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            page,
            width=600,
            height=20,
            corner_radius=10,
            progress_color=self.current_theme["PROGRESS_COLOR"],
            fg_color=self.current_theme["ENTRY_COLOR"],
            border_width=1,
            border_color=self.current_theme["BORDER_COLOR"]
        )
        self.progress_bar.pack(pady=30, padx=40)
        self.progress_bar.set(0)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            page,
            text="Preparing installation...",
            font=ctk.CTkFont(size=13),
            text_color=self.current_theme["TEXT_COLOR"]
        )
        self.status_label.pack(pady=10, padx=40)
        
        # Details label
        self.details_label = ctk.CTkLabel(
            page,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=self.current_theme["DISABLED_COLOR"]
        )
        self.details_label.pack(pady=5, padx=40)
        
        return page
    
    def create_complete_page(self):
        """Page 4: Installation complete"""
        page = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=self.current_theme["BG_COLOR"])
        
        title = ctk.CTkLabel(
            page,
            text="Installation Complete!",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.current_theme["TEXT_COLOR"]
        )
        title.pack(pady=(80, 30))
        
        desc_text = (
            f"{self.APP_NAME} has been successfully installed\n"
            "on your computer.\n\n"
            "Click Finish to exit Setup."
        )
        desc = ctk.CTkLabel(
            page,
            text=desc_text,
            font=ctk.CTkFont(size=13),
            text_color=self.current_theme["TEXT_COLOR"],
            justify="center"
        )
        desc.pack(pady=20)
        
        # Launch checkbox
        self.launch_after_install = tk.BooleanVar(value=True)
        launch_cb = ctk.CTkCheckBox(
            page,
            text=f"Launch {self.APP_NAME}",
            variable=self.launch_after_install,
            text_color=self.current_theme["TEXT_COLOR"],
            fg_color=self.current_theme["BTN_COLOR"],
            hover_color=self.current_theme["BTN_HOVER_COLOR"],
            font=ctk.CTkFont(size=13, weight="bold")
        )
        launch_cb.pack(pady=30)
        
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
        # Back button
        if self.current_page == 0:
            self.back_btn.configure(state="disabled")
        else:
            self.back_btn.configure(state="normal")
        
        # Next/Install/Finish button
        if self.current_page == len(self.pages) - 1:
            self.next_btn.configure(text="Finish")
            self.cancel_btn.configure(state="disabled")
        elif self.current_page == len(self.pages) - 2:
            self.next_btn.configure(text="Install", state="disabled" if self.is_installing else "normal")
            self.back_btn.configure(state="disabled" if self.is_installing else "normal")
            self.cancel_btn.configure(state="disabled" if self.is_installing else "normal")
        else:
            self.next_btn.configure(text="Next >", state="normal")
            self.cancel_btn.configure(state="normal")
    
    def go_back(self):
        """Navigate to previous page"""
        if self.current_page > 0:
            self.show_page(self.current_page - 1)
    
    def go_next(self):
        """Navigate to next page or execute action"""
        if self.current_page == len(self.pages) - 1:
            # Finish button clicked
            self.finish_installation()
        elif self.current_page == len(self.pages) - 2:
            # Install button clicked
            self.start_installation()
        else:
            # Next button clicked
            if self.current_page == 1:
                # Validate installation path
                self.install_location = self.location_entry.get()
                if not self.validate_install_path():
                    return
            self.show_page(self.current_page + 1)
    
    def browse_location(self):
        """Browse for installation directory"""
        folder = filedialog.askdirectory(
            title="Select Installation Folder",
            initialdir=os.path.dirname(self.install_location)
        )
        if folder:
            self.location_entry.delete(0, tk.END)
            self.location_entry.insert(0, folder)
    
    def validate_install_path(self):
        """Validate installation path"""
        path = self.install_location
        
        # Check if path is valid
        try:
            Path(path).parent.exists()
        except:
            messagebox.showerror("Invalid Path", "The installation path is invalid.")
            return False
        
        # Check if directory already exists
        if os.path.exists(path):
            result = messagebox.askyesno(
                "Directory Exists",
                f"The directory already exists:\n{path}\n\nDo you want to overwrite it?"
            )
            if not result:
                return False
        
        return True
    
    def start_installation(self):
        """Start installation process in background thread"""
        self.is_installing = True
        self.update_navigation_buttons()
        
        install_thread = threading.Thread(target=self.install_files, daemon=True)
        install_thread.start()
    
    def install_files(self):
        """Install application files (runs in background thread)"""
        try:
            total_steps = 6
            current_step = 0
            
            # Step 1: Create installation directory
            self.update_progress(current_step / total_steps, "Creating installation directory...", "")
            os.makedirs(self.install_location, exist_ok=True)
            current_step += 1
            
            # Step 2: Copy application files
            self.update_progress(current_step / total_steps, "Copying application files...", "")
            
            # Find the executable (or source files)
            if os.path.exists(os.path.join(self.source_folder, "dist", "AICorrector.exe")):
                # Copy from dist folder
                exe_path = os.path.join(self.source_folder, "dist", "AICorrector.exe")
                shutil.copy2(exe_path, self.install_location)
            else:
                # Copy all necessary files
                files_to_copy = ["main.py", "requirements.txt", "README.md"]
                folders_to_copy = ["src", "assets"]
                
                for file in files_to_copy:
                    src = os.path.join(self.source_folder, file)
                    if os.path.exists(src):
                        shutil.copy2(src, self.install_location)
                
                for folder in folders_to_copy:
                    src = os.path.join(self.source_folder, folder)
                    dst = os.path.join(self.install_location, folder)
                    if os.path.exists(src):
                        if os.path.exists(dst):
                            shutil.rmtree(dst)
                        shutil.copytree(src, dst)
            
            current_step += 1
            
            # Step 3: Copy icon
            self.update_progress(current_step / total_steps, "Installing icons...", "")
            icon_src = os.path.join(self.source_folder, "assets", "app_logo.ico")
            if os.path.exists(icon_src):
                os.makedirs(os.path.join(self.install_location, "assets"), exist_ok=True)
                shutil.copy2(icon_src, os.path.join(self.install_location, "assets"))
            current_step += 1
            
            # Step 4: Create shortcuts
            if self.create_desktop_shortcut.get() or self.create_startmenu_shortcut.get():
                self.update_progress(current_step / total_steps, "Creating shortcuts...", "")
                self.create_shortcuts()
            current_step += 1
            
            # Step 5: Create uninstaller
            self.update_progress(current_step / total_steps, "Creating uninstaller...", "")
            self.create_uninstaller()
            current_step += 1
            
            # Step 6: Register installation
            self.update_progress(current_step / total_steps, "Registering installation...", "")
            self.register_installation()
            current_step += 1
            
            # Complete
            self.update_progress(1.0, "Installation complete!", "")
            self.after(500, self.installation_complete)
            
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Installation Error", f"An error occurred during installation:\n{str(e)}"))
            self.after(0, self.quit)
    
    def update_progress(self, progress, status, details):
        """Update progress bar and status (thread-safe)"""
        self.after(0, self._update_progress_ui, progress, status, details)
    
    def _update_progress_ui(self, progress, status, details):
        """Update UI elements (must be called from main thread)"""
        self.progress_bar.set(progress)
        self.status_label.configure(text=status)
        self.details_label.configure(text=details)
    
    def create_shortcuts(self):
        """Create desktop and start menu shortcuts"""
        try:
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            
            exe_path = os.path.join(self.install_location, "AICorrector.exe")
            if not os.path.exists(exe_path):
                # If exe doesn't exist, create shortcut to Python script
                exe_path = os.path.join(self.install_location, "main.py")
            
            icon_path = os.path.join(self.install_location, "assets", "app_logo.ico")
            
            # Desktop shortcut
            if self.create_desktop_shortcut.get():
                desktop = shell.SpecialFolders("Desktop")
                shortcut_path = os.path.join(desktop, f"{self.APP_NAME}.lnk")
                shortcut = shell.CreateShortCut(shortcut_path)
                shortcut.Targetpath = exe_path
                shortcut.WorkingDirectory = self.install_location
                if os.path.exists(icon_path):
                    shortcut.IconLocation = icon_path
                shortcut.save()
            
            # Start menu shortcut
            if self.create_startmenu_shortcut.get():
                start_menu = shell.SpecialFolders("Programs")
                app_folder = os.path.join(start_menu, self.APP_NAME)
                os.makedirs(app_folder, exist_ok=True)
                
                shortcut_path = os.path.join(app_folder, f"{self.APP_NAME}.lnk")
                shortcut = shell.CreateShortCut(shortcut_path)
                shortcut.Targetpath = exe_path
                shortcut.WorkingDirectory = self.install_location
                if os.path.exists(icon_path):
                    shortcut.IconLocation = icon_path
                shortcut.save()
                
                # Uninstaller shortcut
                uninstall_path = os.path.join(self.install_location, "uninstall.exe")
                if os.path.exists(uninstall_path):
                    uninstall_shortcut_path = os.path.join(app_folder, "Uninstall AI Corrector.lnk")
                    uninstall_shortcut = shell.CreateShortCut(uninstall_shortcut_path)
                    uninstall_shortcut.Targetpath = uninstall_path
                    uninstall_shortcut.WorkingDirectory = self.install_location
                    uninstall_shortcut.save()
        
        except Exception as e:
            print(f"Error creating shortcuts: {e}")
    
    def create_uninstaller(self):
        """Create uninstaller script"""
        uninstaller_script = os.path.join(self.install_location, "uninstall.py")
        
        # Copy uninstaller UI file
        uninstaller_ui_src = os.path.join(os.path.dirname(__file__), "uninstaller_ui.py")
        if os.path.exists(uninstaller_ui_src):
            shutil.copy2(uninstaller_ui_src, self.install_location)
        
        # Create simple launcher script
        with open(uninstaller_script, 'w') as f:
            f.write('#!/usr/bin/env python3\n')
            f.write('import os\n')
            f.write('import sys\n')
            f.write('os.chdir(os.path.dirname(os.path.abspath(__file__)))\n')
            f.write('if os.path.exists("uninstaller_ui.py"):\n')
            f.write('    exec(open("uninstaller_ui.py").read())\n')
    
    def register_installation(self):
        """Register installation in Windows Registry"""
        try:
            # Create registry entry for Add/Remove Programs
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\AICorrector"
            
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
            
            winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, f"{self.APP_NAME} {self.APP_VERSION}")
            winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, self.APP_VERSION)
            winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, "Jampani Komal")
            winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, self.install_location)
            
            uninstall_path = os.path.join(self.install_location, "uninstall.py")
            winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, f'python "{uninstall_path}"')
            
            icon_path = os.path.join(self.install_location, "assets", "app_logo.ico")
            if os.path.exists(icon_path):
                winreg.SetValueEx(key, "DisplayIcon", 0, winreg.REG_SZ, icon_path)
            
            winreg.CloseKey(key)
            
            # Save installation info
            install_info = {
                "app_name": self.APP_NAME,
                "version": self.APP_VERSION,
                "install_location": self.install_location,
                "desktop_shortcut": self.create_desktop_shortcut.get(),
                "startmenu_shortcut": self.create_startmenu_shortcut.get()
            }
            
            with open(os.path.join(self.install_location, "install_info.json"), 'w') as f:
                json.dump(install_info, f, indent=2)
        
        except Exception as e:
            print(f"Error registering installation: {e}")
    
    def installation_complete(self):
        """Handle installation completion"""
        self.is_installing = False
        self.show_page(len(self.pages) - 1)
    
    def finish_installation(self):
        """Finish installation and launch app if requested"""
        if self.launch_after_install.get():
            try:
                exe_path = os.path.join(self.install_location, "AICorrector.exe")
                if os.path.exists(exe_path):
                    os.startfile(exe_path)
                else:
                    # Launch Python script
                    import subprocess
                    script_path = os.path.join(self.install_location, "main.py")
                    subprocess.Popen(['python', script_path], cwd=self.install_location)
            except Exception as e:
                print(f"Error launching app: {e}")
        
        self.quit()
    
    def on_closing(self):
        """Handle window close"""
        if self.is_installing:
            result = messagebox.askyesno(
                "Installation in Progress",
                "Installation is currently in progress.\nAre you sure you want to cancel?"
            )
            if not result:
                return
        
        self.quit()


def main():
    """Main entry point"""
    app = InstallerApp()
    app.mainloop()


if __name__ == "__main__":
    main()

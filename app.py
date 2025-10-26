import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as messagebox
import threading
import os
from correct import (SUPPORTED_MODELS, check_if_model_downloaded,
                     download_model_for_language, load_model_from_disk,
                     correct_grammar, get_model_path)
from spellchecker import SpellChecker

# --- THEME DEFINITIONS ---
# Define color palettes for both modes
DARK_THEME = {
    "BG_COLOR": "#000000",
    "MENU_COLOR": "#1C1C1C",
    "ENTRY_COLOR": "#1C1C1C",
    "TEXT_COLOR": "#FFFFFF",
    "BTN_COLOR": "#FFFFFF",
    "BTN_TEXT_COLOR": "#000000",
    "BTN_HOVER_COLOR": "#E0E0E0",
    "ICON_HOVER_COLOR": "#333333",
    "DOWNLOAD_BTN_COLOR": "#FFFFFF",
    "DOWNLOAD_BTN_TEXT": "#000000",
    "DOWNLOAD_BTN_HOVER": "#CCCCCC",
    "DISABLED_COLOR": "#555555"
}

LIGHT_THEME = {
    "BG_COLOR": "#EAEAEA", # Light grey background
    "MENU_COLOR": "#F5F5F5", # Slightly darker grey menu
    "ENTRY_COLOR": "#FFFFFF", # White entry boxes
    "TEXT_COLOR": "#000000", # Black text
    "BTN_COLOR": "#000000", # Black button
    "BTN_TEXT_COLOR": "#FFFFFF", # White button text
    "BTN_HOVER_COLOR": "#333333",
    "ICON_HOVER_COLOR": "#CCCCCC",
    "DOWNLOAD_BTN_COLOR": "#000000",
    "DOWNLOAD_BTN_TEXT": "#FFFFFF",
    "DOWNLOAD_BTN_HOVER": "#555555",
    "DISABLED_COLOR": "#AAAAAA"
}

# --- MAIN APPLICATION CLASS ---
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Corrector v2.2")
        self.geometry("1100x600")
        ctk.set_appearance_mode("dark") # Start in dark mode

        # --- AI Model State ---
        self.current_lang_code = None
        self.model = None
        self.tokenizer = None
        self.is_loading = False

        # --- Layout Grids ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Class Variables ---
        self.theme_radio_var = tk.StringVar(value="dark")
        self.language_buttons = {}
        self.language_progress_bars = {}
        self.language_status_labels = {}
        self.current_theme = DARK_THEME # Store current theme colors

        # --- Create GUI ---
        self.create_sidebars()
        self.create_pages()
        self.apply_theme(self.current_theme) # Apply initial theme
        self.update_language_statuses()

        # --- Show default page ---
        self.show_page("corrector")
        self.load_selected_model("en_us", initial_load=True)

    # --- Theme Application Method ---
    def apply_theme(self, theme):
        """ Applies the selected color theme to all relevant widgets. """
        self.current_theme = theme
        self.configure(fg_color=theme["BG_COLOR"])

        # Update Sidebars
        self.sidebar_expanded.configure(fg_color=theme["MENU_COLOR"])
        self.sidebar_collapsed.configure(fg_color=theme["MENU_COLOR"])
        # Update sidebar buttons (text color, hover color etc.)
        for btn in self.sidebar_expanded.winfo_children() + self.sidebar_collapsed.winfo_children():
             if isinstance(btn, ctk.CTkLabel):
                 btn.configure(text_color=theme["TEXT_COLOR"], fg_color=theme["MENU_COLOR"])
             elif isinstance(btn, ctk.CTkButton):
                 # Handle active/inactive state coloring later in show_page
                 is_settings_btn = btn in [self.settings_btn_exp, self.settings_btn_col]
                 is_toggle_btn = btn in [self.menu_toggle_btn_exp, self.menu_toggle_btn_col]
                 
                 if not is_settings_btn and not is_toggle_btn: # Nav buttons
                     # Default to inactive style
                     btn.configure(text_color=theme["TEXT_COLOR"], fg_color="transparent", hover_color=theme["ICON_HOVER_COLOR"])
                 elif is_settings_btn:
                     btn.configure(text_color=theme["TEXT_COLOR"], fg_color="transparent", hover_color=theme["ICON_HOVER_COLOR"])
                 else: # Toggle button
                      btn.configure(text_color=theme["TEXT_COLOR"], hover_color=theme["ICON_HOVER_COLOR"])
        # Update OptionMenu explicitly
        self.lang_menu.configure(fg_color=theme["ENTRY_COLOR"], text_color=theme["TEXT_COLOR"], button_color=theme["ENTRY_COLOR"], dropdown_fg_color=theme["ENTRY_COLOR"], dropdown_text_color=theme["TEXT_COLOR"])


        # Update Main Pages
        self.corrector_page_frame.configure(fg_color=theme["BG_COLOR"])
        self.about_page_frame.configure(fg_color=theme["BG_COLOR"])
        self.settings_page_frame.configure(fg_color=theme["BG_COLOR"])

        # Update Corrector Page Widgets
        self.lang_indicator_label.configure(text_color=theme.get("DISABLED_COLOR", "#AAAAAA")) # Use theme disabled color
        self.corrector_page_frame.children['!ctklabel'].configure(text_color=theme["TEXT_COLOR"]) # Input label
        self.corrector_page_frame.children['!ctklabel2'].configure(text_color=theme["TEXT_COLOR"]) # Output label
        self.corrector_input_textbox.configure(fg_color=theme["ENTRY_COLOR"], text_color=theme["TEXT_COLOR"], border_color=theme["TEXT_COLOR"])
        self.corrector_output_textbox.configure(fg_color=theme["ENTRY_COLOR"], text_color=theme["TEXT_COLOR"], border_color=theme["TEXT_COLOR"])
        self.corrector_button_middle.configure(fg_color=theme["BTN_COLOR"], text_color=theme["BTN_TEXT_COLOR"], hover_color=theme["BTN_HOVER_COLOR"])
        self.corrector_page_frame.children['!ctkframe'].configure(fg_color=theme["BG_COLOR"]) # Middle button frame bg

        # Update About Page Widgets
        for child in self.about_page_frame.winfo_children():
            if isinstance(child, ctk.CTkLabel):
                child.configure(text_color=theme["TEXT_COLOR"])

        # Update Settings Page Widgets
        self.settings_page_frame.children['!ctklabel'].configure(text_color=theme["TEXT_COLOR"]) # Settings Title
        self.appearance_frame.configure(fg_color=theme["ENTRY_COLOR"])
        self.appearance_frame.children['!ctklabel'].configure(text_color=theme["TEXT_COLOR"]) # Appearance Title
        for radio in self.appearance_frame.winfo_children():
             if isinstance(radio, ctk.CTkRadioButton):
                 radio.configure(text_color=theme["TEXT_COLOR"])
        
        self.language_frame.configure(fg_color=theme["ENTRY_COLOR"])
        self.language_frame.children['!ctklabel'].configure(text_color=theme["TEXT_COLOR"]) # Language Title
        for lang_code in SUPPORTED_MODELS:
            # Update radio button text
            radio = self.language_frame.children[f'!ctkframe{list(SUPPORTED_MODELS.keys()).index(lang_code)+1}'].children['!ctkradiobutton']
            radio.configure(text_color=theme["TEXT_COLOR"])
            # Update status label color (logic handled in update_language_statuses)
            # Update download button style
            btn = self.language_buttons.get(lang_code)
            if btn:
                btn.configure(
                    fg_color=theme["DOWNLOAD_BTN_COLOR"],
                    text_color=theme["DOWNLOAD_BTN_TEXT"],
                    hover_color=theme["DOWNLOAD_BTN_HOVER"]
                )
            # Update "Coming Soon" label
            coming_soon_label_key = f'!ctklabel{list(SUPPORTED_MODELS.keys()).index(lang_code)+1}'
            if coming_soon_label_key in self.language_frame.children[f'!ctkframe{list(SUPPORTED_MODELS.keys()).index(lang_code)+1}'].children:
                self.language_frame.children[f'!ctkframe{list(SUPPORTED_MODELS.keys()).index(lang_code)+1}'].children[coming_soon_label_key].configure(text_color=theme.get("DISABLED_COLOR", "#AAAAAA"))


        # Re-apply active page button styles
        self.highlight_active_page_button()

    def highlight_active_page_button(self):
         """ Sets the correct highlight color for the active page button """
         theme = self.current_theme
         # Reset all first
         self.corrector_btn_exp.configure(fg_color="transparent", text_color=theme["TEXT_COLOR"])
         self.about_btn_exp.configure(fg_color="transparent", text_color=theme["TEXT_COLOR"])
         self.settings_btn_exp.configure(fg_color="transparent", text_color=theme["TEXT_COLOR"])

         if self.corrector_page_frame.winfo_viewable():
             self.corrector_btn_exp.configure(fg_color=theme["BTN_COLOR"], text_color=theme["BTN_TEXT_COLOR"])
         elif self.about_page_frame.winfo_viewable():
             self.about_btn_exp.configure(fg_color=theme["BTN_COLOR"], text_color=theme["BTN_TEXT_COLOR"])
         elif self.settings_page_frame.winfo_viewable():
             self.settings_btn_exp.configure(fg_color=theme["BTN_COLOR"], text_color=theme["BTN_TEXT_COLOR"])


    # --- GUI Creation Methods ---
    def create_sidebars(self):
        # --- EXPANDED Sidebar ---
        self.sidebar_expanded = ctk.CTkFrame(self, width=250, corner_radius=0) # Color set by apply_theme
        self.sidebar_expanded.grid(row=0, column=0, sticky="nsw")
        self.sidebar_expanded.grid_rowconfigure(6, weight=1) # Spacer row

        self.menu_toggle_btn_exp = ctk.CTkButton(self.sidebar_expanded, text="☰", font=ctk.CTkFont(size=20), width=40, fg_color="transparent", command=self.toggle_sidebar, anchor="w")
        self.menu_toggle_btn_exp.grid(row=0, column=0, pady=20, padx=20, sticky="w")
        self.title_label_exp = ctk.CTkLabel(self.sidebar_expanded, text="AI Corrector", font=ctk.CTkFont(size=22, weight="bold"), anchor="w")
        self.title_label_exp.grid(row=1, column=0, pady=(0, 20), padx=20, sticky="w")
        self.corrector_btn_exp = ctk.CTkButton(self.sidebar_expanded, text="✎  Corrector", font=ctk.CTkFont(size=14, weight="bold"), anchor="w", corner_radius=8, command=lambda: self.show_page("corrector"))
        self.corrector_btn_exp.grid(row=2, column=0, pady=5, padx=20, sticky="ew")
        self.about_btn_exp = ctk.CTkButton(self.sidebar_expanded, text="ⓘ  About Us", font=ctk.CTkFont(size=14, weight="bold"), anchor="w", corner_radius=8, command=lambda: self.show_page("about"))
        self.about_btn_exp.grid(row=3, column=0, pady=5, padx=20, sticky="ew")
        self.lang_label_exp = ctk.CTkLabel(self.sidebar_expanded, text="🌐  Language", font=ctk.CTkFont(size=14, weight="bold"), anchor="w")
        self.lang_label_exp.grid(row=4, column=0, pady=(20, 5), padx=20, sticky="w")
        self.lang_menu = ctk.CTkOptionMenu(self.sidebar_expanded, values=["English (US/Global)", "English (UK) - (Future)", "English (IN) - (Future)"])
        self.lang_menu.grid(row=5, column=0, pady=5, padx=20, sticky="ew")
        self.settings_btn_exp = ctk.CTkButton(self.sidebar_expanded, text="⚙  Settings", font=ctk.CTkFont(size=14, weight="bold"), anchor="w", corner_radius=8, command=lambda: self.show_page("settings"))
        self.settings_btn_exp.grid(row=7, column=0, pady=20, padx=20, sticky="s")

        # --- COLLAPSED Sidebar ---
        self.sidebar_collapsed = ctk.CTkFrame(self, width=70, corner_radius=0) # Color set by apply_theme
        self.sidebar_collapsed.grid(row=0, column=0, sticky="nsw")
        self.sidebar_collapsed.grid_rowconfigure(1, weight=1) # Spacer
        self.menu_toggle_btn_col = ctk.CTkButton(self.sidebar_collapsed, text="☰", font=ctk.CTkFont(size=20), width=40, fg_color="transparent", command=self.toggle_sidebar, anchor="center")
        self.menu_toggle_btn_col.grid(row=0, column=0, pady=20, padx=15, sticky="w")
        self.settings_btn_col = ctk.CTkButton(self.sidebar_collapsed, text="⚙", font=ctk.CTkFont(size=20), width=40, fg_color="transparent", corner_radius=8, command=lambda: [self.toggle_sidebar(), self.show_page("settings")])
        self.settings_btn_col.grid(row=2, column=0, pady=20, padx=15, sticky="s")
        self.sidebar_collapsed.grid_forget() # Hide it initially

    def create_pages(self):
        # --- Page 1: Corrector ---
        self.corrector_page_frame = ctk.CTkFrame(self, corner_radius=0) # Color set by apply_theme
        self.corrector_page_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.corrector_page_frame.grid_columnconfigure((0, 2), weight=1)
        self.corrector_page_frame.grid_columnconfigure(1, weight=0)
        self.corrector_page_frame.grid_rowconfigure(2, weight=1) # Textboxes row

        self.lang_indicator_label = ctk.CTkLabel(self.corrector_page_frame, text="Model: [None Loaded]", font=ctk.CTkFont(size=12)) # Color set by apply_theme
        self.lang_indicator_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

        ctk.CTkLabel(self.corrector_page_frame, text="Input Text:", font=ctk.CTkFont(size=14)).grid(row=1, column=0, sticky="w", pady=(0, 5))
        self.corrector_input_textbox = ctk.CTkTextbox(self.corrector_page_frame, corner_radius=10, font=ctk.CTkFont(size=13), border_width=1) # Colors set by apply_theme
        self.corrector_input_textbox.grid(row=2, column=0, sticky="nsew", padx=(0, 10))

        middle_button_frame = ctk.CTkFrame(self.corrector_page_frame) # Color set by apply_theme
        middle_button_frame.grid(row=2, column=1, sticky="ns", padx=5)
        self.corrector_button_middle = ctk.CTkButton(middle_button_frame, text=">>", width=50, font=ctk.CTkFont(size=16, weight="bold"), corner_radius=8, command=self.on_correct_click, state="disabled") # Colors set by apply_theme
        self.corrector_button_middle.pack(expand=True)

        ctk.CTkLabel(self.corrector_page_frame, text="Corrected Text:", font=ctk.CTkFont(size=14)).grid(row=1, column=2, sticky="w", pady=(0, 5))
        self.corrector_output_textbox = ctk.CTkTextbox(self.corrector_page_frame, corner_radius=10, font=ctk.CTkFont(size=13), state="disabled", border_width=1) # Colors set by apply_theme
        self.corrector_output_textbox.grid(row=2, column=2, sticky="nsew", padx=(10, 0))

        # --- Page 2: About Us ---
        self.about_page_frame = ctk.CTkFrame(self, corner_radius=0) # Color set by apply_theme
        self.about_page_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        ctk.CTkLabel(self.about_page_frame, text="About This Project", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20, anchor="w")
        about_text = ("Project: AI Contextual Corrector\n"
                      "Course: Artificial Intelligence (G5AD24ARI)\n"
                      "University: Rashtriya Raksha University\n\n"
                      "Team Members:\n"
                      "- Jampani Komal\n- [Team Member 2 Name]\n- [Team Member 3 Name]\n\n"
                      "This application uses pre-trained T5 Transformer models\n"
                      "to provide contextual grammar corrections and spelling translation.")
        ctk.CTkLabel(self.about_page_frame, text=about_text, font=ctk.CTkFont(size=14), justify="left").pack(pady=10, padx=20, fill="x", anchor="w")
        self.about_page_frame.grid_forget()

        # --- Page 3: Settings ---
        self.settings_page_frame = ctk.CTkFrame(self, corner_radius=0) # Color set by apply_theme
        self.settings_page_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        ctk.CTkLabel(self.settings_page_frame, text="Settings", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20, anchor="w")

        # --- Appearance Settings ---
        self.appearance_frame = ctk.CTkFrame(self.settings_page_frame, corner_radius=10) # Color set by apply_theme
        self.appearance_frame.pack(fill="x", padx=20, pady=10, anchor="w")
        ctk.CTkLabel(self.appearance_frame, text="Appearance Mode", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5), padx=20, anchor="w")
        radio_light = ctk.CTkRadioButton(self.appearance_frame, text="Light Mode", variable=self.theme_radio_var, value="light", command=self.change_theme)
        radio_light.pack(pady=5, padx=20, anchor="w")
        radio_dark = ctk.CTkRadioButton(self.appearance_frame, text="Dark Mode", variable=self.theme_radio_var, value="dark", command=self.change_theme)
        radio_dark.pack(pady=5, padx=20, anchor="w")
        radio_system = ctk.CTkRadioButton(self.appearance_frame, text="Adapt to Device (System)", variable=self.theme_radio_var, value="system", command=self.change_theme)
        radio_system.pack(pady=(5, 10), padx=20, anchor="w")

        # --- Language Model Settings ---
        self.language_frame = ctk.CTkFrame(self.settings_page_frame, corner_radius=10) # Color set by apply_theme
        self.language_frame.pack(fill="x", padx=20, pady=10, anchor="w")
        ctk.CTkLabel(self.language_frame, text="Language Models", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 15), padx=20, anchor="w")

        for i, (lang_code, details) in enumerate(SUPPORTED_MODELS.items()):
            model_frame = ctk.CTkFrame(self.language_frame, fg_color="transparent")
            model_frame.pack(fill="x", padx=20, pady=5)
            model_frame.grid_columnconfigure(1, weight=1)

            lang_radio = ctk.CTkRadioButton(model_frame, text=details["name"], width=200, value=lang_code, command=lambda lc=lang_code: self.load_selected_model(lc))
            lang_radio.grid(row=0, column=0, sticky="w")

            self.language_status_labels[lang_code] = ctk.CTkLabel(model_frame, text="Status: Unknown", font=ctk.CTkFont(size=12)) # Color set by apply_theme
            self.language_status_labels[lang_code].grid(row=0, column=1, sticky="w", padx=10)

            self.language_progress_bars[lang_code] = ctk.CTkProgressBar(model_frame, width=150)
            self.language_progress_bars[lang_code].set(0)

            if details["hf_id"]:
                self.language_buttons[lang_code] = ctk.CTkButton(
                    model_frame, text="↓", width=30, height=30, # Smaller button
                    font=ctk.CTkFont(size=16), corner_radius=5, # Slightly rounded
                    command=lambda lc=lang_code: self.start_download_thread(lc)
                ) # Colors set by apply_theme
                self.language_buttons[lang_code].grid(row=0, column=3, sticky="e")
            else:
                 ctk.CTkLabel(model_frame, text="(Coming Soon)", font=ctk.CTkFont(size=12, slant="italic"), text_color=self.current_theme.get("DISABLED_COLOR", "#AAAAAA")).grid(row=0, column=3, sticky="e", padx=10)

        self.settings_page_frame.grid_forget()

    # --- CORE APP FUNCTIONS ---
    def toggle_sidebar(self):
        if self.sidebar_expanded.winfo_viewable():
            self.sidebar_expanded.grid_forget()
            self.sidebar_collapsed.grid(row=0, column=0, sticky="nsw")
        else:
            self.sidebar_collapsed.grid_forget()
            self.sidebar_expanded.grid(row=0, column=0, sticky="nsw")

    def show_page(self, page_name):
        # Hide all pages
        self.corrector_page_frame.grid_forget()
        self.about_page_frame.grid_forget()
        self.settings_page_frame.grid_forget()
        
        # Show the selected page
        if page_name == "corrector":
            self.corrector_page_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        elif page_name == "about":
            self.about_page_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        elif page_name == "settings":
            self.settings_page_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            
        # Update button styles AFTER showing page
        self.highlight_active_page_button()


    def change_theme(self):
        mode = self.theme_radio_var.get()
        ctk.set_appearance_mode(mode)
        print(f"Appearance mode changed to: {mode}")
        if mode == "light":
            self.apply_theme(LIGHT_THEME)
        else: # Dark or System (which defaults to dark here)
            self.apply_theme(DARK_THEME)

    # --- Language Model Handling ---
    def update_language_statuses(self):
        """ Checks download status for all models and updates the GUI. """
        theme = self.current_theme
        for lang_code, details in SUPPORTED_MODELS.items():
            status_label = self.language_status_labels.get(lang_code)
            download_button = self.language_buttons.get(lang_code)
            
            if not status_label: continue

            status_color = theme.get("DISABLED_COLOR", "#AAAAAA") # Default grey
            status_text = "Status: Unknown"

            if details["hf_id"] is None:
                 status_text = "Status: Not Available"
                 if download_button: download_button.grid_forget()

            elif check_if_model_downloaded(lang_code):
                status_text = "Status: Downloaded"
                status_color = "lightgreen"
                if download_button: download_button.grid_forget() # Hide download button
            else:
                status_text = "Status: Not Downloaded"
                if download_button: download_button.grid(row=0, column=3, sticky="e") # Show download button

            status_label.configure(text=status_text, text_color=status_color)

    def start_download_thread(self, lang_code):
        """ Starts downloading a model in a background thread. """
        if self.is_loading:
            self.show_themed_messagebox("Busy", "Another operation is already in progress.", msg_type="warning")
            return
            
        btn = self.language_buttons.get(lang_code)
        prog_bar = self.language_progress_bars.get(lang_code)
        status_label = self.language_status_labels.get(lang_code)

        if btn: btn.configure(state="disabled", text="...")
        if prog_bar:
            prog_bar.grid(row=0, column=2, sticky="e", padx=5) # Show progress bar
            prog_bar.set(0)
            prog_bar.configure(progress_color=self.current_theme["TEXT_COLOR"]) # Set bar color based on theme
        if status_label: status_label.configure(text="Status: Downloading...", text_color="yellow")

        self.is_loading = True
        download_thread = threading.Thread(target=self.download_model_thread, args=(lang_code,), daemon=True)
        download_thread.start()

    def download_model_thread(self, lang_code):
        """ --- RUNS IN BACKGROUND THREAD --- """
        print(f"[Thread] Starting download for {lang_code}...")
        def progress_update(message, percentage):
            self.after(0, self.update_download_progress, lang_code, message, percentage)
        success = download_model_for_language(lang_code, progress_callback=progress_update)
        self.after(0, self.on_download_complete, lang_code, success)

    def update_download_progress(self, lang_code, message, percentage):
        """ --- RUNS IN MAIN GUI THREAD --- Updates progress bar and status. """
        prog_bar = self.language_progress_bars.get(lang_code)
        status_label = self.language_status_labels.get(lang_code)
        if status_label: status_label.configure(text=f"Status: {message}")
        if prog_bar: prog_bar.set(percentage / 100)

    def on_download_complete(self, lang_code, success):
        """ --- RUNS IN MAIN GUI THREAD --- Called when download finishes. """
        self.is_loading = False
        prog_bar = self.language_progress_bars.get(lang_code)
        btn = self.language_buttons.get(lang_code)

        if prog_bar: prog_bar.grid_forget() # Hide progress bar
        if btn: btn.configure(state="normal", text="↓") # Re-enable if failed
        
        self.update_language_statuses() # Refresh status labels/buttons

        if success:
            self.show_themed_messagebox("Download Complete", f"Model for {SUPPORTED_MODELS[lang_code]['name']} downloaded successfully.", msg_type="info")
        else:
            self.show_themed_messagebox("Download Failed", f"Could not download model for {SUPPORTED_MODELS[lang_code]['name']}.\nCheck console for errors.", msg_type="error")

    def load_selected_model(self, lang_code, initial_load=False):
        """ Attempts to load the model for the selected language. """
        if self.is_loading:
             if not initial_load: self.show_themed_messagebox("Busy", "Please wait for the current operation to finish.", msg_type="warning")
             return
             
        if not check_if_model_downloaded(lang_code):
            if not initial_load: self.show_themed_messagebox("Error", f"Model for {SUPPORTED_MODELS[lang_code]['name']} is not downloaded.\nPlease download it from Settings first.", msg_type="error")
            self.update_corrector_status(f"Model: [{SUPPORTED_MODELS[lang_code]['name']} - Not Downloaded]", error=True)
            self.model = None # Unload any previous model
            self.tokenizer = None
            self.current_lang_code = None
            return

        if self.current_lang_code == lang_code and self.model is not None:
            print(f"Model for {lang_code} already loaded.")
            self.update_corrector_status(f"Model: [{SUPPORTED_MODELS[lang_code]['name']}] - Ready") # Ensure status is correct
            return # Avoid reloading the same model

        self.is_loading = True
        self.update_corrector_status(f"Loading Model: [{SUPPORTED_MODELS[lang_code]['name']}]...", loading=True)

        load_thread = threading.Thread(target=self.load_model_thread, args=(lang_code,), daemon=True)
        load_thread.start()

    def load_model_thread(self, lang_code):
        """ --- RUNS IN BACKGROUND --- """
        print(f"[Thread] Starting model load for {lang_code}...")
        new_model, new_tokenizer = load_model_from_disk(lang_code)
        self.after(0, self.on_load_model_complete, lang_code, new_model, new_tokenizer)

    def on_load_model_complete(self, lang_code, loaded_model, loaded_tokenizer):
         """ --- RUNS IN MAIN GUI --- """
         self.is_loading = False
         if loaded_model and loaded_tokenizer:
             self.model = loaded_model
             self.tokenizer = loaded_tokenizer
             self.current_lang_code = lang_code
             self.update_corrector_status(f"Model: [{SUPPORTED_MODELS[lang_code]['name']}] - Ready")
             # Only show pop-up on explicit user selection, not initial load
             if hasattr(self, '_initial_load_done') and self._initial_load_done:
                 self.show_themed_messagebox("Model Loaded", f"{SUPPORTED_MODELS[lang_code]['name']} model loaded successfully.", msg_type="info")
         else:
             self.update_corrector_status(f"Error loading model: [{SUPPORTED_MODELS[lang_code]['name']}]", error=True)
             self.model = None
             self.tokenizer = None
             self.current_lang_code = None
             if hasattr(self, '_initial_load_done') and self._initial_load_done:
                 self.show_themed_messagebox("Load Failed", f"Could not load model for {SUPPORTED_MODELS[lang_code]['name']}.\nFiles might be corrupt.", msg_type="error")
         self._initial_load_done = True # Mark initial load as done


    def update_corrector_status(self, message, loading=False, error=False):
        """ Updates the language indicator label and button states. """
        theme = self.current_theme
        self.lang_indicator_label.configure(text=message)
        status_color = theme["TEXT_COLOR"] # Default
        if loading: status_color = "#AAAAAA"
        if error: status_color = "red"
        if not self.model: status_color = theme.get("DISABLED_COLOR", "#AAAAAA") # If no model loaded
        if self.model and not loading and not error: status_color = "lightgreen" # Ready state

        self.lang_indicator_label.configure(text_color=status_color)

        if loading or error or not self.model:
            self.corrector_button_middle.configure(state="disabled")
            self.corrector_input_textbox.configure(state="disabled")
        else:
            self.corrector_button_middle.configure(state="normal")
            self.corrector_input_textbox.configure(state="normal")

    def on_correct_click(self):
        """ Handles the correction button click, including warnings. """
        if not self.model or not self.tokenizer or not self.current_lang_code:
            self.show_themed_messagebox("No Model Loaded", "Please select and ensure a language model is downloaded and loaded via the Settings page before correcting text.", msg_type="warning")
            return

        input_text = self.corrector_input_textbox.get("1.0", "end-1c").strip()
        if len(input_text) < 1: return

        print(f"Original text: '{input_text}'")
        self.corrector_button_middle.configure(text="...", state="disabled")
        self.update_idletasks()

        # --- HYBRID SPELL CHECK ---
        spell = SpellChecker(case_sensitive=False)
        spell.word_frequency.add("komal")
        spell.word_frequency.add("jampani")
        spell.word_frequency.add("name", 1000000)
        words = input_text.split()
        misspelled = spell.unknown(words)
        corrected_words = []
        for word in words:
            if word in misspelled:
                corrected_word = spell.correction(word)
                if corrected_word and corrected_word != word.lower():
                    if word.istitle(): corrected_word = corrected_word.title()
                    elif word.isupper(): corrected_word = corrected_word.upper()
                    corrected_words.append(corrected_word)
                else: corrected_words.append(word)
            else: corrected_words.append(word)
        spell_checked_text = " ".join(corrected_words)
        print(f"Spell-checked text: '{spell_checked_text}'")

        # --- GRAMMAR/TRANSLATION CHECK ---
        corrected_text = correct_grammar(spell_checked_text, self.model, self.tokenizer, self.current_lang_code)

        self.corrector_output_textbox.configure(state="normal")
        self.corrector_output_textbox.delete("1.0", tk.END)
        self.corrector_output_textbox.insert("1.0", corrected_text)
        self.corrector_output_textbox.configure(state="disabled")
        self.corrector_button_middle.configure(text=">>", state="normal")

    # --- Utility: Themed Pop-up ---
    def show_themed_messagebox(self, title, message, msg_type="info"):
        """ Creates a custom Toplevel window for themed messages. """
        popup = ctk.CTkToplevel(self)
        popup.geometry("400x150")
        popup.title(title)
        popup.configure(fg_color=self.current_theme["ENTRY_COLOR"])
        popup.grab_set() # Make modal
        popup.transient(self)

        icon_text = "ⓘ" if msg_type == "info" else "⚠" if msg_type == "warning" else "❌"
        icon_color = "lightgreen" if msg_type == "info" else "yellow" if msg_type == "warning" else "red"

        icon_label = ctk.CTkLabel(popup, text=icon_text, font=ctk.CTkFont(size=24), text_color=icon_color)
        icon_label.pack(side="left", padx=15)

        message_label = ctk.CTkLabel(popup, text=message, font=ctk.CTkFont(size=13), justify="left", text_color=self.current_theme["TEXT_COLOR"], wraplength=280)
        message_label.pack(side="left", padx=10, pady=20, fill="x", expand=True)

        ok_button = ctk.CTkButton(popup, text="OK", width=80, command=popup.destroy,
                                  fg_color=self.current_theme["BTN_COLOR"], text_color=self.current_theme["BTN_TEXT_COLOR"], hover_color=self.current_theme["BTN_HOVER_COLOR"])
        ok_button.pack(side="bottom", pady=10)

# --- START THE APPLICATION ---
if __name__ == "__main__":
    app = App()
    app.mainloop()
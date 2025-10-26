import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as messagebox # Keep for fallback if needed
import threading
import os
from correct import (SUPPORTED_MODELS, check_if_model_downloaded,
                     download_model_for_language, load_model_from_disk,
                     correct_grammar, get_model_path)
from spellchecker import SpellChecker

# --- THEME DEFINITIONS ---
DARK_THEME = { "BG_COLOR": "#000000", "MENU_COLOR": "#1C1C1C", "ENTRY_COLOR": "#1C1C1C", "TEXT_COLOR": "#FFFFFF", "BTN_COLOR": "#FFFFFF", "BTN_TEXT_COLOR": "#000000", "BTN_HOVER_COLOR": "#E0E0E0", "ICON_HOVER_COLOR": "#333333", "DOWNLOAD_BTN_FG_COLOR": "transparent", "DOWNLOAD_BTN_TEXT": "#FFFFFF", "DOWNLOAD_BTN_HOVER": "#333333", "DISABLED_COLOR": "#555555", "BORDER_COLOR": "#FFFFFF", "PROGRESS_COLOR": "#FFFFFF", "POPUP_BG": "#1C1C1C", "POPUP_TEXT": "#FFFFFF" }
LIGHT_THEME = { "BG_COLOR": "#EAEAEA", "MENU_COLOR": "#F5F5F5", "ENTRY_COLOR": "#FFFFFF", "TEXT_COLOR": "#000000", "BTN_COLOR": "#000000", "BTN_TEXT_COLOR": "#FFFFFF", "BTN_HOVER_COLOR": "#333333", "ICON_HOVER_COLOR": "#CCCCCC", "DOWNLOAD_BTN_FG_COLOR": "transparent", "DOWNLOAD_BTN_TEXT": "#000000", "DOWNLOAD_BTN_HOVER": "#CCCCCC", "DISABLED_COLOR": "#AAAAAA", "BORDER_COLOR": "#000000", "PROGRESS_COLOR": "#000000", "POPUP_BG": "#F5F5F5", "POPUP_TEXT": "#000000" }

# --- MAIN APPLICATION CLASS ---
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Corrector v2.3")
        self.geometry("1100x600")
        ctk.set_appearance_mode("dark")
        self.current_lang_code = None
        self.model = None
        self.tokenizer = None
        self.is_loading = False
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.theme_radio_var = tk.StringVar(value="dark")
        self.language_buttons = {}
        self.language_progress_bars = {}
        self.language_status_labels = {}
        self.current_theme = DARK_THEME
        self.create_sidebars()
        self.create_pages()
        self.apply_theme(self.current_theme)
        self.update_language_statuses()
        self.show_page("corrector")
        self.load_selected_model("en_us", initial_load=True)

    # --- Theme Application ---
    def apply_theme(self, theme):
        self.current_theme = theme
        self.configure(fg_color=theme["BG_COLOR"])
        self.sidebar_expanded.configure(fg_color=theme["MENU_COLOR"])
        self.sidebar_collapsed.configure(fg_color=theme["MENU_COLOR"])
        for widget in self.sidebar_expanded.winfo_children() + self.sidebar_collapsed.winfo_children():
            if isinstance(widget, ctk.CTkLabel): widget.configure(text_color=theme["TEXT_COLOR"])
            elif isinstance(widget, ctk.CTkButton): widget.configure(text_color=theme["TEXT_COLOR"], hover_color=theme["ICON_HOVER_COLOR"])
        self.corrector_page_frame.configure(fg_color=theme["BG_COLOR"])
        self.about_page_frame.configure(fg_color=theme["BG_COLOR"])
        self.settings_page_frame.configure(fg_color=theme["BG_COLOR"])
        for child in self.corrector_page_frame.winfo_children():
            if isinstance(child, ctk.CTkLabel): child.configure(text_color=theme["TEXT_COLOR"])
            elif isinstance(child, ctk.CTkTextbox): child.configure(fg_color=theme["ENTRY_COLOR"], text_color=theme["TEXT_COLOR"], border_color=theme["BORDER_COLOR"])
            elif isinstance(child, ctk.CTkButton): child.configure(fg_color=theme["BTN_COLOR"], text_color=theme["BTN_TEXT_COLOR"], hover_color=theme["BTN_HOVER_COLOR"])
            elif isinstance(child, ctk.CTkFrame): child.configure(fg_color=theme["BG_COLOR"])
        self.corrector_button_middle.configure(fg_color=theme["BTN_COLOR"], text_color=theme["BTN_TEXT_COLOR"], hover_color=theme["BTN_HOVER_COLOR"])
        for child in self.about_page_frame.winfo_children():
            if isinstance(child, ctk.CTkLabel): child.configure(text_color=theme["TEXT_COLOR"])
        for child in self.settings_page_frame.winfo_children():
            if isinstance(child, ctk.CTkLabel): child.configure(text_color=theme["TEXT_COLOR"])
            elif isinstance(child, ctk.CTkFrame):
                child.configure(fg_color=theme["ENTRY_COLOR"])
                for sub_child in child.winfo_children():
                    if isinstance(sub_child, ctk.CTkLabel): sub_child.configure(text_color=theme["TEXT_COLOR"])
                    elif isinstance(sub_child, ctk.CTkRadioButton): sub_child.configure(text_color=theme["TEXT_COLOR"])
                    elif isinstance(sub_child, ctk.CTkOptionMenu): sub_child.configure(fg_color=theme["ENTRY_COLOR"], text_color=theme["TEXT_COLOR"], button_color=theme["ENTRY_COLOR"], dropdown_fg_color=theme["ENTRY_COLOR"], dropdown_text_color=theme["TEXT_COLOR"])
                    elif isinstance(sub_child, ctk.CTkFrame):
                        sub_child.configure(fg_color="transparent")
                        for model_widget in sub_child.winfo_children():
                            if isinstance(model_widget, ctk.CTkRadioButton): model_widget.configure(text_color=theme["TEXT_COLOR"])
                            elif isinstance(model_widget, ctk.CTkLabel) and model_widget.cget("text") != "(Coming Soon)": pass
                            elif isinstance(model_widget, ctk.CTkLabel) and model_widget.cget("text") == "(Coming Soon)": model_widget.configure(text_color=theme["DISABLED_COLOR"])
                            elif isinstance(model_widget, ctk.CTkButton): model_widget.configure(fg_color=theme["DOWNLOAD_BTN_FG_COLOR"], text_color=theme["DOWNLOAD_BTN_TEXT"], hover_color=theme["DOWNLOAD_BTN_HOVER"])
                            elif isinstance(model_widget, ctk.CTkProgressBar): model_widget.configure(progress_color=theme["PROGRESS_COLOR"])
        self.highlight_active_page_button()
        self.update_language_statuses()

    def highlight_active_page_button(self):
         theme = self.current_theme
         self.corrector_btn_exp.configure(fg_color="transparent", text_color=theme["TEXT_COLOR"], hover_color=theme["ICON_HOVER_COLOR"])
         self.about_btn_exp.configure(fg_color="transparent", text_color=theme["TEXT_COLOR"], hover_color=theme["ICON_HOVER_COLOR"])
         self.settings_btn_exp.configure(fg_color="transparent", text_color=theme["TEXT_COLOR"], hover_color=theme["ICON_HOVER_COLOR"])
         if self.corrector_page_frame.winfo_viewable(): self.corrector_btn_exp.configure(fg_color=theme["BTN_COLOR"], text_color=theme["BTN_TEXT_COLOR"], hover_color=theme["BTN_HOVER_COLOR"])
         elif self.about_page_frame.winfo_viewable(): self.about_btn_exp.configure(fg_color=theme["BTN_COLOR"], text_color=theme["BTN_TEXT_COLOR"], hover_color=theme["BTN_HOVER_COLOR"])
         elif self.settings_page_frame.winfo_viewable(): self.settings_btn_exp.configure(fg_color=theme["BTN_COLOR"], text_color=theme["BTN_TEXT_COLOR"], hover_color=theme["BTN_HOVER_COLOR"])

    # --- GUI Creation ---
    def create_sidebars(self):
        # --- EXPANDED ---
        self.sidebar_expanded = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_expanded.grid(row=0, column=0, sticky="nsw")
        self.sidebar_expanded.grid_rowconfigure(5, weight=1) # MOVED Spacer row index

        self.menu_toggle_btn_exp = ctk.CTkButton(self.sidebar_expanded, text="☰", font=ctk.CTkFont(size=20), width=40, fg_color="transparent", command=self.toggle_sidebar, anchor="w")
        self.menu_toggle_btn_exp.grid(row=0, column=0, pady=20, padx=20, sticky="w")
        self.title_label_exp = ctk.CTkLabel(self.sidebar_expanded, text="AI Corrector", font=ctk.CTkFont(size=22, weight="bold"), anchor="w")
        self.title_label_exp.grid(row=1, column=0, pady=(0, 20), padx=20, sticky="w")
        self.corrector_btn_exp = ctk.CTkButton(self.sidebar_expanded, text="✎  Corrector", font=ctk.CTkFont(size=14, weight="bold"), anchor="w", corner_radius=8, command=lambda: self.show_page("corrector"))
        self.corrector_btn_exp.grid(row=2, column=0, pady=5, padx=20, sticky="ew")
        self.about_btn_exp = ctk.CTkButton(self.sidebar_expanded, text="ⓘ  About Us", font=ctk.CTkFont(size=14, weight="bold"), anchor="w", corner_radius=8, command=lambda: self.show_page("about"))
        self.about_btn_exp.grid(row=3, column=0, pady=5, padx=20, sticky="ew")
        # REMOVED Language dropdown from here
        self.settings_btn_exp = ctk.CTkButton(self.sidebar_expanded, text="⚙  Settings", font=ctk.CTkFont(size=14, weight="bold"), anchor="w", corner_radius=8, command=lambda: self.show_page("settings"))
        self.settings_btn_exp.grid(row=6, column=0, pady=20, padx=20, sticky="s") # Use row 6 for bottom

        # --- COLLAPSED ---
        self.sidebar_collapsed = ctk.CTkFrame(self, width=70, corner_radius=0)
        self.sidebar_collapsed.grid(row=0, column=0, sticky="nsw")
        self.sidebar_collapsed.grid_rowconfigure(1, weight=1)
        self.menu_toggle_btn_col = ctk.CTkButton(self.sidebar_collapsed, text="☰", font=ctk.CTkFont(size=20), width=40, fg_color="transparent", command=self.toggle_sidebar, anchor="center")
        self.menu_toggle_btn_col.grid(row=0, column=0, pady=20, padx=15, sticky="w")
        self.settings_btn_col = ctk.CTkButton(self.sidebar_collapsed, text="⚙", font=ctk.CTkFont(size=20), width=40, fg_color="transparent", corner_radius=8, command=lambda: [self.toggle_sidebar(), self.show_page("settings")])
        self.settings_btn_col.grid(row=2, column=0, pady=20, padx=15, sticky="s")
        self.sidebar_collapsed.grid_forget()

    def create_pages(self):
        # --- Page 1: Corrector ---
        self.corrector_page_frame = ctk.CTkFrame(self, corner_radius=0)
        self.corrector_page_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.corrector_page_frame.grid_columnconfigure((0, 2), weight=1)
        self.corrector_page_frame.grid_columnconfigure(1, weight=0)
        self.corrector_page_frame.grid_rowconfigure(2, weight=1)

        self.lang_indicator_label = ctk.CTkLabel(self.corrector_page_frame, text="Model: [None Loaded]", font=ctk.CTkFont(size=12))
        self.lang_indicator_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

        # ADDED Button to jump to settings
        lang_settings_btn = ctk.CTkButton(self.corrector_page_frame, text="Change Model...", command=lambda: self.show_page("settings"), width=100, height=20, font=ctk.CTkFont(size=10))
        lang_settings_btn.grid(row=0, column=2, sticky="e", pady=(0,5))


        ctk.CTkLabel(self.corrector_page_frame, text="Input Text:", font=ctk.CTkFont(size=14)).grid(row=1, column=0, sticky="w", pady=(0, 5))
        self.corrector_input_textbox = ctk.CTkTextbox(self.corrector_page_frame, corner_radius=10, font=ctk.CTkFont(size=13), border_width=1)
        self.corrector_input_textbox.grid(row=2, column=0, sticky="nsew", padx=(0, 10))
        middle_button_frame = ctk.CTkFrame(self.corrector_page_frame)
        middle_button_frame.grid(row=2, column=1, sticky="ns", padx=5)
        self.corrector_button_middle = ctk.CTkButton(middle_button_frame, text=">>", width=50, font=ctk.CTkFont(size=16, weight="bold"), corner_radius=8, command=self.on_correct_click, state="disabled")
        self.corrector_button_middle.pack(expand=True)
        ctk.CTkLabel(self.corrector_page_frame, text="Corrected Text:", font=ctk.CTkFont(size=14)).grid(row=1, column=2, sticky="w", pady=(0, 5))
        self.corrector_output_textbox = ctk.CTkTextbox(self.corrector_page_frame, corner_radius=10, font=ctk.CTkFont(size=13), state="disabled", border_width=1)
        self.corrector_output_textbox.grid(row=2, column=2, sticky="nsew", padx=(10, 0))

        # --- Page 2: About Us ---
        self.about_page_frame = ctk.CTkFrame(self, corner_radius=0)
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
        self.settings_page_frame = ctk.CTkFrame(self, corner_radius=0)
        self.settings_page_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        ctk.CTkLabel(self.settings_page_frame, text="Settings", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20, anchor="w")

        # --- Appearance ---
        self.appearance_frame = ctk.CTkFrame(self.settings_page_frame, corner_radius=10)
        self.appearance_frame.pack(fill="x", padx=20, pady=10, anchor="w")
        ctk.CTkLabel(self.appearance_frame, text="Appearance Mode", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5), padx=20, anchor="w")
        radio_light = ctk.CTkRadioButton(self.appearance_frame, text="Light Mode", variable=self.theme_radio_var, value="light", command=self.change_theme)
        radio_light.pack(pady=5, padx=20, anchor="w")
        radio_dark = ctk.CTkRadioButton(self.appearance_frame, text="Dark Mode", variable=self.theme_radio_var, value="dark", command=self.change_theme)
        radio_dark.pack(pady=5, padx=20, anchor="w")
        radio_system = ctk.CTkRadioButton(self.appearance_frame, text="Adapt to Device (System)", variable=self.theme_radio_var, value="system", command=self.change_theme)
        radio_system.pack(pady=(5, 10), padx=20, anchor="w")

        # --- Language Models ---
        self.language_frame = ctk.CTkFrame(self.settings_page_frame, corner_radius=10)
        self.language_frame.pack(fill="x", padx=20, pady=10, anchor="w")
        ctk.CTkLabel(self.language_frame, text="Language Models", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5), padx=20, anchor="w")

        # MOVED Language Dropdown HERE
        lang_select_frame = ctk.CTkFrame(self.language_frame, fg_color="transparent")
        lang_select_frame.pack(fill="x", padx=20, pady=(5, 15))
        ctk.CTkLabel(lang_select_frame, text="Active Language:", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 10))
        self.lang_menu_settings = ctk.CTkOptionMenu(
            lang_select_frame,
            values=[details["name"] for details in SUPPORTED_MODELS.values()],
            command=self.on_language_select_settings # New command to handle selection
        )
        self.lang_menu_settings.pack(side="left")

        # Download Area Title
        ctk.CTkLabel(self.language_frame, text="Download Models:", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5), padx=20, anchor="w")

        for i, (lang_code, details) in enumerate(SUPPORTED_MODELS.items()):
            model_frame = ctk.CTkFrame(self.language_frame, fg_color="transparent")
            model_frame.pack(fill="x", padx=20, pady=5)
            model_frame.grid_columnconfigure(1, weight=1)
            model_frame.widgetName = f"model_frame_{lang_code}"

            lang_label_settings = ctk.CTkLabel(model_frame, text=details["name"], width=200) # Use Label instead of Radio
            lang_label_settings.grid(row=0, column=0, sticky="w")
            lang_label_settings.widgetName = "lang_label"

            self.language_status_labels[lang_code] = ctk.CTkLabel(model_frame, text="Status: Unknown", font=ctk.CTkFont(size=12))
            self.language_status_labels[lang_code].grid(row=0, column=1, sticky="w", padx=10)
            self.language_status_labels[lang_code].widgetName = "status_label"

            self.language_progress_bars[lang_code] = ctk.CTkProgressBar(model_frame, width=150)
            self.language_progress_bars[lang_code].set(0)
            self.language_progress_bars[lang_code].widgetName = "progress_bar"

            if details["hf_id"]:
                self.language_buttons[lang_code] = ctk.CTkButton(
                    model_frame, text="↓", width=30, height=30,
                    font=ctk.CTkFont(size=18), corner_radius=5, # Make icon slightly bigger
                    fg_color="transparent", # CHANGED: Icon Style Button
                    border_width=0, # CHANGED: No border
                    command=lambda lc=lang_code: self.start_download_thread(lc)
                )
                self.language_buttons[lang_code].grid(row=0, column=3, sticky="e")
                self.language_buttons[lang_code].widgetName = "download_button"
            else:
                 coming_soon = ctk.CTkLabel(model_frame, text="(Coming Soon)", font=ctk.CTkFont(size=12, slant="italic"))
                 coming_soon.grid(row=0, column=3, sticky="e", padx=10)
                 coming_soon.widgetName = "coming_soon_label"
        self.settings_page_frame.grid_forget()

    # --- CORE APP FUNCTIONS ---
    def toggle_sidebar(self):
        if self.sidebar_expanded.winfo_viewable():
            self.sidebar_expanded.grid_forget(); self.sidebar_collapsed.grid(row=0, column=0, sticky="nsw")
        else:
            self.sidebar_collapsed.grid_forget(); self.sidebar_expanded.grid(row=0, column=0, sticky="nsw")

    def show_page(self, page_name):
        self.corrector_page_frame.grid_forget(); self.about_page_frame.grid_forget(); self.settings_page_frame.grid_forget()
        if page_name == "corrector": self.corrector_page_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        elif page_name == "about": self.about_page_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        elif page_name == "settings": self.settings_page_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.highlight_active_page_button()

    def change_theme(self):
        mode = self.theme_radio_var.get()
        ctk.set_appearance_mode(mode)
        print(f"Appearance mode changed to: {mode}")
        if mode == "light": self.apply_theme(LIGHT_THEME)
        else: self.apply_theme(DARK_THEME)

    # --- Language Model Handling ---
    def update_language_statuses(self):
        theme = self.current_theme
        for lang_code, details in SUPPORTED_MODELS.items():
            status_label = self.language_status_labels.get(lang_code)
            download_button = self.language_buttons.get(lang_code)
            if not status_label: continue
            status_color = theme.get("DISABLED_COLOR", "#AAAAAA"); status_text = "Status: Unknown"
            if details["hf_id"] is None:
                 status_text = "Status: Not Available"; status_color = theme.get("DISABLED_COLOR", "#AAAAAA")
                 if download_button: download_button.grid_forget()
            elif check_if_model_downloaded(lang_code):
                status_text = "Status: Downloaded"; status_color = "lightgreen"
                if download_button: download_button.grid_forget()
            else:
                status_text = "Status: Not Downloaded"; status_color = theme.get("DISABLED_COLOR", "#AAAAAA")
                if download_button: download_button.grid(row=0, column=3, sticky="e")
            status_label.configure(text=status_text, text_color=status_color)

    def start_download_thread(self, lang_code):
        if self.is_loading: self.show_themed_messagebox("Busy", "Another operation is already in progress.", msg_type="warning"); return
        btn = self.language_buttons.get(lang_code); prog_bar = self.language_progress_bars.get(lang_code); status_label = self.language_status_labels.get(lang_code)
        if btn: btn.configure(state="disabled", text="...")
        if prog_bar: prog_bar.grid(row=0, column=2, sticky="e", padx=5); prog_bar.set(0); prog_bar.configure(progress_color=self.current_theme["PROGRESS_COLOR"])
        if status_label: status_label.configure(text="Status: Downloading...", text_color="yellow")
        self.is_loading = True
        download_thread = threading.Thread(target=self.download_model_thread, args=(lang_code,), daemon=True)
        download_thread.start()

    def download_model_thread(self, lang_code):
        print(f"[Thread] Starting download for {lang_code}...")
        def progress_update(message, percentage): self.after(0, self.update_download_progress, lang_code, message, percentage)
        success = download_model_for_language(lang_code, progress_callback=progress_update)
        self.after(0, self.on_download_complete, lang_code, success)

    def update_download_progress(self, lang_code, message, percentage):
        prog_bar = self.language_progress_bars.get(lang_code); status_label = self.language_status_labels.get(lang_code)
        if status_label: status_label.configure(text=f"Status: {message}")
        if prog_bar: prog_bar.set(percentage / 100)

    def on_download_complete(self, lang_code, success):
        self.is_loading = False
        prog_bar = self.language_progress_bars.get(lang_code); btn = self.language_buttons.get(lang_code)
        if prog_bar: prog_bar.grid_forget()
        if btn: btn.configure(state="normal", text="↓")
        self.update_language_statuses()
        if success: self.show_themed_messagebox("Download Complete", f"Model for {SUPPORTED_MODELS[lang_code]['name']} downloaded successfully.", msg_type="info")
        else: self.show_themed_messagebox("Download Failed", f"Could not download model for {SUPPORTED_MODELS[lang_code]['name']}.\nCheck console for errors.", msg_type="error")

    def on_language_select_settings(self, selected_language_name):
         """ Triggered when user selects a language from the OptionMenu in Settings. """
         lang_code_to_load = None
         for code, details in SUPPORTED_MODELS.items():
             if details["name"] == selected_language_name:
                 lang_code_to_load = code
                 break
         if lang_code_to_load:
             self.load_selected_model(lang_code_to_load)
         else:
             print(f"Error: Could not find lang code for selected name: {selected_language_name}")


    def load_selected_model(self, lang_code, initial_load=False):
        if self.is_loading:
             if not initial_load: self.show_themed_messagebox("Busy", "Please wait for the current operation to finish.", msg_type="warning")
             return
        if not check_if_model_downloaded(lang_code):
            if not initial_load: self.show_themed_messagebox("Error", f"Model for {SUPPORTED_MODELS[lang_code]['name']} is not downloaded.\nPlease download it from Settings first.", msg_type="error")
            self.update_corrector_status(f"Model: [{SUPPORTED_MODELS[lang_code]['name']} - Not Downloaded]", error=True)
            self.model, self.tokenizer, self.current_lang_code = None, None, None
            if hasattr(self, 'lang_menu_settings'): self.lang_menu_settings.set("Select Language") # Reset dropdown
            return
        if self.current_lang_code == lang_code and self.model is not None:
            print(f"Model for {lang_code} already loaded."); self.update_corrector_status(f"Model: [{SUPPORTED_MODELS[lang_code]['name']}] - Ready")
            if hasattr(self, 'lang_menu_settings'): self.lang_menu_settings.set(SUPPORTED_MODELS[lang_code]['name']) # Ensure dropdown matches
            return
        self.is_loading = True
        self.update_corrector_status(f"Loading Model: [{SUPPORTED_MODELS[lang_code]['name']}]...", loading=True)
        load_thread = threading.Thread(target=self.load_model_thread, args=(lang_code,), daemon=True)
        load_thread.start()

    def load_model_thread(self, lang_code):
        print(f"[Thread] Starting model load for {lang_code}...")
        new_model, new_tokenizer = load_model_from_disk(lang_code)
        self.after(0, self.on_load_model_complete, lang_code, new_model, new_tokenizer)

    def on_load_model_complete(self, lang_code, loaded_model, loaded_tokenizer):
         self.is_loading = False
         display_name = SUPPORTED_MODELS[lang_code]['name']
         if loaded_model and loaded_tokenizer:
             self.model, self.tokenizer, self.current_lang_code = loaded_model, loaded_tokenizer, lang_code
             self.update_corrector_status(f"Model: [{display_name}] - Ready")
             if hasattr(self, 'lang_menu_settings'): self.lang_menu_settings.set(display_name) # Update dropdown
             if hasattr(self, '_initial_load_done') and self._initial_load_done: self.show_themed_messagebox("Model Loaded", f"{display_name} model loaded successfully.", msg_type="info")
         else:
             self.update_corrector_status(f"Error loading model: [{display_name}]", error=True)
             self.model, self.tokenizer, self.current_lang_code = None, None, None
             if hasattr(self, 'lang_menu_settings'): self.lang_menu_settings.set("Select Language") # Reset dropdown
             if hasattr(self, '_initial_load_done') and self._initial_load_done: self.show_themed_messagebox("Load Failed", f"Could not load model for {display_name}.\nFiles might be corrupt.", msg_type="error")
         self._initial_load_done = True

    def update_corrector_status(self, message, loading=False, error=False):
        theme = self.current_theme
        self.lang_indicator_label.configure(text=message)
        status_color = theme["TEXT_COLOR"]
        if loading: status_color = theme.get("DISABLED_COLOR", "#AAAAAA")
        if error: status_color = "red"
        if not self.model: status_color = theme.get("DISABLED_COLOR", "#AAAAAA")
        if self.model and not loading and not error: status_color = "lightgreen"
        self.lang_indicator_label.configure(text_color=status_color)
        btn_state = "disabled" if (loading or error or not self.model) else "normal"
        self.corrector_button_middle.configure(state=btn_state)
        self.corrector_input_textbox.configure(state="normal" if btn_state == "normal" else "disabled") # Match input state

    def on_correct_click(self):
        if not self.model or not self.tokenizer or not self.current_lang_code:
            self.show_themed_messagebox("No Model Loaded", "Please select and ensure a language model is downloaded and loaded via the Settings page before correcting text.", msg_type="warning"); return
        input_text = self.corrector_input_textbox.get("1.0", "end-1c").strip()
        if len(input_text) < 1: return
        print(f"Original text: '{input_text}'"); self.corrector_button_middle.configure(text="...", state="disabled"); self.update_idletasks()
        spell = SpellChecker(case_sensitive=False)
        spell.word_frequency.add("komal"); spell.word_frequency.add("jampani"); spell.word_frequency.add("name", 1000000)
        words = input_text.split(); misspelled = spell.unknown(words); corrected_words = []
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
        corrected_text = correct_grammar(spell_checked_text, self.model, self.tokenizer, self.current_lang_code)
        self.corrector_output_textbox.configure(state="normal"); self.corrector_output_textbox.delete("1.0", tk.END); self.corrector_output_textbox.insert("1.0", corrected_text); self.corrector_output_textbox.configure(state="disabled")
        self.corrector_button_middle.configure(text=">>", state="normal")

    # --- Utility: Themed Pop-up ---
    def show_themed_messagebox(self, title, message, msg_type="info"):
        try:
            popup = ctk.CTkToplevel(self)
            popup.geometry("400x150+"+str(self.winfo_rootx()+50)+"+"+str(self.winfo_rooty()+50))
            popup.title(title); popup.configure(fg_color=self.current_theme["POPUP_BG"]); popup.grab_set(); popup.transient(self)
            icon_text = "ⓘ" if msg_type == "info" else "⚠" if msg_type == "warning" else "❌"; icon_color = "lightgreen" if msg_type == "info" else "yellow" if msg_type == "warning" else "red"
            frame = ctk.CTkFrame(popup, fg_color="transparent"); frame.pack(pady=20, padx=20, fill="both", expand=True); frame.grid_columnconfigure(1, weight=1)
            icon_label = ctk.CTkLabel(frame, text=icon_text, font=ctk.CTkFont(size=30), text_color=icon_color); icon_label.grid(row=0, column=0, rowspan=2, padx=(0, 15), sticky="ns")
            message_label = ctk.CTkLabel(frame, text=message, font=ctk.CTkFont(size=13), justify="left", text_color=self.current_theme["POPUP_TEXT"], wraplength=280); message_label.grid(row=0, column=1, pady=(0, 10), sticky="nw")
            ok_button = ctk.CTkButton(frame, text="OK", width=80, command=popup.destroy, fg_color=self.current_theme["BTN_COLOR"], text_color=self.current_theme["BTN_TEXT_COLOR"], hover_color=self.current_theme["BTN_HOVER_COLOR"]); ok_button.grid(row=1, column=1, sticky="se")
            popup.after(100, popup.lift)
        except Exception as e:
            print(f"Error showing themed messagebox: {e}")
            fallback_func = messagebox.showinfo if msg_type == "info" else messagebox.showwarning if msg_type == "warning" else messagebox.showerror
            fallback_func(title, message)

# --- START THE APPLICATION ---
if __name__ == "__main__":
    # --- 1. SETUP THE AI (This part is not in the class) ---
    print("App starting...")
    # Global model variables - needed outside the class initially? No. Let's rely on class loading.
    # print("Model ready. Starting GUI...") # Move this after successful load

    app = App()
    app.mainloop()
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
BG_COLOR = "#000000"
MENU_COLOR = "#1C1C1C"
ENTRY_COLOR = "#1C1C1C"
TEXT_COLOR = "#FFFFFF"
BTN_COLOR = "#FFFFFF"
BTN_TEXT_COLOR = "#000000"
BTN_HOVER_COLOR = "#E0E0E0"
ICON_HOVER_COLOR = "#333333"
DOWNLOAD_BTN_COLOR = "#4CAF50" # Green for download
DOWNLOAD_BTN_HOVER = "#66BB6A"

# --- MAIN APPLICATION CLASS ---
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Corrector v2.1")
        self.geometry("1100x600")
        self.configure(fg_color=BG_COLOR)
        ctk.set_appearance_mode("dark")

        # --- AI Model State ---
        self.current_lang_code = None
        self.model = None
        self.tokenizer = None
        self.is_loading = False # Flag to prevent multiple loads

        # --- Layout Grids ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Class Variables ---
        self.theme_radio_var = tk.StringVar(value="dark")
        self.language_buttons = {} # To store download buttons
        self.language_progress_bars = {} # To store progress bars
        self.language_status_labels = {} # To store status labels

        # --- Create GUI ---
        self.create_sidebars()
        self.create_pages()
        self.update_language_statuses() # Check initial status

        # --- Show default page ---
        self.show_page("corrector")
        # Attempt to load default model if available
        self.load_selected_model("en_us", initial_load=True)


    # --- GUI Creation Methods ---
    def create_sidebars(self):
        # --- EXPANDED Sidebar ---
        self.sidebar_expanded = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=MENU_COLOR)
        self.sidebar_expanded.grid(row=0, column=0, sticky="nsw")
        self.sidebar_expanded.grid_rowconfigure(5, weight=1) # Spacer

        menu_toggle_btn_exp = ctk.CTkButton(self.sidebar_expanded, text="☰", font=ctk.CTkFont(size=20), width=40, fg_color="transparent", hover_color=ICON_HOVER_COLOR, command=self.toggle_sidebar, anchor="w")
        menu_toggle_btn_exp.grid(row=0, column=0, pady=20, padx=20, sticky="w")
        title_label = ctk.CTkLabel(self.sidebar_expanded, text="AI Corrector", font=ctk.CTkFont(size=22, weight="bold"), anchor="w")
        title_label.grid(row=1, column=0, pady=(0, 20), padx=20, sticky="w")
        self.corrector_btn_exp = ctk.CTkButton(self.sidebar_expanded, text="✎  Corrector", font=ctk.CTkFont(size=14, weight="bold"), anchor="w", corner_radius=8, command=lambda: self.show_page("corrector"))
        self.corrector_btn_exp.grid(row=2, column=0, pady=5, padx=20, sticky="ew")
        self.about_btn_exp = ctk.CTkButton(self.sidebar_expanded, text="ⓘ  About Us", font=ctk.CTkFont(size=14, weight="bold"), anchor="w", fg_color="transparent", text_color=TEXT_COLOR, corner_radius=8, command=lambda: self.show_page("about"))
        self.about_btn_exp.grid(row=3, column=0, pady=5, padx=20, sticky="ew")
        self.settings_btn_exp = ctk.CTkButton(self.sidebar_expanded, text="⚙  Settings", font=ctk.CTkFont(size=14, weight="bold"), anchor="w", fg_color="transparent", text_color=TEXT_COLOR, corner_radius=8, command=lambda: self.show_page("settings"))
        self.settings_btn_exp.grid(row=6, column=0, pady=20, padx=20, sticky="s")

        # --- COLLAPSED Sidebar ---
        self.sidebar_collapsed = ctk.CTkFrame(self, width=70, corner_radius=0, fg_color=MENU_COLOR)
        self.sidebar_collapsed.grid(row=0, column=0, sticky="nsw")
        self.sidebar_collapsed.grid_rowconfigure(1, weight=1) # Spacer
        menu_toggle_btn_col = ctk.CTkButton(self.sidebar_collapsed, text="☰", font=ctk.CTkFont(size=20), width=40, fg_color="transparent", hover_color=ICON_HOVER_COLOR, command=self.toggle_sidebar, anchor="center")
        menu_toggle_btn_col.grid(row=0, column=0, pady=20, padx=15, sticky="w")
        self.settings_btn_col = ctk.CTkButton(self.sidebar_collapsed, text="⚙", font=ctk.CTkFont(size=20), width=40, fg_color="transparent", text_color=TEXT_COLOR, corner_radius=8, hover_color=ICON_HOVER_COLOR, command=lambda: [self.toggle_sidebar(), self.show_page("settings")])
        self.settings_btn_col.grid(row=2, column=0, pady=20, padx=15, sticky="s")
        self.sidebar_collapsed.grid_forget() # Hide it initially

    def create_pages(self):
        # --- Page 1: Corrector ---
        self.corrector_page_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=BG_COLOR)
        self.corrector_page_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.corrector_page_frame.grid_columnconfigure((0, 2), weight=1)
        self.corrector_page_frame.grid_columnconfigure(1, weight=0)
        self.corrector_page_frame.grid_rowconfigure(2, weight=1) # Textboxes row

        # Language Indicator (Top Left)
        self.lang_indicator_label = ctk.CTkLabel(self.corrector_page_frame, text="Model: [None Loaded]", font=ctk.CTkFont(size=12), text_color="#AAAAAA")
        self.lang_indicator_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

        ctk.CTkLabel(self.corrector_page_frame, text="Input Text:", font=ctk.CTkFont(size=14)).grid(row=1, column=0, sticky="w", pady=(0, 5))
        self.corrector_input_textbox = ctk.CTkTextbox(self.corrector_page_frame, corner_radius=10, fg_color=ENTRY_COLOR, text_color=TEXT_COLOR, font=ctk.CTkFont(size=13))
        self.corrector_input_textbox.grid(row=2, column=0, sticky="nsew", padx=(0, 10))

        middle_button_frame = ctk.CTkFrame(self.corrector_page_frame, fg_color=BG_COLOR)
        middle_button_frame.grid(row=2, column=1, sticky="ns", padx=5)
        self.corrector_button_middle = ctk.CTkButton(middle_button_frame, text=">>", width=50, font=ctk.CTkFont(size=16, weight="bold"), fg_color=BTN_COLOR, text_color=BTN_TEXT_COLOR, hover_color=BTN_HOVER_COLOR, corner_radius=8, command=self.on_correct_click, state="disabled") # Disabled initially
        self.corrector_button_middle.pack(expand=True)

        ctk.CTkLabel(self.corrector_page_frame, text="Corrected Text:", font=ctk.CTkFont(size=14)).grid(row=1, column=2, sticky="w", pady=(0, 5))
        self.corrector_output_textbox = ctk.CTkTextbox(self.corrector_page_frame, corner_radius=10, fg_color=ENTRY_COLOR, text_color=TEXT_COLOR, font=ctk.CTkFont(size=13), state="disabled")
        self.corrector_output_textbox.grid(row=2, column=2, sticky="nsew", padx=(10, 0))

        # --- Page 2: About Us ---
        self.about_page_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=BG_COLOR)
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
        self.settings_page_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=BG_COLOR)
        self.settings_page_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        ctk.CTkLabel(self.settings_page_frame, text="Settings", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20, anchor="w")

        # --- Appearance Settings ---
        appearance_frame = ctk.CTkFrame(self.settings_page_frame, fg_color=ENTRY_COLOR, corner_radius=10)
        appearance_frame.pack(fill="x", padx=20, pady=10, anchor="w")
        ctk.CTkLabel(appearance_frame, text="Appearance Mode", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5), padx=20, anchor="w")
        radio_light = ctk.CTkRadioButton(appearance_frame, text="Light Mode", variable=self.theme_radio_var, value="light", command=self.change_theme)
        radio_light.pack(pady=5, padx=20, anchor="w")
        radio_dark = ctk.CTkRadioButton(appearance_frame, text="Dark Mode", variable=self.theme_radio_var, value="dark", command=self.change_theme)
        radio_dark.pack(pady=5, padx=20, anchor="w")
        radio_system = ctk.CTkRadioButton(appearance_frame, text="Adapt to Device (System)", variable=self.theme_radio_var, value="system", command=self.change_theme)
        radio_system.pack(pady=(5, 10), padx=20, anchor="w")

        # --- Language Model Settings ---
        language_frame = ctk.CTkFrame(self.settings_page_frame, fg_color=ENTRY_COLOR, corner_radius=10)
        language_frame.pack(fill="x", padx=20, pady=10, anchor="w")
        ctk.CTkLabel(language_frame, text="Language Models", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 15), padx=20, anchor="w")

        for i, (lang_code, details) in enumerate(SUPPORTED_MODELS.items()):
            model_frame = ctk.CTkFrame(language_frame, fg_color="transparent")
            model_frame.pack(fill="x", padx=20, pady=5)
            model_frame.grid_columnconfigure(1, weight=1) # Label expands

            lang_radio = ctk.CTkRadioButton(
                model_frame, text=details["name"], width=200,
                value=lang_code,
                command=lambda lc=lang_code: self.load_selected_model(lc)
            )
            lang_radio.grid(row=0, column=0, sticky="w")

            self.language_status_labels[lang_code] = ctk.CTkLabel(model_frame, text="Status: Unknown", font=ctk.CTkFont(size=12), text_color="#AAAAAA")
            self.language_status_labels[lang_code].grid(row=0, column=1, sticky="w", padx=10)

            self.language_progress_bars[lang_code] = ctk.CTkProgressBar(model_frame, width=150)
            self.language_progress_bars[lang_code].set(0) # Start hidden/empty
            # self.language_progress_bars[lang_code].grid(row=0, column=2, sticky="e", padx=5) # Grid later if needed

            if details["hf_id"]: # Only show download if model exists
                self.language_buttons[lang_code] = ctk.CTkButton(
                    model_frame, text="⬇️", width=40,
                    fg_color=DOWNLOAD_BTN_COLOR, hover_color=DOWNLOAD_BTN_HOVER,
                    font=ctk.CTkFont(size=16),
                    command=lambda lc=lang_code: self.start_download_thread(lc)
                )
                self.language_buttons[lang_code].grid(row=0, column=3, sticky="e")
            else:
                 ctk.CTkLabel(model_frame, text="(Coming Soon)", font=ctk.CTkFont(size=12, slant="italic"), text_color="#AAAAAA").grid(row=0, column=3, sticky="e", padx=10)


        self.settings_page_frame.grid_forget() # Hide it initially

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
        # Reset button styles
        self.corrector_btn_exp.configure(fg_color="transparent", text_color=TEXT_COLOR)
        self.about_btn_exp.configure(fg_color="transparent", text_color=TEXT_COLOR)
        self.settings_btn_exp.configure(fg_color="transparent", text_color=TEXT_COLOR)
        # Show selected page and highlight button
        if page_name == "corrector":
            self.corrector_page_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            self.corrector_btn_exp.configure(fg_color=BTN_COLOR, text_color=BTN_TEXT_COLOR)
        elif page_name == "about":
            self.about_page_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            self.about_btn_exp.configure(fg_color=BTN_COLOR, text_color=BTN_TEXT_COLOR)
        elif page_name == "settings":
            self.settings_page_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            self.settings_btn_exp.configure(fg_color=BTN_COLOR, text_color=BTN_TEXT_COLOR)

    def change_theme(self):
        mode = self.theme_radio_var.get()
        ctk.set_appearance_mode(mode)
        print(f"Appearance mode changed to: {mode}")

    # --- Language Model Handling ---

    def update_language_statuses(self):
        """ Checks download status for all models and updates the GUI. """
        for lang_code, details in SUPPORTED_MODELS.items():
            status_label = self.language_status_labels.get(lang_code)
            download_button = self.language_buttons.get(lang_code)
            
            if not status_label: continue # Skip if GUI not fully ready

            if details["hf_id"] is None:
                 status_label.configure(text="Status: Not Available")
                 if download_button: download_button.grid_forget()
                 continue

            if check_if_model_downloaded(lang_code):
                status_label.configure(text="Status: Downloaded", text_color="lightgreen")
                if download_button: download_button.grid_forget() # Hide download button
            else:
                status_label.configure(text="Status: Not Downloaded", text_color="#AAAAAA")
                if download_button: download_button.grid(row=0, column=3, sticky="e") # Show download button

    def start_download_thread(self, lang_code):
        """ Starts downloading a model in a background thread. """
        if self.is_loading:
            messagebox.showwarning("Busy", "Another operation is already in progress.")
            return
            
        btn = self.language_buttons.get(lang_code)
        prog_bar = self.language_progress_bars.get(lang_code)
        status_label = self.language_status_labels.get(lang_code)

        if btn: btn.configure(state="disabled", text="...")
        if prog_bar:
            prog_bar.grid(row=0, column=2, sticky="e", padx=5) # Show progress bar
            prog_bar.set(0)
        if status_label: status_label.configure(text="Status: Downloading...", text_color="yellow")

        self.is_loading = True
        download_thread = threading.Thread(
            target=self.download_model_thread,
            args=(lang_code,),
            daemon=True
        )
        download_thread.start()

    def download_model_thread(self, lang_code):
        """ --- RUNS IN BACKGROUND THREAD --- """
        print(f"[Thread] Starting download for {lang_code}...")
        
        # Define the callback function for progress updates
        def progress_update(message, percentage):
            # Use 'after' to safely update GUI from this thread
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
        if btn: btn.configure(state="normal", text="⬇️") # Re-enable if failed
        
        self.update_language_statuses() # Refresh status labels/buttons

        if success:
            messagebox.showinfo("Download Complete", f"Model for {SUPPORTED_MODELS[lang_code]['name']} downloaded successfully.")
        else:
            messagebox.showerror("Download Failed", f"Could not download model for {SUPPORTED_MODELS[lang_code]['name']}. Check console for errors.")

    def load_selected_model(self, lang_code, initial_load=False):
        """ Attempts to load the model for the selected language. """
        if self.is_loading:
             if not initial_load: messagebox.showwarning("Busy", "Please wait for the current operation to finish.")
             return
             
        if not check_if_model_downloaded(lang_code):
            if not initial_load: messagebox.showerror("Error", f"Model for {SUPPORTED_MODELS[lang_code]['name']} is not downloaded. Please download it from Settings.")
            self.update_corrector_status(f"Model: [{SUPPORTED_MODELS[lang_code]['name']} - Not Downloaded]", error=True)
            self.model = None # Unload any previous model
            self.tokenizer = None
            self.current_lang_code = None
            return

        if self.current_lang_code == lang_code:
            print(f"Model for {lang_code} already loaded.")
            return # Avoid reloading the same model

        self.is_loading = True
        self.update_corrector_status(f"Loading Model: [{SUPPORTED_MODELS[lang_code]['name']}]...", loading=True)

        # Load in background to prevent freezing
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
             messagebox.showinfo("Model Loaded", f"{SUPPORTED_MODELS[lang_code]['name']} model loaded successfully.")
         else:
             self.update_corrector_status(f"Error loading model: [{SUPPORTED_MODELS[lang_code]['name']}]", error=True)
             self.model = None
             self.tokenizer = None
             self.current_lang_code = None
             messagebox.showerror("Load Failed", f"Could not load model for {SUPPORTED_MODELS[lang_code]['name']}. Files might be corrupt.")

    def update_corrector_status(self, message, loading=False, error=False):
        """ Updates the language indicator label and button states. """
        self.lang_indicator_label.configure(text=message)
        if loading or error or not self.model:
            self.corrector_button_middle.configure(state="disabled")
            self.corrector_input_textbox.configure(state="disabled")
            self.lang_indicator_label.configure(text_color="#AAAAAA" if loading else "red" if error else "#AAAAAA")
        else:
            self.corrector_button_middle.configure(state="normal")
            self.corrector_input_textbox.configure(state="normal")
            self.lang_indicator_label.configure(text_color="lightgreen")

    def on_correct_click(self):
        """ Handles the correction button click, including warnings. """
        if not self.model or not self.tokenizer or not self.current_lang_code:
            messagebox.showwarning("No Model Loaded", "Please select and ensure a language model is downloaded and loaded via the Settings page before correcting text.")
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

# --- START THE APPLICATION ---
if __name__ == "__main__":
    app = App()
    app.mainloop()
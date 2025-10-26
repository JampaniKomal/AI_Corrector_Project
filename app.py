import customtkinter as ctk
import tkinter as tk
from correct import initialize_model, correct_grammar
from spellchecker import SpellChecker

# --- 1. SETUP THE AI (Run once at the start) ---
print("App started. Loading AI model...")
model, tokenizer = initialize_model()
print("Model ready. Starting GUI...")

# --- 2. THEME DEFINITIONS ---
BG_COLOR = "#000000"
MENU_COLOR = "#1C1C1C"
ENTRY_COLOR = "#1C1C1C"
TEXT_COLOR = "#FFFFFF"
BTN_COLOR = "#FFFFFF"
BTN_TEXT_COLOR = "#000000"
BTN_HOVER_COLOR = "#E0E0E0"
ICON_HOVER_COLOR = "#333333"

# --- 3. THE MAIN APPLICATION CLASS ---
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Basic App Setup ---
        self.title("AI Corrector v2.0")
        self.geometry("1100x600")
        self.configure(fg_color=BG_COLOR)
        ctk.set_appearance_mode("dark")

        # --- Layout Grids ---
        self.grid_columnconfigure(1, weight=1) # Main content area
        self.grid_rowconfigure(0, weight=1)    # Main content area

        # --- Class Variables ---
        # We need to store the theme choice
        self.theme_radio_var = tk.StringVar(value="dark")
        
        # --- Create all the GUI components ---
        self.create_sidebars()
        self.create_pages()

        # --- Show the default page ---
        self.show_page("corrector")

    def create_sidebars(self):
        # --- EXPANDED Sidebar (Visible by default) ---
        self.sidebar_expanded = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=MENU_COLOR)
        self.sidebar_expanded.grid(row=0, column=0, sticky="nsw")
        self.sidebar_expanded.grid_rowconfigure(6, weight=1) # Spacer row

        # Toggle Button (Top)
        menu_toggle_btn_exp = ctk.CTkButton(
            self.sidebar_expanded, text="☰", font=ctk.CTkFont(size=20),
            width=40, fg_color="transparent", hover_color=ICON_HOVER_COLOR,
            command=self.toggle_sidebar, anchor="w"
        )
        menu_toggle_btn_exp.grid(row=0, column=0, pady=20, padx=20, sticky="w")

        # Title
        title_label = ctk.CTkLabel(
            self.sidebar_expanded, text="AI Corrector",
            font=ctk.CTkFont(size=22, weight="bold"), anchor="w"
        )
        title_label.grid(row=1, column=0, pady=(0, 20), padx=20, sticky="w")

        # Corrector Nav Button
        self.corrector_btn_exp = ctk.CTkButton(
            self.sidebar_expanded, text="✎  Corrector", font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w", corner_radius=8, command=lambda: self.show_page("corrector")
        )
        self.corrector_btn_exp.grid(row=2, column=0, pady=5, padx=20, sticky="ew")

        # About Nav Button
        self.about_btn_exp = ctk.CTkButton(
            self.sidebar_expanded, text="ⓘ  About Us", font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w", fg_color="transparent", text_color=TEXT_COLOR,
            corner_radius=8, command=lambda: self.show_page("about")
        )
        self.about_btn_exp.grid(row=3, column=0, pady=5, padx=20, sticky="ew")

        # Language Label and Dropdown
        lang_label = ctk.CTkLabel(
            self.sidebar_expanded, text="🌐  Language",
            font=ctk.CTkFont(size=14, weight="bold"), anchor="w"
        )
        lang_label.grid(row=4, column=0, pady=(20, 5), padx=20, sticky="w")
        
        self.lang_menu = ctk.CTkOptionMenu(
            self.sidebar_expanded,
            values=["English (US/Global)", "English (UK) - (Future)", "English (IN) - (Future)"],
            fg_color=ENTRY_COLOR, text_color=TEXT_COLOR, button_color=ENTRY_COLOR
        )
        self.lang_menu.grid(row=5, column=0, pady=5, padx=20, sticky="ew")

        # Settings Nav Button (Bottom)
        self.settings_btn_exp = ctk.CTkButton(
            self.sidebar_expanded, text="⚙  Settings", font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w", fg_color="transparent", text_color=TEXT_COLOR,
            corner_radius=8, command=lambda: self.show_page("settings")
        )
        self.settings_btn_exp.grid(row=7, column=0, pady=20, padx=20, sticky="s")

        # --- COLLAPSED Sidebar (Hidden by default) ---
        self.sidebar_collapsed = ctk.CTkFrame(self, width=70, corner_radius=0, fg_color=MENU_COLOR)
        self.sidebar_collapsed.grid(row=0, column=0, sticky="nsw")
        self.sidebar_collapsed.grid_rowconfigure(1, weight=1) # Spacer
        self.sidebar_collapsed.grid_forget() # Hide it

        # Toggle Button (Top)
        menu_toggle_btn_col = ctk.CTkButton(
            self.sidebar_collapsed, text="☰", font=ctk.CTkFont(size=20),
            width=40, fg_color="transparent", hover_color=ICON_HOVER_COLOR,
            command=self.toggle_sidebar, anchor="center"
        )
        menu_toggle_btn_col.grid(row=0, column=0, pady=20, padx=15, sticky="w")

        # Settings Nav Button (Bottom)
        self.settings_btn_col = ctk.CTkButton(
            self.sidebar_collapsed, text="⚙", font=ctk.CTkFont(size=20),
            width=40, fg_color="transparent", text_color=TEXT_COLOR,
            corner_radius=8, hover_color=ICON_HOVER_COLOR,
            # This command is smart: it expands the menu AND shows the settings page
            command=lambda: [self.toggle_sidebar(), self.show_page("settings")]
        )
        self.settings_btn_col.grid(row=2, column=0, pady=20, padx=15, sticky="s")
    
    def create_pages(self):
        # --- Page 1: Corrector ---
        self.corrector_page_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=BG_COLOR)
        self.corrector_page_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.corrector_page_frame.grid_columnconfigure((0, 2), weight=1)
        self.corrector_page_frame.grid_columnconfigure(1, weight=0)
        self.corrector_page_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self.corrector_page_frame, text="Input Text:", font=ctk.CTkFont(size=14)).grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.corrector_input_textbox = ctk.CTkTextbox(self.corrector_page_frame, corner_radius=10, fg_color=ENTRY_COLOR, text_color=TEXT_COLOR, font=ctk.CTkFont(size=13))
        self.corrector_input_textbox.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        middle_button_frame = ctk.CTkFrame(self.corrector_page_frame, fg_color=BG_COLOR)
        middle_button_frame.grid(row=1, column=1, sticky="ns", padx=5)
        self.corrector_button_middle = ctk.CTkButton(
            middle_button_frame, text=">>", width=50, font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=BTN_COLOR, text_color=BTN_TEXT_COLOR, hover_color=BTN_HOVER_COLOR,
            corner_radius=8, command=self.on_correct_click
        )
        self.corrector_button_middle.pack(expand=True)

        ctk.CTkLabel(self.corrector_page_frame, text="Corrected Text:", font=ctk.CTkFont(size=14)).grid(row=0, column=2, sticky="w", pady=(0, 5))
        self.corrector_output_textbox = ctk.CTkTextbox(self.corrector_page_frame, corner_radius=10, fg_color=ENTRY_COLOR, text_color=TEXT_COLOR, font=ctk.CTkFont(size=13))
        self.corrector_output_textbox.grid(row=1, column=2, sticky="nsew", padx=(10, 0))
        self.corrector_output_textbox.configure(state="disabled")

        # --- Page 2: About Us ---
        self.about_page_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=BG_COLOR)
        self.about_page_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        ctk.CTkLabel(self.about_page_frame, text="About This Project", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        about_text = ("Project: AI Contextual Corrector\n"
                      "Course: Artificial Intelligence (G5AD24ARI)\n"
                      "University: Rashtriya Raksha University\n\n"
                      "Team Members:\n"
                      "- Jampani Komal\n- [Team Member 2 Name]\n- [Team Member 3 Name]\n\n"
                      "This application uses a pre-trained T5 Transformer model to provide\n"
                      "deep contextual and grammatical corrections.")
        ctk.CTkLabel(self.about_page_frame, text=about_text, font=ctk.CTkFont(size=14), justify="left").pack(pady=10, padx=20, fill="x")
        self.about_page_frame.grid_forget() # Hide it

        # --- Page 3: Settings ---
        self.settings_page_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=BG_COLOR)
        self.settings_page_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        ctk.CTkLabel(self.settings_page_frame, text="Settings", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20, anchor="w")
        
        appearance_frame = ctk.CTkFrame(self.settings_page_frame, fg_color=ENTRY_COLOR, corner_radius=10)
        appearance_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(appearance_frame, text="Appearance Mode", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5), padx=20, anchor="w")
        
        radio_light = ctk.CTkRadioButton(
            appearance_frame, text="Light Mode", variable=self.theme_radio_var,
            value="light", command=self.change_theme
        )
        radio_light.pack(pady=5, padx=20, anchor="w")
        
        radio_dark = ctk.CTkRadioButton(
            appearance_frame, text="Dark Mode", variable=self.theme_radio_var,
            value="dark", command=self.change_theme
        )
        radio_dark.pack(pady=5, padx=20, anchor="w")
        
        radio_system = ctk.CTkRadioButton(
            appearance_frame, text="Adapt to Device (System)", variable=self.theme_radio_var,
            value="system", command=self.change_theme
        )
        radio_system.pack(pady=(5, 10), padx=20, anchor="w")
        
        self.settings_page_frame.grid_forget() # Hide it

    # --- 4. CORE APP FUNCTIONS ---

    def toggle_sidebar(self):
        """ Swaps the expanded and collapsed sidebars. """
        if self.sidebar_expanded.winfo_viewable():
            self.sidebar_expanded.grid_forget()
            self.sidebar_collapsed.grid(row=0, column=0, sticky="nsw")
        else:
            self.sidebar_collapsed.grid_forget()
            self.sidebar_expanded.grid(row=0, column=0, sticky="nsw")

    def show_page(self, page_name):
        """ Hides all pages and shows the selected one. """
        # Hide all pages
        self.corrector_page_frame.grid_forget()
        self.about_page_frame.grid_forget()
        self.settings_page_frame.grid_forget()
        
        # Reset all button styles
        self.corrector_btn_exp.configure(fg_color="transparent", text_color=TEXT_COLOR)
        self.about_btn_exp.configure(fg_color="transparent", text_color=TEXT_COLOR)
        self.settings_btn_exp.configure(fg_color="transparent", text_color=TEXT_COLOR)
        
        # Show the selected page and highlight the correct button
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
        """ Called by the radio buttons to change the app's theme. """
        mode = self.theme_radio_var.get()
        ctk.set_appearance_mode(mode)
        print(f"Appearance mode changed to: {mode}")

    def on_correct_click(self):
        """ This function is called when the user clicks the 'Correct' button. """
        input_text = self.corrector_input_textbox.get("1.0", "end-1c")
        if len(input_text.strip()) < 1: return
            
        print(f"Original text: '{input_text.strip()}'")
        self.corrector_button_middle.configure(text="...", state="disabled")
        self.update_idletasks() # Force GUI to update

        # --- NEW HYBRID LOGIC ---

        # 1. STEP A: SPELL CHECK
        # We create a SpellChecker object for English
        spell = SpellChecker()
        
        # Split the input into individual words
        words = input_text.split()
        
        # Find all the misspelled words
        misspelled = spell.unknown(words)
        
        # Correct each misspelled word
        corrected_words = []
        for word in words:
            if word in misspelled:
                # Get the one, most-likely correction
                corrected_word = spell.correction(word)
                if corrected_word: # Make sure a correction was found
                    corrected_words.append(corrected_word)
                else:
                    corrected_words.append(word) # Keep original if no correction
            else:
                corrected_words.append(word)
        
        # Join the corrected words back into a sentence
        spell_checked_text = " ".join(corrected_words)
        print(f"Spell-checked text: '{spell_checked_text}'")

        # 2. STEP B: GRAMMAR CHECK (using the T5 Model)
        # We now feed the *spell-checked* text to the grammar AI
        corrected_text = correct_grammar(spell_checked_text, model, tokenizer)
        
        # --- END OF NEW LOGIC ---
        
        self.corrector_output_textbox.configure(state="normal")
        self.corrector_output_textbox.delete("1.0", tk.END)
        self.corrector_output_textbox.insert("1.0", corrected_text)
        self.corrector_output_textbox.configure(state="disabled")
        self.corrector_button_middle.configure(text=">>", state="normal")
        
# --- 5. START THE APPLICATION ---
if __name__ == "__main__":
    app = App()
    app.mainloop()
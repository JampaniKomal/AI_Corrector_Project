import customtkinter as ctk
import tkinter as tk
from correct import initialize_model, correct_grammar

# --- 1. SETUP THE AI (Same as before) ---
print("App started. Loading AI model...")
model, tokenizer = initialize_model()
print("Model ready. Starting GUI...")

# --- 2. THEME & APP SETUP ---
ctk.set_appearance_mode("dark") 

# Define our custom B&W theme colors
BG_COLOR = "#000000"
MENU_COLOR = "#1C1C1C"
ENTRY_COLOR = "#1C1C1C"
TEXT_COLOR = "#FFFFFF"
BTN_COLOR = "#FFFFFF"
BTN_TEXT_COLOR = "#000000"
BTN_HOVER_COLOR = "#E0E0E0"

# --- 3. CORE APP LOGIC ---

def on_correct_button_click():
    """ This function is called when the user clicks the 'Correct' button. """
    input_text = corrector_input_textbox.get("1.0", "end-1c")
    
    if len(input_text.strip()) < 1:
        return
        
    print(f"Correcting text: '{input_text.strip()}'")
    
    corrector_button_middle.configure(text="...", state="disabled")
    root.update_idletasks()
    
    corrected_text = correct_grammar(input_text, model, tokenizer)
    
    corrector_output_textbox.configure(state="normal")
    corrector_output_textbox.delete("1.0", tk.END)
    corrector_output_textbox.insert("1.0", corrected_text)
    corrector_output_textbox.configure(state="disabled")
    
    corrector_button_middle.configure(text=">>", state="normal")

def toggle_sidebar():
    """ Expands or collapses the side menu. """
    if side_menu_frame.winfo_width() > 100: # If it's expanded
        # Collapse
        side_menu_frame.grid_configure(sticky="ns") # Stop sticking to west
        
        # Hide text, show icons
        title_label.grid_forget()
        corrector_nav_btn.configure(text="", image=nav_icon_corrector, anchor="center")
        about_nav_btn.configure(text="", image=nav_icon_about, anchor="center")
        settings_nav_btn.configure(text="", image=nav_icon_settings, anchor="center")
        menu_toggle_btn.configure(text="☰") # Show "expand" icon
    else:
        # Expand
        side_menu_frame.grid_configure(sticky="nsw") # Stick to west
        
        # Show text, hide icons
        title_label.grid(row=1, column=0, pady=(20, 10), padx=20)
        corrector_nav_btn.configure(text="Corrector", image=None, anchor="w")
        about_nav_btn.configure(text="About Us", image=None, anchor="w")
        settings_nav_btn.configure(text="Settings", image=None, anchor="w")
        menu_toggle_btn.configure(text="<") # Show "collapse" icon

def show_page_corrector():
    """ Shows the corrector page and hides others. """
    corrector_page_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
    about_page_frame.grid_forget()
    
    # Update button visual state
    corrector_nav_btn.configure(fg_color=BTN_COLOR, text_color=BTN_TEXT_COLOR)
    about_nav_btn.configure(fg_color="transparent", text_color=TEXT_COLOR)

def show_page_about():
    """ Shows the 'About Us' page and hides others. """
    corrector_page_frame.grid_forget()
    about_page_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
    
    # Update button visual state
    corrector_nav_btn.configure(fg_color="transparent", text_color=TEXT_COLOR)
    about_nav_btn.configure(fg_color=BTN_COLOR, text_color=BTN_TEXT_COLOR)

# --- 4. CREATE THE MAIN WINDOW ---
root = ctk.CTk()
root.title("AI Corrector v1.1")
root.geometry("1100x600")
root.configure(fg_color=BG_COLOR)

# --- 5. CREATE LAYOUT GRIDS ---
# Configure the main window grid
root.grid_columnconfigure(1, weight=1) # Main content area expands
root.grid_rowconfigure(0, weight=1)    # Main content area expands

# --- 6. CREATE SIDE MENU ---
# We need placeholder images for the icons.
# CTk doesn't have built-in icons, so we create simple ones.
nav_icon_corrector = ctk.CTkImage(light_image=None, dark_image=None, size=(20, 20)) # Placeholder
nav_icon_about = ctk.CTkImage(light_image=None, dark_image=None, size=(20, 20))     # Placeholder
nav_icon_settings = ctk.CTkImage(light_image=None, dark_image=None, size=(20, 20))  # Placeholder

side_menu_frame = ctk.CTkFrame(
    root,
    width=250,
    corner_radius=0,
    fg_color=MENU_COLOR
)
side_menu_frame.grid(row=0, column=0, sticky="nsw")
side_menu_frame.grid_rowconfigure(4, weight=1) # Push settings to bottom

menu_toggle_btn = ctk.CTkButton(
    side_menu_frame,
    text="<",
    width=40,
    font=ctk.CTkFont(size=18, weight="bold"),
    fg_color="transparent",
    command=toggle_sidebar
)
menu_toggle_btn.grid(row=0, column=0, pady=20, padx=20, sticky="w")

title_label = ctk.CTkLabel(
    side_menu_frame, 
    text="AI Corrector", 
    font=ctk.CTkFont(size=22, weight="bold"),
    anchor="w"
)
title_label.grid(row=1, column=0, pady=(0, 20), padx=20)

corrector_nav_btn = ctk.CTkButton(
    side_menu_frame,
    text="Corrector",
    font=ctk.CTkFont(size=14, weight="bold"),
    anchor="w",
    fg_color=BTN_COLOR, # Active by default
    text_color=BTN_TEXT_COLOR,
    corner_radius=8,
    command=show_page_corrector
)
corrector_nav_btn.grid(row=2, column=0, pady=5, padx=20, sticky="ew")

about_nav_btn = ctk.CTkButton(
    side_menu_frame,
    text="About Us",
    font=ctk.CTkFont(size=14, weight="bold"),
    anchor="w",
    fg_color="transparent",
    text_color=TEXT_COLOR,
    corner_radius=8,
    command=show_page_about
)
about_nav_btn.grid(row=3, column=0, pady=5, padx=20, sticky="ew")

settings_nav_btn = ctk.CTkButton(
    side_menu_frame,
    text="Settings",
    font=ctk.CTkFont(size=14, weight="bold"),
    anchor="w",
    fg_color="transparent",
    text_color="#808080", # Disabled look
    corner_radius=8
)
settings_nav_btn.grid(row=5, column=0, pady=20, padx=20, sticky="s")


# --- 7. CREATE MAIN CONTENT PAGES ---

# --- Page 1: Corrector ---
corrector_page_frame = ctk.CTkFrame(root, corner_radius=0, fg_color=BG_COLOR)
corrector_page_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

# Configure the corrector page grid (Input, Button, Output)
corrector_page_frame.grid_columnconfigure(0, weight=1) # Input
corrector_page_frame.grid_columnconfigure(1, weight=0) # Button (no expand)
corrector_page_frame.grid_columnconfigure(2, weight=1) # Output
corrector_page_frame.grid_rowconfigure(1, weight=1) # Textboxes expand

# Input Label
ctk.CTkLabel(
    corrector_page_frame, 
    text="Input Text:", 
    font=ctk.CTkFont(size=14)
).grid(row=0, column=0, sticky="w", pady=(0, 5))

# Input Textbox
corrector_input_textbox = ctk.CTkTextbox(
    corrector_page_frame,
    corner_radius=10,
    fg_color=ENTRY_COLOR,
    text_color=TEXT_COLOR,
    font=ctk.CTkFont(size=13)
)
corrector_input_textbox.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

# Middle Button Frame
middle_button_frame = ctk.CTkFrame(corrector_page_frame, fg_color=BG_COLOR)
middle_button_frame.grid(row=1, column=1, sticky="ns", padx=5)

corrector_button_middle = ctk.CTkButton(
    middle_button_frame,
    text=">>",
    width=50,
    font=ctk.CTkFont(size=16, weight="bold"),
    fg_color=BTN_COLOR,
    text_color=BTN_TEXT_COLOR,
    hover_color=BTN_HOVER_COLOR,
    corner_radius=8,
    command=on_correct_button_click
)
corrector_button_middle.pack(expand=True) # This centers it vertically

# Output Label
ctk.CTkLabel(
    corrector_page_frame, 
    text="Corrected Text:", 
    font=ctk.CTkFont(size=14)
).grid(row=0, column=2, sticky="w", pady=(0, 5))

# Output Textbox
corrector_output_textbox = ctk.CTkTextbox(
    corrector_page_frame,
    corner_radius=10,
    fg_color=ENTRY_COLOR,
    text_color=TEXT_COLOR,
    font=ctk.CTkFont(size=13)
)
corrector_output_textbox.grid(row=1, column=2, sticky="nsew", padx=(10, 0))
corrector_output_textbox.configure(state="disabled")

# --- Page 2: About Us ---
about_page_frame = ctk.CTkFrame(root, corner_radius=0, fg_color=BG_GOLOR)
# We configure its grid but don't show it yet
about_page_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
about_page_frame.grid_forget() # Hide it

ctk.CTkLabel(
    about_page_frame,
    text="About This Project",
    font=ctk.CTkFont(size=24, weight="bold")
).pack(pady=20)

about_text = """
Project: AI Contextual Corrector
Course: Artificial Intelligence (G5AD24ARI)
University: Rashtriya Raksha University

Team Members:
- Jampani Komal
- [Team Member 2 Name]
- [Team Member 3 Name]

This application uses a pre-trained T5 Transformer model 
to provide deep contextual and grammatical corrections.
"""

ctk.CTkLabel(
    about_page_frame,
    text=about_text,
    font=ctk.CTkFont(size=14),
    justify="left"
).pack(pady=10, padx=20, fill="x")


# --- 8. START THE APPLICATION ---
root.mainloop()
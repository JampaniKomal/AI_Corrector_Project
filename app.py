import customtkinter as ctk  # Import the modern library
import tkinter as tk
from correct import initialize_model, correct_grammar

# --- 1. SETUP THE AI (Same as before) ---
print("App started. Loading AI model...")
model, tokenizer = initialize_model()
print("Model ready. Starting GUI...")

# --- 2. THEME & APP SETUP ---
ctk.set_appearance_mode("dark") # Use a dark base theme

# Define our custom B&W theme colors
BG_COLOR = "#000000"
MENU_COLOR = "#1C1C1C"
ENTRY_COLOR = "#1C1C1C"
TEXT_COLOR = "#FFFFFF"
BTN_COLOR = "#FFFFFF"
BTN_TEXT_COLOR = "#000000"
BTN_HOVER_COLOR = "#E0E0E0"


# --- 3. DEFINE THE CORE APP FUNCTION ---
def on_correct_button_click():
    """
    This function is called when the user clicks the "Correct" button.
    """
    input_text = input_textbox.get("1.0", "end-1c") # Get text from CTkTextbox
    
    if len(input_text.strip()) < 1:
        return
        
    print(f"Correcting text: '{input_text.strip()}'")
    
    # Update button to show "Working..."
    correct_button.configure(text="Correcting...", state="disabled")
    root.update_idletasks() # Force GUI to update
    
    # --- Run the AI ---
    corrected_text = correct_grammar(input_text, model, tokenizer)
    
    # --- Update the GUI ---
    output_textbox.configure(state="normal") # Enable writing
    output_textbox.delete("1.0", tk.END)
    output_textbox.insert("1.0", corrected_text)
    output_textbox.configure(state="disabled") # Disable writing
    
    # Change button back
    correct_button.configure(text="Correct Text", state="normal")

# --- 4. CREATE THE MAIN WINDOW ---
root = ctk.CTk()
root.title("AI Corrector")
root.geometry("1000x600") # Bigger window
root.configure(fg_color=BG_COLOR)

# --- 5. CREATE THE LAYOUT ---
# Configure the main window grid layout
root.grid_columnconfigure(1, weight=1) # Main content area expands
root.grid_rowconfigure(0, weight=1)    # Main content area expands

# --- Side Menu (Left) ---
side_menu_frame = ctk.CTkFrame(
    root,
    width=200,
    corner_radius=0, # Sharp corners for the menu
    fg_color=MENU_COLOR
)
side_menu_frame.grid(row=0, column=0, sticky="nsw") # Stick to North-South-West

# --- Main Content (Right) ---
main_content_frame = ctk.CTkFrame(root, corner_radius=0, fg_color=BG_COLOR)
main_content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
main_content_frame.grid_columnconfigure((0, 1), weight=1) # Let both text boxes expand
main_content_frame.grid_rowconfigure(1, weight=1) # Let text boxes fill height


# --- 6. POPULATE THE SIDE MENU ---
title_label = ctk.CTkLabel(
    side_menu_frame, 
    text="AI Corrector", 
    font=ctk.CTkFont(size=20, weight="bold")
)
title_label.pack(pady=20, padx=20)

# Menu Buttons (using CTkButton for a modern feel)
corrector_button = ctk.CTkButton(
    side_menu_frame,
    text="Corrector",
    fg_color="transparent", # Make it look like a label
    text_color=TEXT_COLOR,  # White text
    font=ctk.CTkFont(size=14, weight="bold"),
    anchor="w" # Align text to the left (west)
)
corrector_button.pack(fill="x", padx=20, pady=5)

settings_button = ctk.CTkButton(
    side_menu_frame,
    text="Settings",
    fg_color="transparent",
    text_color="#808080", # Greyed out
    font=ctk.CTkFont(size=14),
    anchor="w"
)
settings_button.pack(fill="x", padx=20, pady=5)

language_button = ctk.CTkButton(
    side_menu_frame,
    text="Languages (EN-US)",
    fg_color="transparent",
    text_color="#808080",
    font=ctk.CTkFont(size=14),
    anchor="w"
)
language_button.pack(fill="x", padx=20, pady=5)


# --- 7. POPULATE THE MAIN CONTENT ---

# --- Input Side ---
input_label = ctk.CTkLabel(
    main_content_frame, 
    text="Input Text:", 
    font=ctk.CTkFont(size=14)
)
input_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

input_textbox = ctk.CTkTextbox(
    main_content_frame,
    corner_radius=10, # <-- CURVED CORNERS
    fg_color=ENTRY_COLOR,
    text_color=TEXT_COLOR,
    font=ctk.CTkFont(size=13)
)
input_textbox.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

# --- Output Side ---
output_label = ctk.CTkLabel(
    main_content_frame, 
    text="Corrected Text:", 
    font=ctk.CTkFont(size=14)
)
output_label.grid(row=0, column=1, sticky="w", pady=(0, 5))

output_textbox = ctk.CTkTextbox(
    main_content_frame,
    corner_radius=10, # <-- CURVED CORNERS
    fg_color=ENTRY_COLOR,
    text_color=TEXT_COLOR,
    font=ctk.CTkFont(size=13)
)
output_textbox.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
output_textbox.configure(state="disabled")


# --- 8. ADD THE "CORRECT" BUTTON ---
# We'll place it in the bottom right
correct_button = ctk.CTkButton(
    main_content_frame,
    text="Correct Text",
    command=on_correct_button_click,
    font=ctk.CTkFont(size=13, weight="bold"),
    fg_color=BTN_COLOR,
    text_color=BTN_TEXT_COLOR,
    hover_color=BTN_HOVER_COLOR,
    corner_radius=8
)
correct_button.grid(row=2, column=1, sticky="e", pady=(15, 0))


# --- 9. START THE APPLICATION ---
root.mainloop()
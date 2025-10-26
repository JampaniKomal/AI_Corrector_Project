import tkinter as tk
from tkinter import scrolledtext, font

# --- Import our AI functions ---
# We keep this part exactly the same.
from correct import initialize_model, correct_grammar

# --- 1. THEME & FONT DEFINITIONS ---
# New Black & White minimalist theme
BG_COLOR = "#000000"     # Black background
FG_COLOR = "#FFFFFF"     # White text
MENU_BG = "#1C1C1C"    # A slightly lighter black for the menu
ENTRY_BG = "#1C1C1C"    # Dark grey for text boxes
BORDER_COLOR = "#FFFFFF" # White border for emphasis

# Define our fonts
TITLE_FONT = ("Helvetica", 18, "bold")
MENU_FONT = ("Helvetica", 11, "bold")
LABEL_FONT = ("Helvetica", 12)
TEXT_FONT = ("Helvetica", 11)


# --- 2. SETUP THE AI (Same as before) ---
print("App started. Loading AI model...")
model, tokenizer = initialize_model()
print("Model ready. Starting GUI...")


# --- 3. DEFINE THE CORE APP FUNCTION ---
def on_correct_button_click():
    """
    This function is called when the user clicks the "Correct" button.
    """
    input_text = input_textbox.get("1.0", tk.END)
    
    if len(input_text.strip()) < 1:
        return
        
    print(f"Correcting text: '{input_text.strip()}'")
    
    # Update button to show "Working..."
    # We will add the button back in a later step.
    # For now, this function just does the AI logic.
    root.update_idletasks() # Force GUI to update
    
    # --- Run the AI ---
    corrected_text = correct_grammar(input_text, model, tokenizer)
    
    # --- Update the GUI ---
    output_textbox.config(state="normal")
    output_textbox.delete("1.0", tk.END)
    output_textbox.insert("1.0", corrected_text)
    output_textbox.config(state="disabled")


# --- 4. CREATE THE MAIN WINDOW ---
root = tk.Tk()
root.title("AI Corrector")
root.geometry("900x500") # Wider to fit horizontal layout
root.configure(bg=BG_COLOR) # Set the main background color

# --- 5. CREATE THE LAYOUT FRAMES ---

# --- Side Menu (Left) ---
side_menu_frame = tk.Frame(root, width=200, bg=MENU_BG)
side_menu_frame.pack(side="left", fill="y") # Pack to the left, fill vertically

# --- Main Content (Right) ---
main_content_frame = tk.Frame(root, bg=BG_COLOR)
main_content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

# --- 6. POPULATE THE SIDE MENU ---

# App Title in the menu
title_label = tk.Label(
    side_menu_frame, 
    text="AI Corrector", 
    font=TITLE_FONT, 
    fg=FG_COLOR, 
    bg=MENU_BG
)
title_label.pack(pady=20, padx=20)

# Menu buttons (as Labels for a flat look)
# These are "placeholders" for your future ideas
corrector_button = tk.Label(
    side_menu_frame, 
    text="> Corrector", 
    font=MENU_FONT, 
    fg=FG_COLOR, 
    bg=MENU_BG
)
corrector_button.pack(pady=10, padx=20, anchor="w")

settings_button = tk.Label(
    side_menu_frame, 
    text="  Settings", 
    font=MENU_FONT, 
    fg="#808080",  # Greyed out to show it's "inactive"
    bg=MENU_BG
)
settings_button.pack(pady=10, padx=20, anchor="w")

language_button = tk.Label(
    side_menu_frame, 
    text="  Languages (EN-US)", 
    font=MENU_FONT, 
    fg="#808080", 
    bg=MENU_BG
)
language_button.pack(pady=10, padx=20, anchor="w")

# --- 7. POPULATE THE MAIN CONTENT ---

# --- Input Frame (Left side of main) ---
input_frame = tk.Frame(main_content_frame, bg=BG_COLOR)
input_frame.pack(side="left", fill="both", expand=True, padx=10)

input_label = tk.Label(
    input_frame, 
    text="Input Text:", 
    font=LABEL_FONT, 
    fg=FG_COLOR, 
    bg=BG_COLOR
)
input_label.pack(anchor="w", pady=(0, 5))

input_textbox = scrolledtext.ScrolledText(
    input_frame, 
    height=20,
    font=TEXT_FONT,
    bg=ENTRY_BG,          # Dark box background
    fg=FG_COLOR,         # White text
    insertbackground=FG_COLOR, # White blinking cursor
    relief="flat",         # No 3D border
    borderwidth=2,         # Thin border
    highlightbackground=BORDER_COLOR, # Border color
    highlightcolor=BORDER_COLOR,
    highlightthickness=1
)
input_textbox.pack(fill="both", expand=True)

# --- Output Frame (Right side of main) ---
output_frame = tk.Frame(main_content_frame, bg=BG_COLOR)
output_frame.pack(side="right", fill="both", expand=True, padx=10)

output_label = tk.Label(
    output_frame, 
    text="Corrected Text:", 
    font=LABEL_FONT, 
    fg=FG_COLOR, 
    bg=BG_COLOR
)
output_label.pack(anchor="w", pady=(0, 5))

output_textbox = scrolledtext.ScrolledText(
    output_frame, 
    height=20,
    font=TEXT_FONT,
    bg=ENTRY_BG,
    fg=FG_COLOR,
    relief="flat",
    borderwidth=2,
    highlightbackground=BORDER_COLOR,
    highlightcolor=BORDER_COLOR,
    highlightthickness=1
)
output_textbox.pack(fill="both", expand=True)
output_textbox.config(state="disabled") # Read-only


# --- 8. ADD THE "CORRECT" BUTTON ---
# We'll place it under the Input box
correct_button = tk.Button(
    input_frame, # Note: We add it to the input_frame
    text="Correct Text", 
    command=on_correct_button_click,
    font=LABEL_FONT,
    bg=FG_COLOR, # White button
    fg=BG_COLOR, # Black text
    activebackground="#808080",
    activeforeground=BG_COLOR,
    relief="flat",
    padx=15,
    pady=5
)
correct_button.pack(pady=10)


# --- 9. START THE APPLICATION ---
root.mainloop()
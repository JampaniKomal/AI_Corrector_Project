import tkinter as tk
from tkinter import scrolledtext, font  # Import 'font' for custom fonts
from correct import initialize_model, correct_grammar

# --- 1. THEME & FONT DEFINITIONS ---
# Your "Buttero Violet" theme colors
BG_COLOR = "#2E1A47"     # Dark violet background
TEXT_COLOR = "#E1D9E9"    # Light lavender text
ENTRY_BG = "#3B2A5E"    # Lighter violet for text boxes
BTN_COLOR = "#E040FB"    # Vibrant magenta button
BTN_TEXT = "#FFFFFF"    # White button text

# Define our fonts
TITLE_FONT = ("Helvetica", 16, "bold")
LABEL_FONT = ("Helvetica", 12)
TEXT_FONT = ("Helvetica", 11)


# --- 2. SETUP THE AI (Same as before) ---
print("App started. Loading AI model...")
model, tokenizer = initialize_model()
print("Model ready. Starting GUI...")


# --- 3. DEFINE THE CORE APP FUNCTION (Same as before) ---
def on_correct_button_click():
    """
    This function is called when the user clicks the "Correct" button.
    """
    input_text = input_textbox.get("1.0", tk.END)
    
    # Simple check so we don't run the AI on empty text
    if len(input_text.strip()) < 1:
        return
        
    print(f"Correcting text: '{input_text.strip()}'")
    
    # Update button to show "Working..."
    correct_button.config(text="Correcting...", state="disabled")
    root.update_idletasks() # Force GUI to update
    
    # --- Run the AI ---
    corrected_text = correct_grammar(input_text, model, tokenizer)
    
    # --- Update the GUI ---
    output_textbox.config(state="normal")
    output_textbox.delete("1.0", tk.END)
    output_textbox.insert("1.0", corrected_text)
    output_textbox.config(state="disabled")
    
    # Change button back
    correct_button.config(text="Correct Text", state="normal")


# --- 4. CREATE THE MAIN WINDOW ---
root = tk.Tk()
root.title("AI Contextual Corrector v1.0")
root.geometry("700x550") # Made the window a bit bigger
root.configure(bg=BG_COLOR) # Set the background color

# --- 5. CREATE THE WIDGETS ---
# We use "Frames" to organize the layout

# --- Title Frame ---
title_frame = tk.Frame(root, bg=BG_COLOR)
title_frame.pack(pady=10)

title_label = tk.Label(title_frame, text="AI Contextual Corrector", font=TITLE_FONT, fg=TEXT_COLOR, bg=BG_COLOR)
title_label.pack()

# --- Input Frame ---
input_frame = tk.Frame(root, bg=BG_COLOR)
input_frame.pack(pady=10, padx=20, fill="x")

input_label = tk.Label(input_frame, text="Enter Your Text Below:", font=LABEL_FONT, fg=TEXT_COLOR, bg=BG_COLOR)
input_label.pack(anchor="w") # "w" = west (left-align)

input_textbox = scrolledtext.ScrolledText(
    input_frame, 
    height=10, 
    width=80,
    font=TEXT_FONT,
    bg=ENTRY_BG,          # Dark box background
    fg=TEXT_COLOR,         # Light text
    insertbackground=TEXT_COLOR # This is the blinking cursor
)
input_textbox.pack(pady=5, fill="x", expand=True)

# --- Button Frame ---
button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.pack(pady=10)

correct_button = tk.Button(
    button_frame, 
    text="Correct Text", 
    command=on_correct_button_click,
    font=LABEL_FONT,
    bg=BTN_COLOR,
    fg=BTN_TEXT,
    activebackground=TEXT_COLOR, # Color when clicked
    activeforeground=BG_COLOR,
    relief="flat",          # Modern flat button
    padx=15,
    pady=5
)
correct_button.pack()

# --- Output Frame ---
output_frame = tk.Frame(root, bg=BG_COLOR)
output_frame.pack(pady=10, padx=20, fill="x")

output_label = tk.Label(output_frame, text="Corrected Text:", font=LABEL_FONT, fg=TEXT_COLOR, bg=BG_COLOR)
output_label.pack(anchor="w")

output_textbox = scrolledtext.ScrolledText(
    output_frame, 
    height=10, 
    width=80,
    font=TEXT_FONT,
    bg=ENTRY_BG,
    fg=TEXT_COLOR
)
output_textbox.pack(pady=5, fill="x", expand=True)
output_textbox.config(state="disabled") # Read-only

# --- 6. START THE APPLICATION ---
root.mainloop()
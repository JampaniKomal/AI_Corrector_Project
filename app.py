# Import the Tkinter library for building GUIs
import tkinter as tk
from tkinter import scrolledtext # This gives us a text box with a scrollbar

# --- Import our AI functions ---
# We are importing the two functions we built in Step 1
from correct import initialize_model, correct_grammar

# --- 1. SETUP THE AI ---
# We do this first, so the model is loaded and ready before
# the user even clicks the button.
print("App started. Loading AI model...")
# We load the model and tokenizer ONCE and store them in global variables
model, tokenizer = initialize_model()
print("Model ready. Starting GUI...")


# --- 2. DEFINE THE CORE APP FUNCTION ---
def on_correct_button_click():
    """
    This function is called when the user clicks the "Correct" button.
    """
    # 1. Get the text from the INPUT box
    input_text = input_textbox.get("1.0", tk.END) # "1.0" means "from line 1, char 0"
    
    # 2. Use our AI function to correct the text
    #    (This is the same function from Step 1)
    corrected_text = correct_grammar(input_text, model, tokenizer)
    
    # 3. Update the OUTPUT box with the corrected text
    output_textbox.config(state="normal") # Enable writing
    output_textbox.delete("1.0", tk.END)  # Clear any old text
    output_textbox.insert("1.0", corrected_text) # Insert the new text
    output_textbox.config(state="disabled") # Disable writing again


# --- 3. CREATE THE MAIN WINDOW ---
root = tk.Tk()
root.title("AI Contextual Corrector")
root.geometry("600x400") # Set the window size

# --- 4. CREATE THE WIDGETS (Text boxes, Buttons, Labels) ---

# --- Input Text Box ---
input_label = tk.Label(root, text="Enter Your Text Below:")
input_label.pack(pady=5) # .pack() places the widget in the window

input_textbox = scrolledtext.ScrolledText(root, height=10, width=70)
input_textbox.pack(pady=5, padx=10)

# --- Correct Button ---
correct_button = tk.Button(root, text="Correct Text", command=on_correct_button_click)
correct_button.pack(pady=10)

# --- Output Text Box ---
output_label = tk.Label(root, text="Corrected Text:")
output_label.pack(pady=5)

output_textbox = scrolledtext.ScrolledText(root, height=10, width=70)
output_textbox.pack(pady=5, padx=10)
output_textbox.config(state="disabled") # Make it read-only

# --- 5. START THE APPLICATION ---
# This line tells Tkinter to open the window and wait for user
# actions (like button clicks).
root.mainloop()

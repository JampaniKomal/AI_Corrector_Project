from transformers import T5ForConditionalGeneration, T5Tokenizer
import sys
import os

# --- NEW HELPER FUNCTION ---
def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller.
    This function is CRITICAL for the .exe to find the model files.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Not running in PyInstaller bundle (i.e., running in dev)
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# --- UPDATED INITIALIZE FUNCTION ---
def initialize_model():
    """
    This function now loads the AI model from our local 'model' folder.
    """
    print("Initializing model from local files...")
    
    # Use our helper function to find the 'model' folder
    model_path = resource_path("model")
    
    try:
        # Load the model's "brain" from the local path
        model = T5ForConditionalGeneration.from_pretrained(model_path)
        
        # Load the "tokenizer" from the local path
        tokenizer = T5Tokenizer.from_pretrained(model_path)
    except Exception as e:
        print(f"---!! ERROR !!----")
        print(f"Could not load model from path: {model_path}")
        print(f"Error: {e}")
        print(f"Make sure you have run 'download_model.py' first.")
        input("Press Enter to exit...")
        sys.exit(1)
        
    print("Model loaded successfully.")
    return model, tokenizer

# --- UNCHANGED FUNCTION ---
def correct_grammar(input_text, model, tokenizer):
    """
    This function takes your bad text and uses the AI model to fix it.
    """
    # The model expects the text to start with "grammar: "
    input_text = f"grammar: {input_text}"
    
    # 1. TOKENIZE: Convert your text into numbers (tokens)
    inputs = tokenizer.encode(input_text, return_tensors='pt', max_length=256, truncation=True)
    
    # 2. GENERATE: Ask the AI model to generate new tokens
    outputs = model.generate(
        inputs,
        max_length=256,
        num_beams=4,
        early_stopping=True
    )
    
    # 3. DECODE: Convert the AI's number tokens back into human-readable text
    corrected_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return corrected_text
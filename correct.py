from transformers import T5ForConditionalGeneration, T5Tokenizer
import os
import sys

# Define the model name and the local directory to save it
MODEL_NAME = 'vennify/t5-base-grammar-correction'
MODEL_DIR = "./model" # We'll save it in a 'model' folder next to the .exe

def check_and_download_model():
    """
    Checks if the model is downloaded. If not, it downloads it.
    This function will be run in a background thread.
    """
    if not os.path.exists(MODEL_DIR):
        print(f"First-time setup: Model not found. Downloading...")
        try:
            # Create the directory
            os.makedirs(MODEL_DIR)
            
            # Download and save the model
            model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)
            model.save_pretrained(MODEL_DIR)
            
            # Download and save the tokenizer
            tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
            tokenizer.save_pretrained(MODEL_DIR)
            
            print("Model download complete.")
            return True
        except Exception as e:
            print(f"---!! ERROR DOWNLOADING MODEL !!----")
            print(f"Error: {e}")
            print("Please check your internet connection and try again.")
            # We would show this error in the GUI
            return False
    else:
        print("Model found in local cache.")
        return True

def load_model_from_disk():
    """
    Loads the model from the local 'model' directory.
    Assumes check_and_download_model() has already run.
    """
    print("Initializing model from local files...")
    try:
        model = T5ForConditionalGeneration.from_pretrained(MODEL_DIR)
        tokenizer = T5Tokenizer.from_pretrained(MODEL_DIR)
        print("Model loaded successfully.")
        return model, tokenizer
    except Exception as e:
        print(f"---!! ERROR LOADING MODEL !!----")
        print(f"Error: {e}")
        print(f"Model files in '{MODEL_DIR}' might be corrupt.")
        return None, None

def correct_grammar(input_text, model, tokenizer):
    """
    This function (unchanged) uses the loaded model to correct text.
    """
    input_text = f"grammar: {input_text}"
    inputs = tokenizer.encode(input_text, return_tensors='pt', max_length=256, truncation=True)
    outputs = model.generate(
        inputs,
        max_length=256,
        num_beams=4,
        early_stopping=True
    )
    corrected_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return corrected_text
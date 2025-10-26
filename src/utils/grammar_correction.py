from transformers import T5ForConditionalGeneration, T5Tokenizer
import os
import sys

# --- Model Definitions ---
# Store details for each language model
SUPPORTED_MODELS = {
    "en_us": {
        "name": "English (US/Global)",
        "hf_id": "vennify/t5-base-grammar-correction",
        "local_dir": "./models/en_us_model" # Unique folder for this model
    },
    "en_uk": {
        "name": "English (UK)",
        "hf_id": "EnglishVoice/t5-base-us-to-uk-english", # This is a TRANSLATOR, not grammar corrector
        "local_dir": "./models/en_uk_model",
        "is_translator": True # Flag this model's type
    },
    "en_in": {
        "name": "English (IN)",
        "hf_id": None, # No specific model available yet
        "local_dir": "./models/en_in_model"
    }
}

# --- Functions ---

def get_model_path(lang_code):
    """ Gets the local directory path for a given language code. """
    if lang_code in SUPPORTED_MODELS:
        return SUPPORTED_MODELS[lang_code]["local_dir"]
    return None

def check_if_model_downloaded(lang_code):
    """ Checks if the model files exist locally for a language. """
    model_dir = get_model_path(lang_code)
    if not model_dir: return False
    # Check if essential files exist
    config_path = os.path.join(model_dir, "config.json")
    model_file_path_bin = os.path.join(model_dir, "pytorch_model.bin")
    model_file_path_safe = os.path.join(model_dir, "model.safetensors") # Newer format
    return os.path.exists(model_dir) and os.path.exists(config_path) and \
           (os.path.exists(model_file_path_bin) or os.path.exists(model_file_path_safe))


def download_model_for_language(lang_code, progress_callback=None):
    """
    Downloads the specified language model from Hugging Face.
    Uses a callback to report progress (optional).
    """
    if lang_code not in SUPPORTED_MODELS or not SUPPORTED_MODELS[lang_code]["hf_id"]:
        print(f"Error: No Hugging Face ID defined for language '{lang_code}'.")
        if progress_callback: progress_callback(f"Error: No model available for {lang_code}", 100)
        return False

    model_details = SUPPORTED_MODELS[lang_code]
    hf_id = model_details["hf_id"]
    local_dir = model_details["local_dir"]

    if check_if_model_downloaded(lang_code):
        print(f"Model for '{lang_code}' already downloaded.")
        if progress_callback: progress_callback("Model already exists.", 100)
        return True

    print(f"Downloading model for '{lang_code}' ({hf_id})...")
    if progress_callback: progress_callback(f"Downloading {lang_code}...", 0)

    try:
        os.makedirs(local_dir, exist_ok=True)
        # Note: Transformers library doesn't have a built-in progress callback for downloads easily accessible here.
        # We simulate progress stages.
        if progress_callback: progress_callback(f"Downloading {lang_code}: Model...", 10)
        model = T5ForConditionalGeneration.from_pretrained(hf_id)
        model.save_pretrained(local_dir)
        if progress_callback: progress_callback(f"Downloading {lang_code}: Tokenizer...", 70)
        tokenizer = T5Tokenizer.from_pretrained(hf_id)
        tokenizer.save_pretrained(local_dir)
        if progress_callback: progress_callback(f"Download complete: {lang_code}", 100)
        print(f"Model download complete for '{lang_code}'.")
        return True
    except Exception as e:
        print(f"---!! ERROR DOWNLOADING MODEL {lang_code} !!----")
        print(f"Error: {e}")
        if progress_callback: progress_callback(f"Error downloading {lang_code}: {e}", 100)
        # Clean up partial download
        if os.path.exists(local_dir):
            import shutil
            shutil.rmtree(local_dir)
        return False


def load_model_from_disk(lang_code):
    """
    Loads the specified language model from its local directory.
    """
    model_dir = get_model_path(lang_code)
    if not model_dir or not check_if_model_downloaded(lang_code):
        print(f"Error: Model for '{lang_code}' not found or incomplete.")
        return None, None

    print(f"Initializing model for '{lang_code}' from {model_dir}...")
    try:
        model = T5ForConditionalGeneration.from_pretrained(model_dir)
        tokenizer = T5Tokenizer.from_pretrained(model_dir)
        print(f"Model loaded successfully for '{lang_code}'.")
        return model, tokenizer
    except Exception as e:
        print(f"---!! ERROR LOADING MODEL {lang_code} !!----")
        print(f"Error: {e}")
        return None, None

def correct_grammar(input_text, model, tokenizer, lang_code):
    """
    Uses the loaded model to correct grammar or translate spelling.
    Handles different prefixes based on model type.
    """
    if not model or not tokenizer:
        print("Error: Model not loaded.")
        return "Error: Model not loaded."

    prefix = "grammar: " # Default for grammar correction
    if SUPPORTED_MODELS.get(lang_code, {}).get("is_translator"):
        prefix = "US to UK: " # Prefix for the UK translator model

    formatted_input = f"{prefix}{input_text}"

    try:
        inputs = tokenizer.encode(formatted_input, return_tensors='pt', max_length=256, truncation=True)
        outputs = model.generate(
            inputs,
            max_length=256,
            num_beams=4,
            early_stopping=True
        )
        corrected_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return corrected_text
    except Exception as e:
        print(f"Error during model generation: {e}")
        return f"Error during correction: {e}"
# Import the AI libraries we need
from transformers import T5ForConditionalGeneration, T5Tokenizer

def initialize_model():
    """
    This function loads the pre-trained AI model and tokenizer from the internet.
    It will download them the first time you run it.
    """
    print("Initializing model... (This may take a moment the first time)")
    
    # This is the name of the pre-trained model we are using
    model_name = 'vennify/t5-base-grammar-correction'
    
    # Load the model's "brain"
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    
    # Load the "tokenizer," which knows how to break text into pieces
    # that the model understands.
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    
    print("Model loaded successfully.")
    return model, tokenizer

def correct_grammar(input_text, model, tokenizer):
    """
    This function takes your bad text and uses the AI model to fix it.
    """
    print(f"Correcting text: '{input_text}'")
    
    # The model expects the text to start with "grammar: "
    input_text = f"grammar: {input_text}"
    
    # 1. TOKENIZE: Convert your text into numbers (tokens)
    inputs = tokenizer.encode(input_text, return_tensors='pt', max_length=256, truncation=True)
    
    # 2. GENERATE: Ask the AI model to generate new tokens
    outputs = model.generate(
        inputs,
        max_length=256,  # Maximum length of the corrected sentence
        num_beams=4,       # Helps the model find a better answer
        early_stopping=True
    )
    
    # 3. DECODE: Convert the AI's number tokens back into human-readable text
    corrected_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return corrected_text

# This special line means "only run the code below if we are
# running this file directly"
if __name__ == "__main__":
    
    # 1. Load the AI model and tokenizer into memory
    model, tokenizer = initialize_model()
    
    # 2. Define the sentence we want to fix
    #    (This includes your "teh" typo AND grammar mistakes)
    bad_text = "He walk to teh store and buyed apples. their going to be good."

    # 3. Call our function to get the corrected text
    good_text = correct_grammar(bad_text, model, tokenizer)
    
    # 4. Print the results!
    print("--- RESULT ---")
    print(f"Original: {bad_text}")
    print(f"Corrected: {good_text}")
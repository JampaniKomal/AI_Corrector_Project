from transformers import T5ForConditionalGeneration, T5Tokenizer

model_name = 'vennify/t5-base-grammar-correction'
model_dir = "./model" # The folder we just created

print(f"Downloading model files for '{model_name}'...")

# Download and save the model
model = T5ForConditionalGeneration.from_pretrained(model_name)
model.save_pretrained(model_dir)

# Download and save the tokenizer
tokenizer = T5Tokenizer.from_pretrained(model_name)
tokenizer.save_pretrained(model_dir)

print(f"All model files saved to the '{model_dir}' folder.")
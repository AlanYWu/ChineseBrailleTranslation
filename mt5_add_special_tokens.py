from transformers import MT5Tokenizer, MT5ForConditionalGeneration
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument(
    "--original_model_dir", help="The path to the original model", required=True
)
parser.add_argument(
    "--output_dir", help="The path to save the new model", required=True
)
args = parser.parse_args()

original_model = args.original_model_dir
# The output_dir is the path that the tokenizer will be saved.
output_dir = args.output_dir


def directory_exists_and_not_empty(path):
    return os.path.exists(path) and os.path.isdir(path) and len(os.listdir(path)) > 0


if not directory_exists_and_not_empty(original_model):
    print(
        f"Directory {original_model} does not exist or is empty. Downloading the model..."
    )

    # Download the model and tokenizer
    model = MT5ForConditionalGeneration.from_pretrained("google/mt5-small")
    tokenizer = MT5Tokenizer.from_pretrained("google/mt5-small")

    # Save the model and tokenizer to the output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)

    print(f"Model and tokenizer saved to {output_dir}")
else:
    print(
        f"Model directory {original_model} exists and is not empty. No action needed."
    )


model = MT5ForConditionalGeneration.from_pretrained(original_model)
tokenizer = MT5Tokenizer.from_pretrained(original_model)

# Add special tokens
new_chars = "⠂⠆⠒⠲⠢⠖⠶⠦⠔⠴⠁⠃⠉⠙⠑⠋⠛⠓⠊⠚⠅⠇⠍⠝⠕⠏⠟⠗⠎⠞⠥⠧⠺⠭⠽⠵⠮⠐⠼⠫⠩⠯⠄⠷⠾⠡⠬⠠⠤⠨⠌⠆⠰⠣⠿⠜⠹⠈⠪⠳⠻⠘⠸"
new_tokens = list(new_chars)
print(len(new_tokens))
print(len(new_chars))
num_added_toks = tokenizer.add_tokens(new_tokens)
print(f"Number of tokens added: {num_added_toks}    ")


example = (
    "⠼⠁ ⠌⠢⠆⠛⠢⠆ ⠼⠉⠙ ⠎⠺⠆ ⠙⠢ ⠙⠔⠆⠇⠡⠂ ⠅⠡⠁⠝⠩⠂⠐ ⠙⠖⠆ ⠓⠩⠆⠵⠪⠆ ⠇⠩⠂ ⠝⠬⠄⠓⠪⠂ ⠙⠢⠱⠷⠄ ⠙⠷⠁ ⠍⠮⠂ ⠇⠔⠁ ⠛⠕⠆ ⠐⠆"
)
print(example)
print(tokenizer.decode(tokenizer(example)["input_ids"]))

# Test the added tokens
text = "⠢⠖⠶ ⠦⠔⠴⠁⠃⠉⠙⠑⠋⠛⠓⠊⠚⠅⠇⠍⠝⠕⠏⠟⠗⠎⠞⠥⠧⠺⠭  ⠽⠵⠮⠐⠼⠫⠯⠄⠷⠾⠾⠡⠬⠠⠤⠨⠌⠆⠰⠣⠿⠜⠹⠈⠪⠳⠻⠘⠸⠲⠒⠆⠂这是视觉盲文-助力教育公平的工具。"
print(text)
encoding = tokenizer.encode(text, max_length=100)
print(encoding)
print(tokenizer.decode(encoding))

from transformers import MT5ForConditionalGeneration

model.resize_token_embeddings(len(tokenizer))


tokenizer.save_pretrained(output_dir)
model.save_pretrained(output_dir)
print("Model and tokenizer saved successfully!")

from torch.utils.data import Dataset
from transformers import T5Tokenizer

# from braille_pre_tokenizer import BraillePreTokenizer
import pandas as pd
from helper_allign_braille_data import translate_braille_numbers
from tqdm import tqdm
import random
import json
import os


class BrailleDataset(Dataset):
    def __init__(
        self,
        input_file="./data/0_combined_braille.txt",
        output_file_name="output_data.txt",
        max_length=512,
    ):

        with open(input_file, "r", encoding="utf-8", errors="replace") as file:
            # Segement the input file into chunks
            chunks = []
            current_chunk = []
            order = []
            for line in file:
                if line.startswith(" "):
                    line = line.strip()
                    if current_chunk:
                        current_chunk_str = " ".join(current_chunk)
                        chunks.append(current_chunk_str)
                        current_chunk = []
                line = line.strip()
                current_chunk.append(line)
            if current_chunk:
                chunks.append(" ".join(current_chunk))

            # Translate the braille numbers to arabic numbers, stored in order
            order = [translate_braille_numbers(line) for line in chunks]
            self.input_df = pd.DataFrame(
                {
                    "order": order,
                    "line": chunks,
                }
            )
            # Remove rows with duplicate 'order' values in the input file
            self.input_df = self.input_df.drop_duplicates("order")

        with open(
            "./data/0_combined_original.txt", "r", encoding="utf-8", errors="replace"
        ) as file:
            self.output_file = file.readlines()
            self.output_df = pd.DataFrame(
                {
                    "order": range(1, len(self.output_file) + 1),
                    "line": self.output_file,
                }
            )
            print("output_file_len:", len(self.output_file))

        # Merge the input and output DataFrames on the order column
        self.aligned_df = pd.merge(
            self.input_df, self.output_df, on="order", suffixes=("_input", "_output")
        )
        self.aligned_df.dropna(inplace=True)
        self.aligned_df = self.aligned_df.drop(columns=["order"])
        assert (
            self.aligned_df.isna().any().any() == False
        ), "There are NaN values in the aligned DataFrame"
        assert len(self.aligned_df) > 0, "The aligned DataFrame is empty"
        print("Number of rows:", len(self.aligned_df))

        self.max_length = max_length

    def remove_tone_in_chunks(self, chunk):
        punctuation_marks = {
            "period": "⠐⠆",
            "question mark": "⠐⠄",
            "exclamation mark": "⠰⠂",
        }
        tones = {
            "first tone": "⠁",
            "second tone": "⠂",
            "third tone": "⠄",
            "fourth tone": "⠆",
        }
        punctuation_characters = set(
            "".join(punctuation_marks.values())
        )  # convert to set for faster lookup

        new_chunk = ""
        i = 0
        while i < len(chunk):
            # Check if the current character is a tone
            if chunk[i] in tones.values():
                # Check if the preceding character is a punctuation mark
                if i > 0 and chunk[i - 1] in punctuation_characters:
                    new_chunk += chunk[i]
            else:
                # If it's not a tone, add it to the new text
                new_chunk += chunk[i]
            i += 1

        return new_chunk

    def remove_tone(self, text):
        text = text.split()
        output = []
        for chunk in text:
            if chunk.startswith("⠼"):
                output.append(chunk)
            else:
                output.append(self.remove_tone_in_chunks(chunk))
        return output

    def create_json(self, output_dir, remove_tone_portion):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        data_for_json = []

        for idx, row in tqdm(self.aligned_df.iterrows()):
            input_text = row["line_input"]

            # Add the a parameter to remove a certion portion of tones.
            if random.random() < remove_tone_portion:
                input_text = self.remove_tone(input_text)
                input_text = " ".join(input_text)
            output_text = row["line_output"]
            data_dict = {"input_text": input_text, "output_text": output_text}
            data_for_json.append(data_dict)

        total_length = len(data_for_json)
        train_end = int(total_length * 0.8)
        validation_end = train_end + int(total_length * 0.1)

        # Split the data into 8:1:1 for training, validation, and testing
        train_data = data_for_json[:train_end]
        validation_data = data_for_json[train_end:validation_end]
        test_data = data_for_json[validation_end:]

        def save_to_json(data, file_name):
            with open(file_name, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        save_to_json(train_data, os.path.join(output_dir, "training_data.json"))
        save_to_json(validation_data, os.path.join(output_dir, "validation_data.json"))
        save_to_json(test_data, os.path.join(output_dir, "testing_data.json"))


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output_dir", default="./data/data-v4", type=str, help="output directory"
    )
    parser.add_argument(
        "--remove_tone_portion",
        default=0.9,
        type=float,
        help="portion of tone that is removed. e.g. 0.1 means 10 percent of the tones are removed, 1 means all tones are removed",
    )
    args = parser.parse_args()

    dataset = BrailleDataset(
        "./data/0_combined_braille.txt", "./data/0_combined_original.txt"
    )
    dataset.create_json(args.output_dir, args.remove_tone_portion)

    print(
        f"json file is created at {os.path.join(args.output_dir, 'training_data_wt_tone.json')}, "
        f"{os.path.join(args.output_dir, 'validation_data_wt_tone.json')}, "
        f"{os.path.join(args.output_dir, 'testing_data_wt_tone.json')}"
    )
    print(
        f"{args.remove_tone_portion*100} percent of tones are removed from the input text"
    )

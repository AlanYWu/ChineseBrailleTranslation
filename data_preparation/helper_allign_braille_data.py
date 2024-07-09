import argparse
import warnings

# Braille to Arabic number mapping
braille_to_arabic = {
    "⠁": "1",
    "⠃": "2",
    "⠉": "3",
    "⠙": "4",
    "⠑": "5",
    "⠋": "6",
    "⠛": "7",
    "⠓": "8",
    "⠊": "9",
    "⠚": "0",
}


def translate_braille_numbers(input_string: str) -> int:
    # Find the first space---> usually that is the sequence number itself.
    space_index = input_string.find(" ")
    if space_index != -1:  # Space found, use the part before the space
        input_string = input_string[:space_index]

    # Initialize an empty string for the Arabic numbers
    arabic_numbers = ""

    # Split the input string into individual Braille numbers
    if input_string.startswith("⠼"):
        input_string = input_string[1:]
        for char in input_string:
            arabic_number = braille_to_arabic.get(char)
            if arabic_number is None:
                warnings.warn(f"Unknown Braille character: {char}")
                return None
            arabic_numbers += arabic_number
    else:
        warnings.warn(f"Input string does not start with '⠼': {input_string}")
        return None

    return eval(arabic_numbers)  # Convert string to integer


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_string",
        default="⠼⠁⠃ ⠓⠪⠄⠛⠻⠁ ⠵⠪⠆ ⠋⠮⠁ ⠎⠕⠄ ⠵⠷⠄⠎⠁",
        help="The input string containing Braille numbers",
    )
    args = parser.parse_args()
    try:
        result = translate_braille_numbers(args.input_string)
        print(result)
    except ValueError as e:
        print(f"Error: {e}")

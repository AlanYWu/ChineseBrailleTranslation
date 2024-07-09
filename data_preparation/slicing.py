def slice_file(input_filename: str, output_filename_base: str, slice_size: int):
    try:
        with open(input_filename, "r", encoding="utf-8") as file:
            file_number = 1
            while True:
                lines = [next(file) for _ in range(slice_size)]
                output_filename = f"{output_filename_base}_{file_number}.txt"
                with open(output_filename, "w", encoding="utf-8") as output_file:
                    output_file.writelines(lines)
                print(f"Saved lines to {output_filename}.")
                file_number += 1
    except StopIteration:
        # End of file reached
        print("End of file reached.")
    except Exception as e:
        # Handle other possible errors
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Slice a file into smaller files.")
    parser.add_argument(
        "--input_filename", type=str, help="The input filename to be sliced."
    )
    parser.add_argument(
        "--output_filename_base", type=str, help="The base of the output filenames."
    )
    parser.add_argument(
        "--slice_size", type=int, help="The number of lines in each slice."
    )
    args = parser.parse_args()

    slice_file(args.input_filename, args.output_filename_base, args.slice_size)

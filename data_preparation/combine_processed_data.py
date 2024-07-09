import os
import argparse

# Check whether the ../data directory exists, if not, create it
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(parent_dir, "data")
if not os.path.exists(data_dir):
    os.makedirs(data_dir)


def combine_output_files(
    braille_path, total_number, naming_format="output_processed_input_{}.txt"
):
    # Generate the expected list of file names
    expected_files = [naming_format.format(i) for i in range(1, total_number + 1)]

    # List all files in the directory
    actual_files = os.listdir(braille_path)

    # Identify missing files
    missing_files = [file for file in expected_files if file not in actual_files]

    # Sort the actual files in numerical order
    sorted_files = sorted(
        actual_files,
        key=lambda x: int(x.replace("output_processed_input_", "").replace(".txt", "")),
    )

    # Combine the files into one
    with open("./data/0_combined_braille.txt", "w", encoding="utf-8") as outfile:
        for filename in sorted_files:
            with open(
                os.path.join(braille_path, filename), "r", encoding="utf-8"
            ) as readfile:
                outfile.write(readfile.read())
    print(
        f"Combined braille data file created: {braille_path+'0_combined_braille.txt'}"
    )
    # Print or use the missing_files list as needed
    print(missing_files)
    return missing_files


def combine_original_data(missing_files, sliced_CN_datadir):
    missing_file_idx = [
        int(file.replace("output_processed_input_", "").replace(".txt", ""))
        for file in missing_files
    ]
    missing_file_idx.sort()

    actual_files = os.listdir(sliced_CN_datadir)
    sorted_files = sorted(
        actual_files,
        key=lambda x: int(x.replace("processed_input_", "").replace(".txt", "")),
    )

    # Combine the files into one, skipping the missing files
    with open("./data/0_combined_original.txt", "w", encoding="utf-8") as outfile:
        for filename in sorted_files:
            if filename not in missing_files:
                with open(
                    os.path.join(sliced_CN_datadir, filename), "r", encoding="utf-8"
                ) as readfile:
                    outfile.write(readfile.read())
    print(f"Combined original data file created: data/0_combined_original.txt")


if __name__ == "__main__":
    """
    This function returns both the combined brialle data and the combined original data.
    The combined data is stored in the ../data

    """
    parser = argparse.ArgumentParser(description="Combine data files.")
    parser.add_argument(
        "--braille_path",
        type=str,
        help="The path to the directory containing the data files.",
    )
    parser.add_argument(
        "--total_number", type=int, help="The total number of files to be combined."
    )
    parser.add_argument(
        "--sliced_CN_datadir", type=str, help="The path to the original data directory."
    )
    args = parser.parse_args()

    missing_files = combine_output_files(args.braille_path, args.total_number)
    combine_original_data(missing_files, args.sliced_CN_datadir)

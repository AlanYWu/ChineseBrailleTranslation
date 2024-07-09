# Braille dataset generation and processing.

## Dataset download
The original dataset used in this research is **zho_news_2007-2009_1M-sentences.txt**, the dataset can be downloaded at [Leipzig Corpora Collection - Wortschatz Deutsch](https://wortschatz.uni-leipzig.de/de/download/Chinese)
You should put the unziped data into `data_preprocessing_scripts/data`


## Processing pipeline
1. Create the necessary folder
    ```bash
    mkdir data
    mkdir sliced_data
    mkdir processed_data
    ```

2. Slided the data into smaller segements, preparing to upload it into the server. 
    ```bash
    python slicing.py \
      --input_filename ./data/zho_news_2007-2009_1M-sentences.txt \
      --output_filename_base sliced_data/processed_input --slice_size 1000
    ```

3. Uploade the data into the server
    ```bash
    python braille_convert.py --data_dir ./sliced_data --output_dir ./converted_data --max_workers 10
    ```

4. Combine the processed sliced data into a single large txt
    ```bash
    python combine_processed_data.py --braille_path processed_data --total_number 1000 --sliced_CN_datadir sliced_data
    ```

5. Convert the combined braille data into JSON format for training, validation, and testing
    ```bash
    # Keep all tones
    python braille_dataset_generation.py --output_dir ./data/10_pertent_tone --remove_tone_portion 0

    # Remove 90% of tones
    python braille_dataset_generation.py --output_dir ./data/10_pertent_tone --remove_tone_portion 0.9

    # Remove all tones
    python braille_dataset_generation.py --output_dir ./data/10_pertent_tone --remove_tone_portion 1
    ```

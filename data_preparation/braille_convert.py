import requests
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def requests_retry_session(
    retries=5,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 503, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


# Function to upload the file
def upload_file(file_path):
    upload_url = "http://www.braille.org.cn:8080/braille-web/braille/upload.html"
    files = {"file": open(file_path, "rb")}
    response = requests_retry_session().post(upload_url, files=files)
    print(response)

    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            print("ERROR: Response is not JSON format. Content:", response.content)
    else:
        print(
            "ERROR: Failed to upload file. Status code:",
            response.status_code,
            "file_path:",
            file_path,
        )


# Function to request Braille translation
def request_braille_translation(file_id, file_path):
    translate_url = (
        f"http://www.braille.org.cn:8080/braille-web/braille/fileToBraille.html"
    )
    params = {
        "id": file_id,
        "path": file_path,
        "firstLine": "on",
        "blankBefore": "off",
        "blankAfter": "off",
        "backLine": "off",
        "show": 1,
        "cnType": 1,
        "enType": 1,
        "rectNum": 32,
        "breakLine": 1,
        "flag": 2,
    }
    return requests_retry_session().get(translate_url, params=params)


# Function to download the Braille file
def download_braille_file(download_path):
    return requests_retry_session().get(download_path)


# Main workflow
import os
import glob
from tqdm import tqdm
import concurrent.futures


def convert_into_braille(
    data_dir=".\data", output_dir="./processed_data", max_workers=10
):
    os.makedirs(output_dir, exist_ok=True)
    file_paths = glob.glob(os.path.join(data_dir, "processed_input_*.txt"))

    # Create a ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(process_file, tqdm(file_paths))


def process_file(file_path):
    output_dir = "./processed_data"

    # Count the number of characters in the file
    with open(file_path, "r", encoding="utf-8") as f:
        contents = f.read()
    num_chars = len(contents)
    print("Number of characters in", file_path, ":", num_chars)

    base_name = os.path.basename(file_path)
    file_name, _ = os.path.splitext(base_name)
    output_file_path = os.path.join(output_dir, f"output_{file_name}.txt")
    upload_response = upload_file(file_path)

    if upload_response["status"] == "200":
        file_id = upload_response["info"]["FileId"]
        upload_file_path = upload_response["info"]["filePath"]
        print(upload_file_path)
        print("File uploaded successfully, FileId:", file_id)

        # Repeatedly request Braille translation until it succeeds
        start_time = time.time()
        while True:
            translate_response = request_braille_translation(file_id, upload_file_path)
            if translate_response.status_code == 200:
                print("Translation requested successfully, proceeding to download.")
                break
            else:
                print("Waiting for server to process the file...")
                time.sleep(15)  # Wait before retrying
        end_time = time.time()
        print("Time taken for translation request:", end_time - start_time, "seconds")

        # Download the Braille file
        print(translate_response)
        brf_path = translate_response.json()["info"][
            "pureBraillePath"
        ]  # Use the pureBraillePath from the translate_response
        print(brf_path)
        download_response = download_braille_file(brf_path)
        output_file_path = os.path.join(output_file_path)

        if download_response.status_code == 200:
            with open(output_file_path, "w") as f:
                f.write(download_response.content)
            print("Braille file downloaded successfully.")
        else:
            print(
                "Failed to download Braille file. Status code:",
                download_response.status_code,
            )
    else:
        print("File upload failed:", upload_response["info"])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert files into Braille.")

    parser.add_argument(
        "--data_dir",
        default=".\data",
        help="Directory containing the data files to be converted.",
    )
    parser.add_argument(
        "--output_dir",
        default="./processed_data",
        help="Directory where the converted Braille files will be saved.",
    )
    parser.add_argument(
        "--max_workers", type=int, default=10, help="Maximum number of worker threads."
    )
    args = parser.parse_args()

    convert_into_braille(
        data_dir=args.data_dir, output_dir=args.output_dir, max_workers=args.max_workers
    )

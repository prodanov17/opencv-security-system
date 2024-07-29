import os
import shutil
from datetime import datetime
from storage.storage import Storage
from utils import load_config

config = load_config("config.json")
STORAGE_PATH = config["implementations"]["storage"]["path"]
URL = config["app"]["url"] + STORAGE_PATH


class LocalStorage(Storage):
    def __init__(self):
        self.storage_path = os.path.join(os.getcwd(), STORAGE_PATH[1::])
        # Ensure the storage directory exists
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

    def save(self, path_to_file, output_path):
        filename = os.path.basename(output_path)
        new_path = os.path.join(self.storage_path, filename)
        print(f"Moving file from {output_path} to {new_path}")

        shutil.move(output_path, new_path)

        url = f"{URL}{filename}"
        return url

    def load(self, start_date, end_date, extension=".mp4"):
        files = os.listdir(self.storage_path)

        # Convert start and end dates to datetime objects
        start_date = datetime.strptime(start_date, "%d-%m-%y")
        end_date = datetime.strptime(end_date, "%d-%m-%y")

        # Filter files based on extension
        files = [f for f in files if f.endswith(extension)]

        # Define a function to extract the datetime from the filename
        def extract_datetime(filename):
            try:
                # Extract the date and time part before "-out.mp4"
                date_str = filename.split("-out")[0]
                # Parse the datetime from the extracted part
                return datetime.strptime(date_str, "%d-%m-%y-%H-%M-%S")
            except ValueError:
                # Return None if parsing fails
                return None

        # Filter files based on the extracted datetime
        matching_files = [
            {"date": dt, "url": f"{URL}/{f}"}
            for f in files
            if (dt := extract_datetime(f)) and start_date <= dt <= end_date
        ]

        return matching_files

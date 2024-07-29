from abc import ABC, abstractmethod
import threading
import requests
import ffmpeg
import os
from utils import load_config

config = load_config("config.json")
API_ENDPOINT = config["app"]["url"] + "/motion_detected"

class Storage(ABC):
    @abstractmethod
    def save(self, path_to_file, output_path):
        pass

    def handle_detection(self, path_to_file):
        def action_thread(path_to_file):
            output_path = path_to_file.split(".mp4")[0] + "-out.mp4"
            ffmpeg.input(path_to_file).output(output_path, vf='scale=-1:720').run()
            # shutil.copy(path_to_file, output_path)
            os.remove(path_to_file)
            url = self.save(path_to_file, output_path)
            data = {
                "url": url,
            }
            requests.post(API_ENDPOINT, json=data)

        thread = threading.Thread(target=action_thread, args=(path_to_file,))
        thread.start()

    @abstractmethod
    def load(self, start_date, end_date, extension=".mp4"):
        pass

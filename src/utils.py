import os

import requests
import platform
from requests_toolbelt.multipart import MultipartEncoder
from dotenv import dotenv_values
from tqdm import tqdm

class LingQConfig:
    def __init__(self):
        # Assumes the scripts are run in the src folder
        parent_dir = os.path.dirname(os.getcwd())
        env_path = os.path.join(parent_dir, ".env")
        config = dotenv_values(env_path)
        print(env_path)
        if os.path.exists(env_path):
            config = dotenv_values(env_path)
            if "APIKEY" in config:
                print("APIKEY found in .env file.")
            else:
                print("APIKEY not found in .env file.")
        else:
            print(".env file does not exist.")

        self.key = config["APIKEY"]
        self.headers = {"Authorization": f"Token {self.key}"}


class LingQ:
    API_URL_V3 = "https://www.lingq.com/api/v3/"

    def __init__(self):
        self.config = LingQConfig()

    def post_from_multipart_data(self, language_code: str, data: MultipartEncoder):
        headers = {**self.config.headers} | {"Content-Type": data.content_type}
        url = f"{LingQ.API_URL_V3}{language_code}/lessons/import/"
        response = requests.post(url=url, headers=headers, data=data)

        if response.status_code != 201:
            print(f"Response code: {response.status_code}")
            print(f"Response text: {response.text}")
            print(f"Response headers: {response.__dict__}")

        return response


class Transcriber:

    def __init__(self, wav_path, download_folder, video_length_in_seconds, model_name, language_code):
        self.wav_path = wav_path
        self.download_folder = download_folder
        self.video_length_in_seconds = video_length_in_seconds
        self.model_name = model_name
        self.language_code = language_code

    def transcribe(self):
        import faster_whisper

        models = ["tiny", "tiny.en", "base", "base.en",
                  "small", "small.en", "medium", "medium.en",
                  "large", "large-v1", "large-v2", "large-v3"]

        # Ask the user to choose a model
        print("Available models ⬇️")
        for i, model in enumerate(models, start=1):
            if i % 4 == 0:
                print(f"{i}. {model}")
            else:
                print(f"{i}. {model}", end=" | ")
        model_name = models[int(input("Enter the model number: ")) - 1]

        model = faster_whisper.WhisperModel(
            model_name,
            device="cuda",
            compute_type="float16",
            # cpu_threads=16,
        )

        segments, _info = model.transcribe(self.wav_path, beam_size=5)

        def format_timestamp(seconds: float, always_include_hours: bool = False):
            assert seconds >= 0, "non-negative timestamp expected"
            milliseconds = round(seconds * 1000.0)

            hours = milliseconds // 3_600_000
            milliseconds -= hours * 3_600_000

            minutes = milliseconds // 60_000
            milliseconds -= minutes * 60_000

            seconds = milliseconds // 1_000
            milliseconds -= seconds * 1_000

            hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
            return f"{hours_marker}{minutes:02d}:{seconds:02d},{milliseconds:03d}"

        # Initialize the progress bar
        pbar = tqdm(total=self.video_length_in_seconds, desc="Transcribing")

        def write_srt(transcript, file):
            for chunk, segment in enumerate(transcript, start=1):
                print(
                    f"{chunk}\n"
                    f"{format_timestamp(segment.start, always_include_hours=True)} --> "
                    f"{format_timestamp(segment.end, always_include_hours=True)}\n"
                    f"{segment.text.strip().replace('-->', '->')}\n",
                    file=file,
                    flush=True,
                )
                # Update the progress bar
                pbar.update(segment.end - segment.start)

        with open(f"{self.download_folder}audio.srt", "w", encoding="utf-8") as srt:
            write_srt(segments, file=srt)

        # Close the progress bar
        pbar.close()
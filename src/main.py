import os
import re
import sys
import urllib.request

import ffmpeg
from pytube import YouTube
from requests_toolbelt import MultipartEncoder

from utils import LingQ

LANGUAGE_CODE = "de"
COURSE_ID = 1598834
MODEL_NAME = "ggml-model-german.bin"


def should_overwrite(file_path, name):
    if os.path.exists(file_path):
        overwrite = input(f"The {name} already exists. Do you want to overwrite it? (y/n): ")
        if overwrite.lower() != "y":
            return False
    return True


def main():
    # Check if sys.argv[1] is provided
    if len(sys.argv) < 2:
        print("Error: You need to provide a valid URL")
        print("Usage: python main.py <URL>")
        sys.exit(1)

    # Get the video from the URL
    yt = YouTube(str(sys.argv[1]))
    video = yt.streams.filter(only_audio=True, file_extension='mp4').first()

    # Remove special any special char from the video's title
    clean_title = re.sub(r'[^\w\s]', '', yt.title)

    # Get the download folder
    download_folder = f"downloads/{clean_title}/"

    # Download the video
    video_file_path = f"{download_folder}video.mp4"
    if should_overwrite(video_file_path, "video"):
        video.download(output_path=download_folder, filename=f"video.mp4")
        print(f"{yt.title} has been downloaded successfully")

    # Download the thumbnail
    thumbnail_file_path = f"{download_folder}thumbnail.jpg"
    if should_overwrite(thumbnail_file_path, "thumbnail"):
        urllib.request.urlretrieve(yt.thumbnail_url, thumbnail_file_path)
        print(f"{yt.title} thumbnail has been downloaded successfully")

    # Convert the video to mp3 and wav
    mp3_path = f"{download_folder}audio.mp3"
    wav_path = f"{download_folder}audio.wav"
    overwrite_mp3 = should_overwrite(mp3_path, 'mp3')
    overwrite_wav = should_overwrite(wav_path, 'wav')

    if overwrite_mp3:
        ffmpeg.input(video_file_path).output(mp3_path).run(overwrite_output=True)
        print(f"{yt.title} has been converted to mp3 successfully")

    if overwrite_wav:
        ffmpeg.input(video_file_path).output(wav_path).run(overwrite_output=True)
        print(f"{yt.title} has been converted to wav successfully")

    # Transcribe the audio using Whisper
    if should_overwrite(f"{download_folder}audio.srt", 'subtitle'):
        model_path = os.path.abspath(f".\\whisper\\models\\{MODEL_NAME}")
        exe_path = os.path.abspath(".\\whisper\\main.exe")
        os.system(f"{exe_path} --threads 32 --output-srt --language {LANGUAGE_CODE} --model {model_path} --file \"{wav_path}\"")

    # Upload the video to LingQ
    url = f"https://www.lingq.com/en/learn/{LANGUAGE_CODE}/web/editor/courses/{COURSE_ID}"
    print(f"Starting upload at {url}")

    subs = open(os.path.join(download_folder, "audio.srt"), "r", encoding="UTF-8").read()
    audio = open(os.path.join(download_folder, "audio.mp3"), "rb")
    thumbnail = open(os.path.join(download_folder, "thumbnail.jpg"), "rb")

    data = MultipartEncoder(
        [
            ("audio", ("audio.mp3", audio, "audio/mpeg")),
            ("image", ("thumbnail.jpg", thumbnail, "application/octet-stream")),
            ("description", 'This video has been uploaded by Brendo'),
            ("file", ("audio.srt", subs, "application/octet-stream")),
            ("hasPrice", "false"),
            ("isProtected", "false"),
            ("isHidden", "true"),
            ("language", "de"),
            ("status", "private"),
            ("title", yt.title[:60]),
            ("video", f"{sys.argv[1]}"),
            ("videoDuration", str(yt.length)),
            ("save", "true"),
            ("collection", str(COURSE_ID)),
        ]
    )

    response = LingQ().post_from_multipart_data(LANGUAGE_CODE, data)
    if response.status_code != 201:
        return

    print(f"Posted video {yt.title} successfully")


if __name__ == "__main__":
    main()

import os
import re
import sys
import urllib.request

import ffmpeg
from requests_toolbelt import MultipartEncoder

from pytubefix import YouTube

from utils import LingQ, Transcriber

LANGUAGE_CODE = "de"
COURSE_ID = 1598834
MAX_TITLE_SIZE = 60


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
    yt = YouTube(str(sys.argv[1]), use_oauth=True, allow_oauth_cache=True)
    video = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

    # Remove special any special char from the video's title
    clean_title = re.sub(r'[^\w\s]', '', yt.title)

    # Get a custom title for the video
    print(f"Title: {clean_title[:MAX_TITLE_SIZE]}")
    custom_title = input(f"Enter a custom title for the video (leave empty for default): ")
    if custom_title:
        # Custom title can't exceed MAX_TITLE_SIZE
        if len(custom_title) > MAX_TITLE_SIZE:
            print("Error: Custom title can't exceed MAX_TITLE_SIZE")
            sys.exit(1)
        clean_title = re.sub(r'[^\w\s]', '', custom_title)

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
        ffmpeg.input(video_file_path).output(wav_path, ar="16000").run(overwrite_output=True)
        print(f"{yt.title} has been converted to wav successfully")

    # Transcribe the audio using Whisper
    if should_overwrite(f"{download_folder}audio.srt", 'subtitle'):
        transcriber = Transcriber(wav_path, download_folder, yt.length, LANGUAGE_CODE)
        transcriber.transcribe()

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
            ("description", 'This video has been uploaded by https://github.com/justbrendo/lingq-yt'),
            ("file", ("audio.srt", subs, "application/octet-stream")),
            ("hasPrice", "false"),
            ("isProtected", "false"),
            ("isHidden", "true"),
            ("language", "de"),
            ("status", "private"),
            ("title", clean_title),
            ("video", f"{sys.argv[1]}"),
            ("videoDuration", str(yt.length)),
            ("save", "true"),
            ("collection", str(COURSE_ID)),
        ]
    )

    if input("Do you want to upload the video to LingQ? (y/n): ") == "y":
        response = LingQ().post_from_multipart_data(LANGUAGE_CODE, data)
        if response.status_code != 201:
            return
        print(f"Posted video {yt.title} successfully")
        return


if __name__ == "__main__":
    main()

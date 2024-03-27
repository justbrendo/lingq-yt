# LingQ-YT

Easily download YouTube videos, convert them into audio, generate transcripts, and upload everything to LingQ for a seamless learning experience.

## Features

- **YouTube Video Retrieval**: Simply provide the link of the YouTube video you want to learn from, and LingQ-YT will handle the rest.
- **Audio Conversion**: LingQ-YT converts the downloaded YouTube video into both mp3 and wav audio formats, giving you flexibility in how you want to listen.
- **Transcription**: Using the power of Whisper, LingQ-YT generates a transcript of the video in the .srt format.
- **LingQ Upload**: Finally, LingQ-YT uploads the audio and transcript to LingQ, ready for your language learning journey.

## Technologies Used

- **PyTube**: For interacting with YouTube.
- **FFMpeg**: For converting video to audio.
- **Whisper**: For speech-to-text conversion.
- **LingQ**: For language learning.

## Important Notes

Please note that LingQ-YT relies on Const-me's GPU-accelerated port of whisper.cpp, which only supports Windows. Therefore, LingQ-YT is also Windows-only.

For more information, please refer to [Const-me's Whisper](https://github.com/Const-me/Whisper) and [ggerganov's Whisper.cpp](https://github.com/ggerganov/whisper.cpp).

## Acknowledgements

Special thanks to [Daxida](https://github.com/daxida) for his invaluable initial implementation of the LingQ API integration and handling.

## Getting Started

To use LingQ-YT, you'll need an API token from LingQ. You can get this by visiting [LingQ API Key](https://www.lingq.com/en/accounts/apikey/).

You will need FFMpeg installed in your computer. You can download it from [here](https://ffmpeg.org/download.html).

1. Clone the repository.
2. Install the required packages using `pip install -r requirements.txt`.
3. Create a `.env` file in the root directory with the following format:
    <br>`APIKEY="your-lingq-api-key"`
4. Get a ggml model from [here](https://huggingface.co/ggerganov/whisper.cpp/tree/main) and place it in the `src/whisper/models` directory.
5. Tweak the code to your liking. (Language code, course ID and the model to be used can be changed in the `main.py` file. Default is german)

## Usage

1. Run the script using `python main.py <video-link>`.
2. Follow the prompts to download, convert, transcribe, and upload your YouTube video to LingQ.
3. Enjoy your language learning journey!
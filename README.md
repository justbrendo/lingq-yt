# LingQ-YT

Easily download YouTube videos, convert them into audio, generate transcripts, and upload everything to LingQ. (Because we're too lazy to do it manually)

## Employed Tools

- **PyTubeFix**: For interacting with YouTube (a.k.a. downloading the videos).
- **FFMpeg**: For converting .mp3 to .wav (whisper only works with .wav files).
- **Whisper**: For speech-to-text transcription.
- **LingQ**: For language learning. ❤️

## Important Notes

Whisper relies heavily on [cuda](https://developer.nvidia.com/cuda-toolkit). Although it's possible to run it using your CPU, the transcription speed is going to be **much** worse.

For more information, please refer to [faster-whisper](https://github.com/SYSTRAN/faster-whisper) and [whisper](https://github.com/openai/whisper).

## Acknowledgements

Special thanks to [Daxida](https://github.com/daxida) for his initial implementation of the LingQ API integration and handling.

## Getting Started

To use LingQ-YT, you'll need an API token from LingQ. You can get this by visiting [LingQ API Key](https://www.lingq.com/en/accounts/apikey/).

You will need FFMpeg installed in your computer. You can download it from [here](https://ffmpeg.org/download.html).

As mentioned before, you will also need [CUDA Toolkit12.1](https://developer.nvidia.com/cuda-12-1-0-download-archive).

1. Clone the repository.
2. Install the required packages using `pip install -r requirements.txt`.
3. Create a `.env` file in the root directory with the following format:
    <br>`APIKEY="your-lingq-api-key"`
4. Tweak the code to your liking. (Language code, course ID and the model to be used can be changed in the `main.py` file. Default is german)

## Usage

1. Run the script using `python main.py <video-link>`.
2. Follow the prompts to download, convert, transcribe, and upload your YouTube video to LingQ.
3. Enjoy your language learning journey!
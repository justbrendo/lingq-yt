<h1 style="text-align:center;">LingQ-YT</h1>

This repository provides a script to download YouTube videos, convert them into audio, generate transcripts, and upload everything to LingQ. (Because we're too lazy to do it manually 🦥) 

## Employed Tools 🔨

- **PyTubeFix**: For interacting with YouTube (a.k.a. downloading the videos).
- **FFMpeg**: For converting .mp3 to .wav (whisper only works with .wav files).
- **WhisperX**: For speech-to-text transcription.
- **LingQ**: For language learning. ❤️

## Important Notes 📜

Whisper relies heavily on [cuda](https://developer.nvidia.com/cuda-toolkit). Although it's possible to run it using your CPU, the transcription speed is going to be **much** worse.

For more information, please refer to [WhisperX](https://github.com/m-bain/whisperX), [faster-whisper](https://github.com/SYSTRAN/faster-whisper) and [whisper](https://github.com/openai/whisper).

## Setup ⚙️

The following guide on how to setup your enviroment is a mixture from the setup already provided at WhisperX's repo and specific configurations needed for this repo. It can be partially skipped if you're already familiar with whisper.

To use LingQ-YT, you'll need an API token from LingQ. You can get this by visiting [LingQ API Key](https://www.lingq.com/en/accounts/apikey/).

You will need FFMpeg installed in your computer. You can download it from [here](https://ffmpeg.org/download.html).

As mentioned before, you will also need [CUDA Toolkit11.8](https://developer.nvidia.com/cuda-11-8-0-download-archive).

### 1. Create Python3.10 environment

`conda create --name lingq-x python=3.10`

`conda activate lingq-x`


### 2. Install PyTorch, e.g. for Linux and Windows CUDA11.8:

`conda install pytorch==2.0.0 torchaudio==2.0.0 pytorch-cuda=11.8 -c pytorch -c nvidia`

See other methods [here.](https://pytorch.org/get-started/previous-versions/#v200)

### 3. Install WhisperX's repo

`pip install git+https://github.com/m-bain/whisperx.git`

If already installed, update package to most recent commit

`pip install git+https://github.com/m-bain/whisperx.git --upgrade`

### 4. Clone this repository

`git clone https://github.com/justbrendo/lingq-yt.git`

### 5. Install the required packages

`pip install -r requirements.txt`.

### 6. Create the enviroment file

`echo 'APIKEY="your_api_key"' > .env`


Tweak the code to your liking. (Language code, course ID and the model to be used can be changed in the `main.py` file. Default is german)

## Usage

`python main.py <video-link>`


## Acknowledgements

Special thanks to [Daxida](https://github.com/daxida) for his initial implementation of the LingQ API integration and handling.
import os

import requests
from requests_toolbelt.multipart import MultipartEncoder
from dotenv import dotenv_values


class Config:
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
        self.config = Config()

    def post_from_multipart_data(self, language_code: str, data: MultipartEncoder):
        headers = {**self.config.headers} | {"Content-Type": data.content_type}
        url = f"{LingQ.API_URL_V3}{language_code}/lessons/import/"
        response = requests.post(url=url, headers=headers, data=data)

        if response.status_code != 201:
            print(f"Response code: {response.status_code}")
            print(f"Response text: {response.text}")
            print(f"Response headers: {response.__dict__}")

        return response

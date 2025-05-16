import os
from dotenv import load_dotenv

env_path = ".env"
load_dotenv(dotenv_path=env_path)

class Secrets():
    def __init__(self):
        self.serp_api = os.getenv("SERP_API")
        self.hf_token = os.getenv("HF_TOKEN")

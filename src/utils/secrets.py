from dotenv import load_dotenv
import os

env_path = ".env"
load_dotenv(dotenv_path=env_path)

class Secret():
    def __init__(self) -> None:
        self.SerpAPI = os.getenv("SERP_API")
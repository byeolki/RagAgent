import huggingface_hub, ollama
from transformers import pipeline
from huggingface_hub import login
from utils import HParams, Secrets

secrets = Secrets()
hparams = HParams()

class ChatModel():
    def __init__(self):
        key = secrets.hf_token
        self.pipe = self.load_model(hparams.platform, hparams.model_path, key)

    def load_model(self, platform: str, model_path: str, key: str=None):
        if key: login(key)
        if platform == "huggingface":
            pipe = pipeline("image-text-to-text", model=model_path) # OR "text-generation"
            return pipe
        elif platform == "ollama":
            ollama.pull(model_path)
            ollama_pipe = OllamaPipe(model_path)
            return ollama_pipe.pipeline

class OllamaPipe():
    def __init__(self, model_path: str):
        self.model_path = model_path

    def pipeline(self, messages: list):
        response = ollama.chat(model=self.model_path, messages=messages)
        return response['message']['content']

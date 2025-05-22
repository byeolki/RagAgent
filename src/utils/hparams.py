from .common import JsonManager

class HParams(JsonManager):
    def __init__(self, path: str="config/config.json", exist_data={}):
        super().__init__(path, exist_data)
        hparams = self.read()
        self.platform = hparams["platform"]
        self.model_path = hparams["model_path"]
        self.max_context = hparams["max_context"]

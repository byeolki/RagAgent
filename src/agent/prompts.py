import json
from utils import JsonManager

class PromptManager():
    def __init__(self):
        f = open("./prompts/search_prompt.txt", 'r')
        self.search_prompt = f.read()
        print(self.search_prompt)
        f.close()
        f = open("./prompts/answer_prompt.txt", 'r')
        self.answer_prompt = f.read()
        f.close()

    def _search_prompt(self, data: list, comment: str):
        json_manager = JsonManager("./config/tools.json")
        json_data = json_manager.read()
        tools_data = json_data["tools"]
        tools_str = json.dumps(tools_data, indent=2)
        search_prompt = self.search_prompt.replace("{tools}", tools_str)
        search_prompt = self.search_prompt.replace("{data}", str(data))
        search_prompt = self.search_prompt.replace("{comment}", comment if comment != "" else "No comment provided")
        return search_prompt

    def _answer_prompt(self, data: dict):
        return self.answer_prompt.replace("{data}", str(data))

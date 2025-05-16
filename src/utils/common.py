import os, json, random, re, ast
from snowflake import SnowflakeGenerator

snowflake_gen = SnowflakeGenerator(42)

def id_generator():
    return next(snowflake_gen)

def parse_history(chat_history: list):
    parsed_history = []
    for question_id, questions in chat_history:
        for question in questions:
            parsed_history.append(question)
    return parsed_history

def clean_parsed_history(parsed_history: list):
    index = len(parsed_history) - 1
    while parsed_history[index]["role"] != "user":
        del parsed_history[index]

def clean_answer(answer):
    ...

class JsonManager():
    def __init__(self, path: str, exist_data={}):
        self.path = path
        if not os.path.isfile(path):
            with open(self.path, "w", encoding="UTF-8") as f:
                json.dump(exist_data, f, ensure_ascii=False, indent="\t")

    def read(self):
        with open(self.path, "r", encoding="UTF-8") as f:
            return json.load(f)

    def write(self, data: dict):
        with open(self.path, "w", encoding="UTF-8") as f:
            json.dump(data, f, ensure_ascii=False, indent="\t")

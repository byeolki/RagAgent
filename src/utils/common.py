import os, json, random, re, ast
from bs4 import BeautifulSoup
from snowflake import SnowflakeGenerator

snowflake_gen = SnowflakeGenerator(42)

def generate_id():
    return next(snowflake_gen)

def parse_history(chat_history: list):
    parsed_history = []
    for question_id, questions in chat_history.items():
        for question in questions:
            parsed_history.append(question)
    return parsed_history

def clean_parsed_history(parsed_history: list):
    parsed_history = parsed_history[:-2]

def clean_html(html: str):
    soup = BeautifulSoup(html_content, 'html.parser')
    body = soup.find('body')
    if not body:
        return ""
    for tag in body.find_all():
        tag.attrs = {}
    body.attrs = {}
    return str(body)

def clean_answer(answer):
    pattern = r'<think>.*?</think>\s*'
    result = re.sub(pattern, '', answer, flags=re.DOTALL).strip()
    return result

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

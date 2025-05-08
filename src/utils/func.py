import os, json, random, re, ast
from snowflake import SnowflakeGenerator

snowflake_gen = SnowflakeGenerator(42)

def id_generator():
    return next(snowflake_gen)

def extract_answer(response_text): # Used AI
    cleaned_response = response_text.replace("\n", "").replace("'", '"')
    if cleaned_response == 'exit':
        return 'exit'
    pattern = r'<think>.*?</think>'
    cleaned_tools = re.sub(pattern, '', cleaned_response, flags=re.DOTALL)
    return cleaned_tools

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
            
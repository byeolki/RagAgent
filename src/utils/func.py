import os, json, random, re, ast

def id_generator(min: int, max: int, checker: list=None):
    number = random.randint(min, max)
    while number in checker:
        number = random.randint(min, max)
    return number        

def extract_answer(response_text): # Used AI
    cleaned_response = response_text.replace("\n", "")
    if cleaned_response == 'exit':
        return 'exit'
    pattern = r'<think>.*?</think>'
    cleaned_tools = re.sub(pattern, '', cleaned_response, flags=re.DOTALL)
    return cleaned_tools

def extract_json(data):
   try:
       return json.loads(data)
   except json.JSONDecodeError:
        pattern = r"ChatResponse\(.*?\)"
        if re.search(pattern, data, re.DOTALL):
            match = re.search(r"content=['\"](.+?)['\"]", data)
            if match:
                return {"content": match.group(1)}
            
            match_role = re.search(r"role=['\"](.+?)['\"]", data)
            if match_role:
                role = match_role.group(1)
                return {"role": role}
        
        if data.startswith("[") and data.endswith("]"):
            try:
                return ast.literal_eval(data)
            except (SyntaxError, ValueError):
                fixed_data = re.sub(r"'([^']*)':", r'"\1":', data)
                fixed_data = re.sub(r": *'([^']*)'", r': "\1"', fixed_data)
                return json.loads(fixed_data)

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
            
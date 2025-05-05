import ollama, os, json
from tools import WebTool
from utils import JsonManager, extract_answer, extract_json

class ToolSelector():
    def __init__(self, chat_id: int) -> None:
        self.chat_id = chat_id
        os.makedirs(f"./data/chat/{chat_id}", exist_ok=True)
        os.makedirs(f"./data/chat/{chat_id}/cache", exist_ok=True)

        json_manager = JsonManager("./src/tools/tools.json")
        self.system_prompt = str(json_manager.read())

        json_manager = JsonManager(f"./data/chat/{chat_id}/chat.json", exist_data=[])
        self.chat_record = json_manager.read()

    def input_question(self, question_id: int, content: str):
        JsonManager(f"./data/chat/{self.chat_id}/cache/{question_id}.json", exist_data=[])
        chat_record = self.chat_record.copy()
        chat_record.append({"role": "system", "content": self.system_prompt})
        chat_record.append({"role": "user", "content": content})
        chat_record.append({
            "role": "system", 
            "content": "Here you can find all the data collected so far. After reviewing this data, please respond with 'exit' if you think sufficient \
                information has been gathered, or specify which tools you would like to use to collect additional data."
        })
        self._tool_selction(question_id, chat_record)
    
    def _tool_selction(self, question_id: int, chat_record: list, data: list=[]): # Used AI(Some)
        print("searching..")
        response = ollama.chat(model='qwq:32b', messages=chat_record)
        raw_answer = response['message']['content']
        answer = extract_answer(raw_answer)
        print(answer)
        if answer == "exit":
            print("finish search")
            return data
        
        if answer is None or answer == "":
            print("Could not extract valid tool selection from response")
            chat_record.append({"role": "system", "content": "CRITICAL: Your response must ONLY be a JSON array like [{'func_name':'name', 'params':{}}] with no other text. Try again."})
            return self._tool_selction(question_id, chat_record, data)
        
        try:
            tools = json.loads(answer)
            print(f"Parsed tools: {tools}")
            web_tool = WebTool(self.chat_id, question_id)
            for tool in tools:
                func_name, params = tool["func_name"], tool["params"]
                if func_name == "url_access" and "url" in params:
                    if params["url"] == "..." or params["url"].endswith("..."):
                        import re
                        url_pattern = r'https?://[^\s\'",]+?(?=[\'"\s])'
                        urls = re.findall(url_pattern, raw_answer)
                        if urls:
                            params["url"] = urls[0]
                
                if func_name == "google_search":
                    print(params)
                    result = web_tool.google_search(**params)
                elif func_name == "url_access":
                    result = web_tool.url_access(**params)
                else:
                    print(f"Unknown function: {func_name}")
                    continue
                    
                data.append({"used_tool": tool, "data": result})
                
            return data
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            chat_record.append({"role": "system", "content": "CRITICAL: Your response must ONLY be a JSON array like [{'func_name':'name', 'params':{}}] with no other text. Try again."})
            return self._tool_selction(question_id, chat_record, data)
        except Exception as e:
            print(f"Error processing tools: {e}")
            chat_record.append({"role": "system", "content": "An error occurred processing your response. Please provide a valid JSON array in the format [{'func_name':'name', 'params':{}}]."})
            return self._tool_selction(question_id, chat_record, data)
    
class AnswerGenerator():
    def __init__(self, chat_id: int) -> None:
        self.chat_id = chat_id

    def answer_generate(self, question_id: int, data: list):
        json_manager = JsonManager(f"./data/chat/{self.chat_id}/chat.json")
        chat_record = json_manager.read()
        chat_record.append({"role": "system", "content": "Based on the data below, please provide an answer to the user's question.\n"+str(data)})
        response = ollama.chat(model='qwq:32b', messages=chat_record)
        raw_answer = response['message']['content']
        answer = extract_answer(raw_answer)
        chat_record[-1] = {"role": "assistant", "content": answer}
        chat_record = extract_json(str(chat_record))
        chat_record = json.dumps(chat_record)
        json_manager.write(chat_record)
        return answer
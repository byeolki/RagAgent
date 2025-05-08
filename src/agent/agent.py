import ollama, os, json, re
from tools import WebTool
from utils import JsonManager, extract_answer, Logger
from .prompts import PromptManager

class Agent():
    def __init__(self, chat_id: int) -> None:
        self.chat_id = chat_id
        os.makedirs(f"./data/chat/{chat_id}", exist_ok=True)
        os.makedirs(f"./data/chat/{chat_id}/cache", exist_ok=True)
        
        self.prompt_manager = PromptManager()

        json_manager = JsonManager(f"./data/chat/{chat_id}/chat.json", exist_data=[])
        self.chat_record = json_manager.read()
        self.internal_record = self.chat_record.copy()

    def input_question(self, question_id: int, content: str, logger: Logger):
        self.chat_record.append({"role": "user", "content": content})

        JsonManager(f"./data/chat/{self.chat_id}/cache/{question_id}.json", exist_data=[])
        self.internal_record.append({"role": "system", "content": self.prompt_manager._search_prompt})
        self.internal_record.append({"role": "user", "content": content})
        self.internal_record.append({
            "role": "system", 
            "content": "Here you can see all the data collected so far. Collect information according to the guide provided by 'system', \
                and if it seems to have been collected appropriately, end the collection using the method indicated in the guide."
        })
        logger.info("Searching..")
        return self._tool_selction(question_id, logger)
    
    def _tool_selction(self, question_id: int, logger: Logger): # Used AI(Some)
        json_manager = JsonManager(f"./data/chat/{self.chat_id}/cache/{question_id}.json")
        data = json_manager.read()
        self.internal_record.append({"role": "system", "content": f"Data collected to date: {data}"})
        response = ollama.chat(model='qwq:32b', messages=self.internal_record, options={"num_ctx": 131072})
        del self.internal_record[-1]
        raw_answer = response['message']['content']
        answer = extract_answer(raw_answer)
        if answer == "exit":
            logger.info("Finish search")
            return data
        if answer is None or answer == "":
            logger.info("Retry search")
            return self._tool_selction(question_id, logger)
        try:
            logger.info(answer)
            tools = json.loads(answer)
            web_tool = WebTool(self.chat_id, question_id)
            for tool in tools:
                func_name, params = tool["func_name"], tool["params"]
                if func_name == "url_access" and "url" in params:
                    if params["url"] == "..." or params["url"].endswith("..."):
                        url_pattern = r'https?://[^\s\'",]+?(?=[\'"\s])'
                        urls = re.findall(url_pattern, raw_answer)
                        if urls:
                            params["url"] = urls[0]
                if func_name == "google_search":
                    web_tool.google_search(**params)
                elif func_name == "url_access":
                    web_tool.url_access(**params)
                else:
                    continue
            return self._tool_selction(question_id, logger)
        except Exception as e:
            logger.error(e)
            return self._tool_selction(question_id, logger)

    def answer_generate(self, question_id: int, data: list, logger: Logger):
        json_manager = JsonManager(f"./data/chat/{self.chat_id}/chat.json")
        self.internal_record.append({"role": "system", "content": self.prompt_manager._answer_prompt(data)})
        response = ollama.chat(model='qwq:32b', messages=self.internal_record, options={"num_ctx": 131072})
        raw_answer = response['message']['content']
        answer = extract_answer(raw_answer)

        self.chat_record.append({"role": "assistant", "content": answer})
        self.internal_record.append({"role": "assistant", "content": answer})
        json_manager.write(self.chat_record)
        logger.info(answer)
        return answer
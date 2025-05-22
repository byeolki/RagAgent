import ollama, os, json, re
from tools import WebTool
from tools.tool import BaseTool
from utils import JsonManager, clean_answer, Logger, parse_history, clean_parsed_history
from .prompts import PromptManager
from .model import ChatModel

class Agent():
    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.configure_agent(chat_id)

    def configure_agent(self, chat_id: int):
        os.makedirs(f"./history/{chat_id}", exist_ok=True)
        os.makedirs(f"./history/{chat_id}/cache", exist_ok=True)
        os.makedirs(f"./logs/{chat_id}", exist_ok=True)

        self.prompt_manager = PromptManager()
        model = ChatModel()
        self.pipe = model.pipe

    def initialize_context(self, question_id: int, content: str):
        self.logger = Logger(self.chat_id, question_id)

        json_manager = JsonManager(f"./history/{self.chat_id}/chat.json", exist_data=[])
        chat_history = json_manager.read()
        chat_history[str(question_id)] = [{
            "role": "user", "content": content
        }]
        json_manager.write(chat_history)
        self.chat_history = chat_history

        json_manager = JsonManager(f"./history/{self.chat_id}/cache/{question_id}.json")
        cache = json_manager.read()
        cache[str(question_id)] = [{
            "role": "user", "content": content
        }]
        self.internal_history = parse_history(chat_history)
        self.retrieved_data = []

    def handle_query(self, question_id: int, content: str):
        self.initialize_context(question_id, content)
        data = self.retrieve_documents(question_id)
        answer = self.generate_answer(question_id, data)
        return answer

    def retrieve_documents(self, question_id: int):
        self.internal_history.append({"role": "system", "content": f"Data collected to date: {self.retrieved_data}"})
        raw_answer = self.pipe(self.internal_history)
        answer = clean_answer(raw_answer)
        clean_parsed_history(self.internal_history)
        if answer == "exit":
            self.logger.info("Finish search")
            return self.retrieved_data
        if answer is None or answer == "":
            self.logger.info("Retry search")
            return self.retrieve_documents(question_id)
        try:
            self.logger.info(answer)
            tools = json.loads(answer)
            base_tool = BaseTool(self.chat_id, question_id)
            web_tool = WebTool(self.chat_id, question_id)
            for tool in tools:
                tool_name, params = tool["func_name"], tool["params"]
                if tool_name == "google_search":
                    data = web_tool.google_search(**params)
                elif tool_name == "url_access":
                    data = web_tool.url_access(**params)
                elif tool_name == "delete_data":
                    base_tool.delete_data(**params)
                    data = None
                else:
                    continue
                base_tool.called_tool({
                    "tool_command": tool,
                    "collected_data": data
                })
            if len(str(self.retrieved_data)) > 90000:
                raise Exception("There is too much data. Delete one and add it again or add another one")
            self.retrieved_data.append(data)
            return self.retrieve_documents(question_id)
        except Exception as e:
            self.logger.error(str(e))
            self.internal_history.append({"role": "system", "content": f"Exception: {e}"})
            return self.retrieve_documents(question_id)

    def generate_answer(self, question_id: int, data: list):
        json_manager = JsonManager(f"./data/chat/{self.chat_id}/chat.json")
        self.internal_history.append({"role": "system", "content":  self.prompt_manager.answer_prompt(data)})
        raw_answer = self.pipe(self.internal_history)
        answer = clean_answer(raw_answer)
        self.chat_history.append({"role": "assistant", "content": answer})
        self.internal_history.append({"role": "assistant", "content": answer})
        json_manager.write(self.chat_history)
        return answer

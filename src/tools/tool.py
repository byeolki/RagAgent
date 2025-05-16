import serpapi, requests
from bs4 import BeautifulSoup
from utils import JsonManager, Secrets, HParams

secret = Secrets()

class BaseTool():
    def __init__(self, chat_id: int, question_id: int):
        self.json_manager = JsonManager(f"./history/{chat_id}/cache/{question_id}.json")
        self.data = self.json_manager.read()

    def _used_tool(self, tool_data: dict):
        data = self.json_manager.read()
        data.append(tool_data)
        self.json_manager.write(data)

class WebTool(BaseTool):
    def __init__(self, chat_id: int, question_id: int):
        super().__init__(chat_id, question_id)

    def google_search(self, query: str):
        search = serpapi.search(params = {
            "engine": "google",
            "q": query,
            "api_key": Secrets().serp_api
        })
        data = search.as_dict()
        self._used_tool(data)
        return data

    def url_access(self, url: str):
        data = {url: "Error: Not found site"}
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            full_html = str(soup)
        self._used_tool(data)
        return data

class CalcTool():
    def __init__(self):
        ...

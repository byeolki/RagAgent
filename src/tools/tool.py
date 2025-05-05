import os, serpapi, requests, html_to_json, json
from bs4 import BeautifulSoup
from utils import JsonManager

class BaseTool():
    def __init__(self, chat_id: int, question_id: int):
        self.json_manager = JsonManager(f"./data/chat/{chat_id}/cache/{question_id}.json")
        self.data = self.json_manager.read()

    def _used_tool(self, tool_data: dict):
        data = self.json_manager.read()
        data.append(tool_data)
        self.json_manager.write(data)

class WebTool(BaseTool):
    def __init__(self, chat_id, question_id):
        super().__init__(chat_id, question_id)
    
    def google_search(self, query: str):
        params = {
            "engine": "google",
            "q": query,
            "api_key": "d94f04c4608c787a2a864ad17c40ede39d4392e4b696177c749d1e3f81d1e7f4"
        }
        search = serpapi.search(params)
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
            data = html_to_json.convert(full_html)
        self._used_tool(json)
        return data
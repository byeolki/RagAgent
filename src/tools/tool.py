import serpapi, requests, html_text
from bs4 import BeautifulSoup
from utils import JsonManager
from utils.secrets import Secret

class BaseTool():
    def __init__(self, chat_id: int, question_id: int):
        self.json_manager = JsonManager(f"./data/chat/{chat_id}/cache/{question_id}.json")
        self.data = self.json_manager.read()

    def _used_tool(self, tool_data: dict):
        data = self.json_manager.read()
        data.append(tool_data)
        self.json_manager.write(data)

class WebTool(BaseTool):
    def __init__(self, chat_id: int, question_id: int):
        super().__init__(chat_id, question_id)
    
    def google_search(self, query: str):
        params = {
            "engine": "google",
            "q": query,
            "api_key": Secret().SerpAPI
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
            tree = html_text.parse_html(full_html)
            data = html_text.extract_text(tree)
        self._used_tool(data)
        return data
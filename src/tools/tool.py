import serpapi, requests
from bs4 import BeautifulSoup
from utils import JsonManager, Secrets, HParams, generate_id, clean_html

secret = Secrets()

class BaseTool():
    def __init__(self, chat_id: int, question_id: int):
        self.json_manager = JsonManager(f"./history/{chat_id}/cache/{question_id}.json")
        self.data = self.json_manager.read()

    def delete_data(self, id: int):
        data = self.json_manager.read()
        del data[id]
        self.json_manager.write(data)

    def called_tool(self, tool_data: dict):
        id = generate_id()
        data = self.json_manager.read()
        data[id] = tool_data
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
        return data
        # url = "https://www.searchapi.io/api/v1/search"
        # response = requests.get(url, params={
        #     "engine": "google",
        #     "q": query,
        #     "api_key": secret.serp_api
        # })
        # return str(response.text)

    def url_access(self, url: str):
        data = f"Error: Not found site, URL: {url}"
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            full_html = str(soup)
            data = clean_html(full_html)
        return data

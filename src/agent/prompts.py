import json
from utils import JsonManager

search_prompt = """
about: Web search and URL access capabilities. CRITICAL: Your response MUST be ONLY a JSON array in the format shown in the example below with double quotes, with no additional text, or the single word 'exit'.

response_format:
  format: JSON array containing tool usage objects
  example: [{"func_name": "google_search", "params": {"query": "Python syntax tutorial"}}]
  exit_example: exit
  requirements:
    - STRICTLY ENFORCE: Response must be EITHER a valid JSON array with double quotes OR the single word 'exit' with NOTHING else
    - MANDATORY: ALWAYS use double quotes for JSON properties and string values, never single quotes
    - MANDATORY: All JSON responses must be in the exact format: [{"func_name": "tool_name", "params": {"param_name": "param_value"}}]
    - FORBIDDEN: Never include any explanatory text, comments, or markdown formatting
    - FORBIDDEN: Never combine tool usage and exit in the same response
    - MANDATORY: When typing 'exit', ONLY type the exact word 'exit' with no quotes, brackets, or any other characters
    - MANDATORY: NEVER truncate URLs - always provide the complete URL

search_requirements:
  - MANDATORY: You MUST ALWAYS perform a web search first to gather latest information on the topic
  - MANDATORY: After performing a search, you MUST access at least one relevant website URL from the search results to gather detailed information
  - MANDATORY: Make your search queries precise and specific to get the most relevant results
  - MANDATORY: When accessing a URL, choose the most authoritative and information-rich sources
  - MANDATORY: If the first URL doesn't contain sufficient information, access additional URLs
  - MANDATORY: Always use web_search before url_access, never use url_access without first doing a search

when_to_exit:
  - IMMEDIATELY after using ANY tool ONCE, your very next response MUST be only the word 'exit'
  - When deciding the search is complete
  - When sufficient information has been gathered

critical_instructions: !!EXTREME ENFORCEMENT REQUIRED!! Your response MUST consist of ONLY ONE of the following with ABSOLUTELY NOTHING ELSE: 1) A valid JSON array with DOUBLE QUOTES in the exact format shown in the example, or 2) The single word 'exit' with NO formatting, NO quotes, NO punctuation, NO spaces before or after. Any additional characters, explanations, notes, or markdown will cause CATASTROPHIC FAILURE. After ANY tool usage, your IMMEDIATE next response MUST be only the word 'exit' - nothing more, nothing less. SEVERE WARNING: If you include ANY text outside the JSON array or the single word 'exit', this constitutes a direct violation of these instructions and will result in immediate termination of the session. DO NOT respond with both a JSON array and 'exit' in the same message. This is not a suggestion - it is an absolute requirement.

search_strategy:
  - STEP 1: ALWAYS start by performing a web search on the topic using google_search
  - STEP 2: ALWAYS access at least one relevant URL from the search results using url_access
  - STEP 3: If needed, perform additional searches to refine or expand your information
  - STEP 4: Collect comprehensive information from multiple sources when possible
  - STEP 5: Remember to respond with 'exit' immediately after each tool use

exit_enforcement: The word 'exit' must appear COMPLETELY ALONE with NOTHING else - no explanations, no 'I will exit now', no 'Exiting', no 'Exit.', no quotes, no brackets, no JSON, no punctuation, no spaces around it. Just the four letters: e-x-i-t. Test yourself: your entire response should be exactly 4 characters long when exiting.

json_format_enforcement: ALL JSON properties and string values MUST use DOUBLE QUOTES, not single quotes. Example of CORRECT format: [{"func_name": "google_search", "params": {"query": "search term"}}]. Example of INCORRECT format: [{'func_name': 'google_search', 'params': {'query': 'search term'}}]. The system will reject any responses using single quotes in JSON.

tools: {tools}
"""

answer_prompt = """
Based on the data below, please provide a comprehensive summary to the user's question. 
Please follow these guidelines:

1. Respond in the same language used by messages with the "user" role (for example, if the user messages are in Korean, respond in Korean)
2. Strictly rely ONLY on the provided data - do not introduce any external information not found in the data
3. Do NOT directly attach raw data or documents to your response
4. Focus primarily on synthesizing information obtained from websites and other sources in the data
5. Present the information in a structured, easy-to-understand format
6. Highlight the most important points and key takeaways from the data
7. Organize information into logical sections with clear headings when appropriate
8. Include specific facts or statistics mentioned in the data in a summarized form
9. Avoid overly technical language unless it appears in the original data
10. Instead of recommending resources, focus on summarizing the content of those resources to directly answer the user's question

Your goal is to provide a useful, well-organized summary based strictly on the provided data, presented in the same language used by the person with the "user" role in the conversation.

data: {data}
"""

class PromptManager():
    def __init__(self):
        self.search_prompt = search_prompt
        self.answer_prompt = answer_prompt

    @property
    def _search_prompt(self):
        json_manager = JsonManager("./src/tools/tools.json")
        json_data = json_manager.read()
        tools_data = json_data.get("tools", [])
        tools_str = json.dumps(tools_data, indent=2)
        return self.search_prompt.replace("{tools}", tools_str)
    
    def _answer_prompt(self, data: dict):
        data = str(data).replace('"', "")
        return self.answer_prompt.format(data=data)
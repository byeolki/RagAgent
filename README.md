# 🤖 RagAgent

RagAgent는 검색 증강 생성(Retrieval-Augmented Generation) 기반의 AI 에이전트 시스템입니다. 이 레포지토리는 웹 검색과 URL 접근 기능을 통합한 대화형 AI 에이전트를 구현하는 코드를 제공합니다.

## ✨ Features

- Google 검색 및 웹 페이지 스크래핑 통합
- 다양한 AI 모델 지원 (Ollama, Hugging Face)
- 컨텍스트 관리 및 캐싱 시스템
- 확장 가능한 도구 아키텍처
- 로깅 및 히스토리 추적

## ⚙️ Installation

```bash
git clone https://github.com/username/RagAgent.git
cd RagAgent
pip install -r requirements.txt
```

## 🔧 Configuration

`config/config.json` 파일을 수정하여 사용할 모델과 설정을 변경할 수 있습니다:

```json
{
    "platform": "ollama", # or HuggingFace
    "model_path": "your_model_path",
    "max_context": 100000
}
```

- `src/tools/tool.py`를 수정하여 새로운 도구 기능을 구현할 수 있습니다.
- `config/tools.json` 파일을 수정하여 에이전트가 사용할 도구를 추가하거나 삭제할 수 있습니다.

- 현재 검색 기능은 SERP API를 활용하여 구현되어 있으나, 필요에 따라 다른 검색 API로 대체하여 사용할 수 있습니다. `src/tools/tool.py`의 `WebTool` 클래스를 수정하여 원하는 검색 엔진이나 API로 변경 가능합니다.

## 🚀 Usage

```bash
python src/run.py
```

자세한 사용법은 소스코드의 주석을 참고하세요.

## 🙏 Credits & References

이 프로젝트는 다음 오픈소스 라이브러리들을 활용합니다:

- Ollama
- Hugging Face Transformers
- BeautifulSoup
- SerpAPI

## ⚖️ License

이 프로젝트의 코드는 MIT License에 따라 배포됩니다:

MIT License

Copyright (c) 2024 RagAgent Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

단, 이 프로젝트에 포함된 외부 라이브러리들은 각각의 라이센스를 따릅니다.

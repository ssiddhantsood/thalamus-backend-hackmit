import json
from typing import Dict, List
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOpenAI

from llmsetup import llms

def get_llm_config(select_llm: str) -> Dict:
    for llm in llms:
        if llm['model'] == select_llm:
            return llm
    raise ValueError(f"Model '{select_llm}' not found in configurations")

def list_models() -> List[str]:
    return [config['model'] for config in llms]

def get_llm_client(select_llm: str):
    llm_config = get_llm_config(select_llm)
    provider = llm_config['provider']

    if provider == 'ollama':
        return _get_ollama_client(select_llm, llm_config)
    elif provider == 'openai':
        return _get_openai_client(llm_config)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def _get_ollama_client(select_llm: str, llm_config: Dict):
    num_ctx = _get_ollama_context_size(select_llm)
    return Ollama(
        base_url=llm_config['apiBase'],
        model=llm_config['model'],
        temperature=0.1,
        num_ctx=num_ctx
    )

def _get_openai_client(llm_config: Dict):
    if llm_config['title'] == 'Groq':
        return ChatGroq(model="mixtral-8x7b-32768", temperature=0)
    else:
        return ChatOpenAI(model_name=llm_config['model'])

def _get_ollama_context_size(select_llm: str) -> int:
    if select_llm == "mixtral:8x22b":
        return 32000
    elif 'llama' in select_llm:
        return 8000
    else:
        return 2048  # Ollama Default

# Usage example
if __name__ == "__main__":
    available_models = list_models()
    print(f"Available models: {available_models}")

    selected_model = "your_selected_model_here"
    try:
        client = get_llm_client(selected_model)
        print(f"Created client for model: {selected_model}")
    except ValueError as e:
        print(f"Error: {e}")
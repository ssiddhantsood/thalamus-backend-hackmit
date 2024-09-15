import os
import google.generativeai as genai
import os
from langchain_community.llms import HuggingFaceHub
from dotenv import load_dotenv

load_dotenv()

llm_config = {
    "config_list": [
        # GPT-4
        {"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]},
        
        # Claude 3.5 Sonnet
        {"model": "claude-3-sonnet-20240229", "api_key": os.environ["ANTHROPIC_API_KEY"]},
        
        # Gemini 1.5 Pro
        {"model": "gemini-1.5-pro", "api-key": os.environ["API_KEY"]},
        
        # Mixtral (via Hugging Face)
        {"model": "mistralai/Mixtral-8x7B-Instruct-v0.1", "token": os.environ["HUGGINGFACE_API_KEY"]},
        
        # LLAMA 2 (via Hugging Face)
        {"model": "meta-llama/Llama-2-70b-chat-hf", "token": os.environ["HUGGINGFACE_API_KEY"]},
        
        # Dolphin (via Hugging Face)
        {"model": "cognitivecomputations/dolphin-2.6-mixtral-8x7b", "token": os.environ["HUGGINGFACE_API_KEY"]}
    ]
}


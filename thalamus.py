import random

models =  [
    "gpt-4",
    "claude-3-sonnet-20240229",
    "gemini-1.5-pro",
    "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "meta-llama/Llama-2-70b-chat-hf",
]

def find_llm(query):
    return random.choice(models)
    
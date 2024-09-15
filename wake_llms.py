import llmsetup
from langchain_community.llms import OpenAI, Anthropic
from langchain_google import GoogleVertexAI
from langchain_community.llms import HuggingFaceHub

llms = []

for config in llmsetup.llm_config["config_list"]:
    if config["model"].startswith("gpt-"):
        llms.append(OpenAI(model=config["model"], api_key=config["api_key"]))
    elif config["model"].startswith("claude-"):
        llms.append(Anthropic(model=config["model"], api_key=config["api_key"]))
    elif config["model"].startswith("gemini-"):
        model = genai.GenerativeModel("gemini-1.5-flash")
    else:  # Hugging Face models
        llms.append(HuggingFaceHub(repo_id=config["model"], huggingfacehub_api_token=config["token"]))

# Check if working
for llm in llms:
    response = llm("Hello, world!")
    print(f"Response from {llm.__class__.__name__} ({llm.model if hasattr(llm, 'model') else 'Unknown model'}): {response}")
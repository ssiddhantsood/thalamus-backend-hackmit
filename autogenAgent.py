from autogen import AssistantAgent, UserProxyAgent, ConversableAgent,config_list_from_json
import llmsetup
import os
import toolkit

config_list = llmsetup.llm_config["config_list"]

assistant = ConversableAgent(
    name="Assistant",
    system_message="You are a helpful AI assistant. "
    "You can help with simple calculations. "
    "Return 'TERMINATE' when the task is done.",
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
)

user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

# Register the tool signature with the assistant agent.
assistant.register_for_llm(name="calculator", description="A simple calculator")(toolkit.calculator())

# Register the tool function with the user proxy agent.
user_proxy.register_for_execution(name="calculator")(toolkit.calculator())
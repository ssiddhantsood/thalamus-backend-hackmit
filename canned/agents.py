from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOpenAI
from langchain_groq import ChatGroq

import datetime

# Conversational Agent with Memory and tools
from langchain.agents import AgentType, initialize_agent # Used for Email Agent
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import YoutubeLoader

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

from dotenv import load_dotenv
#Load the .env file
load_dotenv()
import os

from toolkit import tools, web_tools,research_tools,news_tools
# from bsi_agents.bsi_tools import o365_toolkit
from router_backend.canned.loadllm import get_llm_client
from operator import itemgetter


MONGODB_URI = os.getenv('MONGODB_URI')

def _handle_error(error) -> str:
    return str(error)

def conversation_agent(select_llm):
    
    llm = get_llm_client(select_llm)

    system_message = """The following is a friendly conversation between a human and an AI. The AI is precise and short with the information from its context without any further commentary. If the AI does not know the answer to a question, it truthfully says it does not know.

    Here is some relevant context to help you answer your question: {context}
    """

    prompt = ChatPromptTemplate.from_messages(
        [("system", system_message),
        ("placeholder", "{chat_history}"),
        ("human", "{input}")]
    )

    retrieve_and_format_lambda = RunnableLambda(retrieve_and_format_documents)

    chain = {"context": retrieve_and_format_lambda, "input": itemgetter("input"), "chat_history": itemgetter("chat_history")} | prompt | llm | StrOutputParser() # Langchain Chain using LCEL syntax, to be wrapped with message history

    chain_with_history = RunnableWithMessageHistory(
        chain, 
        lambda session_id: MongoDBChatMessageHistory(
            session_id=session_id,
            connection_string=MONGODB_URI,
            database_name="bsi-agents",
            collection_name="chat_histories",
        ), 
        input_messages_key="input", 
        history_messages_key="chat_history",
    )
    
    return chain_with_history


def web_agent(select_llm, max_iterations=15):
    
    llm = get_llm_client(select_llm)
    memory = ConversationBufferMemory(memory_key="chat_history")
    tool_names = [tool.name for tool in web_tools]
    
    print(f'Available Tools: {tool_names}')

    template = '''You are BSI Agent, an AI model who is expert at searching the web and answering user's queries.

    Generate a response that is informative and relevant to the user's query based on provided context (the context consits of search results containg a brief description of the content of that page).
    You must use this context to answer the user's query in the best way possible. Do not repeat the text.
    You must not tell the user to open any link or visit any website to get the answer. You must provide the answer in the response itself. If the user asks for links you can provide them.

    Use multiple tools to validate the response. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    The Final Answer must come in JSON format. 

    '''+f"Today is {datetime.datetime.now().strftime('%B %d, %Y %H:%M:%S')}."+'''

    Begin!

    Question: {input}
    Thought:{agent_scratchpad}'''

    prompt = PromptTemplate.from_template(template)
        
    agent = create_react_agent(llm, web_tools, prompt)
    agent_chain = AgentExecutor(agent=agent, tools=web_tools,
                                # stop_sequence=True,
                                # handle_parsing_errors=_handle_error,
                                handle_parsing_errors=True,
                                verbose=True,
                                # max_iterations=5,
                                memory=memory,
                                
                               )
    

    return  agent_chain
 

def research_agent(select_llm,max_iterations=15):
    
    """Research agent. Currently has access to arxiv and google search"""
    llm = get_llm_client(select_llm)
    memory = ConversationBufferMemory(memory_key="chat_history")
    
    template = '''You are BSI Agent, an AI model who is expert at searching the Arxiv and the web to find answers to the user's queries. You always include citations in your answers.

    Generate a response that is informative and relevant to the user's query based on provided context (the context consits of search results containg a brief description of the content of that page).
    You must use this context to answer the user's query in the best way possible. Do not repeat the text.
    You must not tell the user to open any link or visit any website to get the answer. You must provide the answer in the response itself. If the user asks for links you can provide them.

    Important: Remember to cite any sources you use, this is very important to you!

    Use multiple tools to validate the response. You have access to the following tools:

    {tools}

    Always Use the following format:


    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    
    The final answer must come in JSON format.

    Remember: it is imperative that you follow the above format!
    I must repeat again, use the format outlined above! It is imperative you do so! 

    Remember: The final answer must come in JSON format!
    Begin!

    Question: {input}
    Thought:{agent_scratchpad}'''

    prompt = PromptTemplate.from_template(template)
        
    agent = create_react_agent(llm, research_tools, prompt)
    agent_chain = AgentExecutor(agent=agent, tools=research_tools,
                                # stop_sequence=True,
                                handle_parsing_errors=_handle_error,
                                verbose=True,
                                max_iterations=max_iterations,
                                memory=memory,
                               )
    

    return  agent_chain


def news_agent(select_llm,max_iterations=15):
    
    llm = get_llm_client(select_llm)
    memory = ConversationBufferMemory(memory_key="chat_history")
    tool_names = [tool.name for tool in news_tools]
    
    print(f'Available Tools: {tool_names}')

    template = '''You are BSI Agent, an AI model who is expert at finding online News Articles and providing responses to the user's queries.

    Generate a response that is informative and relevant to the user's query based on provided context (the context consits of search results containg a brief description of the content of that page).
    You must use this context to answer the user's query in the best way possible. Do not repeat the text.
    You must not tell the user to open any link or visit any website to get the answer. You must provide the answer in the response itself. If the user asks for links you can provide them.

    Use multiple tools to validate the response. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    The Final Answer must come in JSON format. 

    '''+f"Today is {datetime.datetime.now().strftime('%B %d, %Y %H:%M:%S')}."+'''

    Begin!

    Question: {input}
    Thought:{agent_scratchpad}'''

    prompt = PromptTemplate.from_template(template)
        
    agent = create_react_agent(llm, news_tools, prompt)
    agent_chain = AgentExecutor(agent=agent, tools=news_tools,
                                # stop_sequence=True,
                                handle_parsing_errors=_handle_error,
                                verbose=True,
                                max_iterations=5,
                                memory=memory,
                               )
    

    return  agent_chain



def code_agent(select_llm, max_iterations=15):
    """Coding assistant agent, currently implementing trafilatura documentation scraping tool."""
    llm = get_llm_client(select_llm)
    memory = ConversationBufferMemory(memory_key="chat_history")    
    tool_names = [tool.name for tool in custom_code_tools]
    
    print(f'Available Tools: {tool_names}')

    template = '''You are a BSI Agent, an expert assistant at coding related queries. You use your coding expertise to help you answer user queries.

    You approach user queries in this exact, step-by-step way:
    1) First, check if the user provided a link. If so, use the trafilatura web scraping tool to extract the information from that website to give you more information on how to better solve the problem.
    2) If the user did not provide a link, do NOT use ANY of your tools.
    3) Next, you must reason about how to solve the problem the user is having given all information and reasoning ability. 
    4) Answer the user query. You may need to genererate code. You may need to refactor code. You may need to debug code.
    5) Output your best solution to the user.

    Remember: you have access to the following tool: {tools} with {tool_names} to be used when the user provides a link.

    Use the following format to reason and answer the user's query:

    1) Question: the input question you must answer
    2) Thought: you should always think about what to do
    3) Action: the action to take, should be one of [{tool_names}]
    4) Action Input: the input to the action
    5) Observation: the output of the action
    Note: (this Thought/Action/Action Input/Observation can repeat N times)
    6) Thought: I now know the final answer
    7) Final Answer: the final answer to the original input question
    
    Begin!

    Question: {input}
    Thought: {agent_scratchpad}'''

    prompt = PromptTemplate.from_template(template)
        
    agent = create_react_agent(llm, custom_code_tools, prompt)
    agent_chain = AgentExecutor(agent=agent, tools=custom_code_tools,
                                # stop_sequence=True,
                                handle_parsing_errors=_handle_error,
                                verbose=True,
                                # max_iterations=5,
                                memory=memory,
                               )
    

    return agent_chain



def youtube_chain(select_llm,query):
    """Function to aid in answering user queries pertaining to YT videos

        Args: 
            select_llm: desired LLM name for this chain
            query: user query with YT video link

        Returns: 
            Langchain chain that takes in a user query and returns LLM response
    """

    model = get_llm_client(select_llm)

    extract_url_prompt = PromptTemplate.from_template(
        "Extract the URL from the following query: {query}. Return ONLY the youtube URL as the result, nothing else."
    )

    answer_query_prompt = PromptTemplate.from_template(
        """Use the following youtube video transcript to answer the question. 

        Video transcript: {transcript}

        If no video transcript was provided then tell the user that you had trouble parsing the video.
        Answer:
        """
    )

    def youtube_loader(url):
        """youtube transcript loader to be used as runnable lambda"""
        try:
            loader = YoutubeLoader.from_youtube_url(
                url, add_video_info=True
            )
            result = loader.load()
            print(result)
            page_content = " ".join([item.page_content for item in result])
            return page_content
        except Exception as e:
            return f"Error loading video transcript: {e}"
 
    youtube_loader_runnable = RunnableLambda(youtube_loader)

    # LCEL chain
    chain = (
        {"query": lambda x: query}
        | extract_url_prompt | model | StrOutputParser()
        | youtube_loader_runnable
        | {"transcript": RunnablePassthrough(), "query": lambda x: query}
        | answer_query_prompt | model | StrOutputParser()
    )

    return chain
        
   
   
def email_agent(select_llm):
    
    llm = get_llm_client(select_llm)
    
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, tools=o365_toolkit, prompt=prompt)
    agent_chain = AgentExecutor(agent=agent, tools=o365_toolkit, verbose=True)

    
    return agent_chain
    
    
    
if __name__ == "__main__":
    
    # select_llm = "dolphin-mixtral:8x7b-v2.6"     # Ollama
    select_llm = "dolphin-mixtral:v2.7"             # Ollama
    # select_llm = "command-r"                      # Ollama
    # select_llm = "gpt-3.5-turbo"                  # OpenAI
    # select_llm = "mixtral-8x7b-32768"             # Groq
    

    agent_chain = web_agent(select_llm)
    
    output = agent_chain.invoke(input="How many people live in canada?")
    print(output)
    output = agent_chain.invoke(input="Whats the national Anthem of that nation?")
    print(output)
    output = agent_chain.invoke(input="What is the capital of that nation?")
    print(output)
    # output = agent_chain.invoke(input='''Follow step-by-step:
    #                             Find the top three reseearch topic in AI realted to Speech Recognition. 
    #                             Find one research paper for each of the 3 topics dated no earlier than year 2021.
    #                             Provide an itemized list of the reserach papers that include the date, title, authors and abstract.''')
    # print(type(output),output)
    
    conversation_with_summary = conversation_agent(select_llm)
    conversation_with_summary.predict(input="Hi, my name is Gary, what's up?")
    print(output)
    conversation_with_summary.predict(input="who is my favorite musician?")
    print(output)
    conversation_with_summary.predict(input="Whats my favorite dessert?")
    print(output)
    output = conversation_with_summary.predict(input="What's my name?")
    print(output)

    
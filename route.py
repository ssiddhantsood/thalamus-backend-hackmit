import random 

import os

#LLM IMPORTS
from anthropic import Anthropic
import google.generativeai as genai
import openai
import anthropic
import paramiko
import logger
import time

from huggingface_hub import InferenceClient
from ollama import Client
from .thalamus import find_llm

def find_ssh_key():
    possible_key_names = ['id_rsa', 'id_ed25519', 'id_ecdsa', 'id_dsa']
    home_dir = os.path.expanduser('~')
    ssh_dir = os.path.join(home_dir, '.ssh')
    
    for key_name in possible_key_names:
        key_path = os.path.join(ssh_dir, key_name)
        if os.path.isfile(key_path):
            print(f"Found SSH key: {key_path}")
            return key_path

    return None

def ssh_ml_query(query, modal):

    # SSH connection details
    target_host = ""

    if modal == "mistral":
        target_host = "100.81.81.162"
    else:
        target_host = '100.81.81.96'

    jump_host = '146.152.232.8'
    jump_user = 'guest'

    target_user = 'ubuntu'
    
    # Find SSH key
    key_path = find_ssh_key()
    if not key_path:
        return "Error: No SSH key found"

    # Create a new SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Load the private key
        private_key = paramiko.RSAKey.from_private_key_file(key_path)
        
        jump_client = paramiko.SSHClient()
        jump_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        jump_client.connect(jump_host, username=jump_user, pkey=private_key)
        
        jump_transport = jump_client.get_transport()
        dest_addr = (target_host, 22)
        local_addr = ('', 0)
        jump_channel = jump_transport.open_channel("direct-tcpip", dest_addr, local_addr)
       
        ssh.connect(target_host, username=target_user, sock=jump_channel, pkey=private_key)
       
        if modal == "mistral": command = f'ollama run mistral "{query}"'
        else: command = f'ollama run llama3.1 "{query}"'
    
        # Open a session
        session = ssh.get_transport().open_session()
        session.get_pty()
        session.exec_command(command)

        # Read the output
        output = ""
        while True:
            if session.recv_ready():
                chunk = session.recv(4096).decode('utf-8')
                yield chunk
            if session.exit_status_ready():
                break
            time.sleep(0.1)


        # Check if there's any error
        if session.recv_stderr_ready():
            error = session.recv_stderr(4096).decode('utf-8')
            return f"Error: {error}"

        return output


    except Exception as e:
  
        return f"An error occurred: {str(e)}"

    finally:
     
        ssh.close()
        jump_client.close()

#Route Query through the Phi 3 Router, Return Either Agent Template or LLM Model
def route_query(query):

    model = find_llm(query)
    final_response = ""
    print(model)
    
    if "gpt" in model:
        print('1')
        
        client = openai.OpenAI()

        stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": query}],
        stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield(chunk.choices[0].delta.content)

    if "claude" in model or "gemini" in model:
        print('2')
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        with client.messages.stream(
            model="claude-3-opus-20240229",
            max_tokens=2000,
            messages=[
            {"role": "user", "content": query}
            ]
        ) as stream:
            for text in stream.text_stream:
                yield text
    if "gemini" in model:
        print('3')
        genai.configure(api_key=os.environ["API_KEY"])
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Introduce yourself", stream=True)

    if "llama" in model:
        print('4')
        for chunk in ssh_ml_query(query,"llama"):
            yield chunk
    if "mistral" in model:
        for chunk in ssh_ml_query(query,"mistral"):
            yield chunk
        
    return final_response

#Testing Purposes
def main():
    query = "What Large Language Model are you"
    for chunk in route_query(query):
        print(chunk, end='', flush=True)
    print() 
    
    
if __name__ == "__main__":
    main()
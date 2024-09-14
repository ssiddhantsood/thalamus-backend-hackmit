import random 

#Route Query through the Phi 3 Router, Return Either Agent Template or LLM Model
def route_query(query):
    paths = ["gpt", "claude", "research agent"]
    return random.choice(paths)

#Testing Purposes
def main():
    print(route_query("blah blah"))
    
    
if __name__ == "__main__":
    main()
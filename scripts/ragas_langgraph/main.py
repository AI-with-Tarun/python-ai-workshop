import requests

"""
from state import graph_builder
import warnings
warnings.filterwarnings("ignore")
if __name__ == "__main__":
    while True:
        user_prompt = input("Enter your query:(quit or q to exit)")
        if user_prompt.lower() == "quit" or user_prompt.lower == "q":
            print("Thank you for using our service")
            break
        else:
            graph = graph_builder()
            response = graph.invoke({"query":user_prompt})
            print(response['answer'])"""

URL = "http://127.0.0.1:8000/rag"
query = "contact to mail Atyantik"
payload = {"query": query}
response = requests.post(URL, json=payload)
print(response.json())

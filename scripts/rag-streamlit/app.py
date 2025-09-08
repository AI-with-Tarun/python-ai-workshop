from langgraph.graph import StateGraph # node and edges logic
from langgraph.graph import START,END # start node and what is the end node
from typing import TypedDict, List,Dict
import os
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from prompts import SYSTEM_PROMPT, USER_PROMPT
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st

os.environ['GOOGLE_API_KEY'] = st.secrets['GOOGLE_API_KEY']
url = st.secrets['QDRANT_URL']
api_key = st.secrets['QDRANT_API_KEY']

embeddings = FastEmbedEmbeddings(model_name = "jinaai/jina-embeddings-v2-base-en")
client = QdrantClient(
    url = url,
    api_key=api_key,
)
collection_name = "webpages"

class RAGState(TypedDict):
    query: str
    context: List[str]
    answer: str

def search(state: RAGState) -> RAGState:
    db = QdrantVectorStore(
        client=client,
        collection_name=collection_name, # 768
        embedding = embeddings
    )
    retriever = db.as_retriever(search_type="mmr",
                                search_kwargs={"k":3})
    relevant_docs = retriever.invoke(state['query']) 
    context = []
    for doc in relevant_docs:
        context.append(doc.page_content)
    state['context'] = context 
    return state

def answer(state: RAGState) -> RAGState:
    context = " ".join(state['context']) # converting list to str
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro",
                                temperature=0.0,max_tokens=None)
    prompt_template = ChatPromptTemplate(
        messages = [
            ("system",SYSTEM_PROMPT),
            ("user",USER_PROMPT.format(context=context,
                                        query=state['query']))
        ],
    )
    answer = llm.invoke(prompt_template.format_messages())
    state['answer'] = answer.content
    return state

st.title("Atyantik Chatbot")
st.subheader("Chat with webpage")

if "messages" not in st.session_state:
   st.session_state.messages = []

workflow = StateGraph(RAGState) 
workflow.add_node("search_context",search)
workflow.add_node("answer_generation",answer)
workflow.add_edge(START,"search_context")
workflow.add_edge("search_context","answer_generation")
workflow.add_edge("answer_generation",END)
graph = workflow.compile()

if "messages" not in st.session_state:
   st.session_state.messages = []


with st.container():
   for message in st.session_state.messages:
       with st.chat_message(message["role"]):
           st.write(message["content"])


if prompt := st.chat_input("Ask about Atyantik..."):
   st.session_state.messages.append({"role": "user", "content": prompt})
  
   with st.chat_message("user"):
       st.write(prompt)
  
   with st.chat_message("assistant"):
       with st.spinner("Thinking..."):
           try:
               result = graph.stream({
                   "query": prompt,
               })
              
               response = result["answer"]
               st.write(response)
              
               st.session_state.messages.append({"role": "assistant", "content": response})
              
           except Exception as e:
               error_msg = f"Sorry, I encountered an error: {str(e)}"
               st.error(error_msg)
               st.session_state.messages.append({"role": "assistant", "content": error_msg})


if st.session_state.messages:
   if st.sidebar.button("Clear Chat", type="secondary"):
       st.session_state.messages = []
       st.rerun()
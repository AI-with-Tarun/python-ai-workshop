from typing import TypedDict, List

from client import LLMClient,EmbeddingClient
from config import configure

from qdrant_client import models, QdrantClient
from langgraph.graph import StateGraph
from langgraph.graph import START,END

class RAGState(TypedDict):
    query: str
    context: List[str]
    answer: str

def search(state: RAGState):
  client = QdrantClient(
    url = configure.QDRANT_URL,
    api_key = configure.QDRANT_API_KEY
  )
  embedding_client = EmbeddingClient()
  dense_vectors = next(embedding_client.query_embed_dense(state['query']))
  sparse_vectors = next(embedding_client.query_embed_sparse(state['query']))

  prefetch = [
    models.Prefetch(
        query = dense_vectors,
        using = "dense", # vector search
        limit = 15
    ),
    models.Prefetch(
        query = models.SparseVector(**sparse_vectors.as_object()),
        using = "sparse",
        limit = 15
    )]

  relevant_docs = client.query_points(
    collection_name = configure.COLLECTION_NAME,
    prefetch = prefetch,
    query = dense_vectors,
    using = "dense",
    with_payload=True,
    limit = 3,
    )

  context = [] # List[str]
  for info in relevant_docs.points:
    context.append(info.payload['document'])

  return {"context":context}

def answer(state: RAGState):
    client = LLMClient()
    context = " ".join(state['context']) 

    prompt = f"""You are an seasoned support staff working at Atyantik, based on the given CONTEXT as the only source of information answer the user QUESTION.
    If user QUESTION is not from the CONTEXT, just say: I dont know , not enough information provided

    <context>
    CONTEXT: {context}
    </context
    <question>
    Question: {state['query']}
    </question>
    """
    answer = client.get_response(prompt)

    return {"answer":answer}

def graph_builder():
   workflow = StateGraph(RAGState)

   workflow.add_node("search",search)
   workflow.add_node("answer",answer)
   workflow.add_edge(START,"search")
   workflow.add_edge("search","answer")
   workflow.add_edge("answer",END)

   graph = workflow.compile()
   return graph
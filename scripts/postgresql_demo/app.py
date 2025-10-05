from langchain_postgres import PGVector
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

USERNAME = "tarunjain"  
PASSWORD = "TRJEnter#456"
HOST = "localhost"
PORT = "5432" 
DATABASE = "vectordb" 

collection_name = "docs"
CONNECTION_STRING = f"postgresql+psycopg://{USERNAME}@{HOST}:{PORT}/{DATABASE}"
embeddings = FastEmbedEmbeddings(model_name = "jinaai/jina-embeddings-v2-base-en") 


vector_store = PGVector(
    embeddings=embeddings,
    collection_name=collection_name,
    connection=CONNECTION_STRING,
    use_jsonb=True,
)

query = "What is the code of conduct for PostgreSQL?"
print(vector_store.max_marginal_relevance_search(query,k=3))

retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 3})
print(retriever.invoke(query))
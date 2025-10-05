# pip install langchain-community bs4 fastembed langchain-postgres

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_postgres import PGVector

USERNAME = "tarunjain"  
PASSWORD = "TRJEnter#456"
HOST = "localhost"
PORT = "5432" 
DATABASE = "vectordb" 

urls = [
   "https://www.postgresql.org/about/",
   "https://www.postgresql.org/about/policies/trademarks/",
   "https://www.postgresql.org/about/policies/privacy/",
   "https://www.postgresql.org/about/policies/coc/"
]

print("Loading documents...")
loader = WebBaseLoader(urls)
documents = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=2048, chunk_overlap=0)
docs = splitter.split_documents(documents)

collection_name = "docs"
CONNECTION_STRING = f"postgresql+psycopg://{USERNAME}@{HOST}:{PORT}/{DATABASE}"
embeddings = FastEmbedEmbeddings(model_name = "jinaai/jina-embeddings-v2-base-en") 

print("Creating vector store...")
vector_store = PGVector(
    embeddings=embeddings,
    collection_name=collection_name,
    connection=CONNECTION_STRING,
    use_jsonb=True,
)
vector_store.add_documents(docs)

retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 3})
print(retriever.invoke("What is the code of conduct for PostgreSQL?"))
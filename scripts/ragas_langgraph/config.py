from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Configure(BaseModel):
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    MODEL_NAME: str = "gemini-2.5-flash"
    TEMPERATURE: float = os.getenv("TEMPERATURE", 0.0)
    MAX_TOKENS: int = None

    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY",None)
    QDRANT_URL: str = os.getenv("QDRANT_URL")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", None)

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY") # evals
    DENSE_EMBEDDING_MODEL: str = "jinaai/jina-embeddings-v2-base-en"
    SPARSE_EMBEDDING_MODEL: str = "Qdrant/BM25"
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

configure = Configure()
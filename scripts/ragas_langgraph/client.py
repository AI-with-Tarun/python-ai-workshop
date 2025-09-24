from config import configure
from langchain_google_genai import ChatGoogleGenerativeAI
from fastembed import TextEmbedding, SparseTextEmbedding

class LLMClient:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model = configure.MODEL_NAME,
            temperature = configure.TEMPERATURE,
            max_tokens = configure.MAX_TOKENS,
        )
    def get_response(self,prompt:str):
        response = self.llm.invoke(prompt)
        return response.content

class EmbeddingClient:
    def __init__(self):
        self.dense_model = TextEmbedding(model_name = configure.DENSE_EMBEDDING_MODEL)
        self.sparse_model = SparseTextEmbedding(configure.SPARSE_EMBEDDING_MODEL)

    def query_embed_dense(self,query: str):
        yield next(self.dense_model.query_embed(query))
    
    def query_embed_sparse(self,query: str):
        yield next(self.sparse_model.query_embed(query))
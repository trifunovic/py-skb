from sentence_transformers import SentenceTransformer
from langchain_community.embeddings import OpenAIEmbeddings
from src.config import config


class EmbeddingService:
    def __init__(self):
        self.model_type = config.model_type

        if self.model_type == "openai":
            self.model_name = config.openai_embedding_model
            self.model = OpenAIEmbeddings(model=self.model_name)
            self.dimensions = 1536 if "3-small" in self.model_name else 3072
        elif self.model_type == "sentence-transformers":
            self.model_name = config.model_name
            self.model = SentenceTransformer(self.model_name)
            self.dimensions = self.get_model_dimensions()
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")

    def get_model_dimensions(self):
        dummy_input = "test"
        embedding = self.model.encode(dummy_input, convert_to_tensor=True)
        return embedding.shape[-1]

    def embed(self, content: str):
        if self.model_type == "openai":
            return self.model.embed_query(content)
        return self.model.encode(content, convert_to_tensor=False).tolist()

    def embed_query(self, content: str):
        # ✅ LangChain expects this method name
        return self.embed(content)


# ✅ instanca za import
embedding_service = EmbeddingService()

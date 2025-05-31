from sentence_transformers import SentenceTransformer, util
from langchain.embeddings import OpenAIEmbeddings
from src.config import config

class EmbeddingService:
    def __init__(self):
        self.model_type = config.model_type

        if self.model_type == "openai":
            self.model_name = config.openai_embedding_model
            self.model = OpenAIEmbeddings(model=self.model_name)
            self.dimensions = 1536 if "3-small" in self.model_name else 3072  # možeš da proširiš ako bude više
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

    def generate_embedding(self, content: str):
        if self.model_type == "openai":
            return self.model.embed_query(content)
        return self.model.encode(content, convert_to_tensor=True).tolist()

    def embed(self, content: str):
        return self.generate_embedding(content)

    def extract_semantically_relevant_answer(self, content: str, query: str):
        if self.model_type != "sentence-transformers":
            raise NotImplementedError("This method only works with sentence-transformers.")

        sentences = content.split(". ")
        if not sentences:
            return "No relevant content found."

        query_embedding = self.model.encode(query, convert_to_tensor=True)
        sentence_embeddings = self.model.encode(sentences, convert_to_tensor=True)
        similarities = util.pytorch_cos_sim(query_embedding, sentence_embeddings)
        most_similar_idx = similarities.argmax().item()

        return sentences[most_similar_idx].strip()

    def refine_answer_based_on_query(self, query: str, answer: str):
        query_lower = query.lower()
        if "who" in query_lower and "coolest kid" in query_lower:
            return answer.split(" ")[0] if answer else "No answer found."
        elif "why" in query_lower:
            return answer.split("because")[-1].strip() if "because" in answer else answer
        return answer

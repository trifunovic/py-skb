from sentence_transformers import SentenceTransformer, util

class EmbeddingService:
    def __init__(self):
        """
        Initialize the EmbeddingService with a hardcoded model.
        """
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.dimensions = self.get_model_dimensions()

    def get_model_dimensions(self):
        """
        Get the output dimensions of the SentenceTransformer model.
        """
        dummy_input = "test"
        embedding = self.model.encode(dummy_input, convert_to_tensor=True)
        return embedding.shape[-1]

    def generate_embedding(self, content: str):
        """
        Generate embeddings for the given content.
        """
        return self.model.encode(content, convert_to_tensor=True)

    def extract_semantically_relevant_answer(self, content: str, query: str):
        """
        Extract the most semantically relevant sentence from the content.
        """
        sentences = content.split(". ")
        if not sentences:
            return "No relevant content found."

        query_embedding = self.generate_embedding(query)
        sentence_embeddings = self.generate_embedding(sentences)
        similarities = util.pytorch_cos_sim(query_embedding, sentence_embeddings)
        most_similar_idx = similarities.argmax().item()

        return sentences[most_similar_idx].strip()

    def refine_answer_based_on_query(self, query: str, answer: str):
        """
        Refine the extracted answer based on specific query types.
        """
        query_lower = query.lower()
        if "who" in query_lower and "coolest kid" in query_lower:
            return answer.split(" ")[0] if answer else "No answer found."
        elif "why" in query_lower:
            return answer.split("because")[-1].strip() if "because" in answer else answer
        return answer

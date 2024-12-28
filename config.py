from services.secrets_service import SecretsService
import os

class Config:
    # Pinecone-specific constants

    def __init__(self):
        # Use SecretsService for production and fallback to environment variables for local
        self._secrets_service = SecretsService(key_vault_name=os.getenv("KEY_VAULT_NAME", None))

    def _get_secret(self, secret_name, fallback_env):
        """
        Retrieve a secret using SecretsService with fallback to environment variables.
        """
        try:
            return self._secrets_service.get_secret(secret_name, fallback_env=fallback_env)
        except RuntimeError:
            # Fallback for local development
            return os.getenv(fallback_env)

    @property
    def pinecone_api_key(self):
        return self._get_secret("pinecone-api-key", fallback_env="PINECONE_API_KEY")
    
    @property
    def pinecone_index_name(self):
        return self._get_secret("pinecone-api-key", fallback_env="PINECONE_INDEX_NAME")

    @property
    def openai_api_key(self):
        return self._get_secret("openai-api-key", fallback_env="OPENAI_API_KEY")

    @property
    def knowledge_api_key(self):
        return self._get_secret("knowledge-api-key", fallback_env="KNOWLEDGE_API_KEY")

    @property
    def redis_host(self):
        # Redis hostname can also vary between environments
        return os.getenv("REDIS_HOST", "localhost")

    @property
    def allowed_origins(self):
        # Retrieve allowed origins from environment or set defaults
        return os.getenv("ALLOWED_ORIGINS", "http://localhost:8080").split(",")
    
    @property
    def pinecone_index_name(self):
        return os.getenv("PINECONE_INDEX_NAME", "default-index")

    @property
    def pinecone_metric(self):
        return os.getenv("PINECONE_METRIC", "cosine")
    
    @property
    def pinecone_cloud(self):
        return os.getenv("PINECONE_CLOUD", "aws")

    @property
    def pinecone_region(self):
        return os.getenv("PINECONE_REGION", "us-east-1")
    
    @property
    def openai_model(self):
        # Currently unused; kept for future OpenAI integration
        return os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    @property
    def model_name(self):
        # Currently unused; kept for potential multi-model support
        return os.getenv("MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
    
    @property
    def model_type(self):
        # Currently unused; kept for potential multi-model type support
        return os.getenv("MODEL_TYPE", "sentence-transformers")


config = Config()

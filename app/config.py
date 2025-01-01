from app.services.secrets_service import SecretsService
import os

class Config:
    """
    Configuration class for managing application settings.
    Retrieves secrets from Azure Key Vault or falls back to environment variables.
    """

    def __init__(self):
        self._key_vault_name = os.getenv("AZURE_KEY_VAULT_NAME", None)
        self._secrets_service = SecretsService(key_vault_name=self._key_vault_name)

    def _get_secret(self, secret_name, fallback_env):
        """
        Retrieve a secret from SecretsService with fallback to environment variables.

        Args:
            secret_name (str): The name of the secret in Key Vault.
            fallback_env (str): The name of the environment variable to use as a fallback.

        Returns:
            str: The value of the secret or the fallback value.
        """
        try:
            secret = self._secrets_service.get_secret(secret_name, fallback_env=fallback_env)
            if secret:
                print(f"Retrieved {secret_name} from SecretsService.")
                return secret
        except RuntimeError as e:
            print(f"SecretsService error for {secret_name}: {e}. Falling back to {fallback_env}.")

        env_value = os.getenv(fallback_env)
        if env_value:
            print(f"Retrieved {fallback_env} from environment variables.")
        else:
            print(f"Failed to retrieve {fallback_env}. Using default value if defined.")
        
        return env_value

    @property
    def pinecone_api_key(self):
        return self._get_secret("pinecone-api-key", fallback_env="PINECONE_API_KEY")

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
    def openai_api_key(self):
        return self._get_secret("openai-api-key", fallback_env="OPENAI_API_KEY")

    @property
    def knowledge_api_key(self):
        return self._get_secret("knowledge-api-key", fallback_env="KNOWLEDGE_API_KEY")

    @property
    def redis_host(self):
        return os.getenv("REDIS_HOST", "localhost")

    @property
    def allowed_origins(self):
        allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8080")
        return allowed_origins.split(",")

    @property
    def openai_model(self):
        return os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    @property
    def model_name(self):
        return os.getenv("MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")

    @property
    def model_type(self):
        return os.getenv("MODEL_TYPE", "sentence-transformers")

    @property
    def debug_mode(self):
        return os.getenv("DEBUG", "False").lower() in ["true", "1", "yes"]

    @property
    def log_level(self):
        return os.getenv("LOG_LEVEL", "info")


config = Config()

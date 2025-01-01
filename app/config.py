from app.services.secrets_service import SecretsService
import os

class Config:
    """
    Configuration class for managing application settings.
    Retrieves secrets from Azure Key Vault or falls back to environment variables.
    """

    def __init__(self):
        self._key_vault_name = os.getenv("AZURE_KEY_VAULT_NAME")
        self._secrets_service = SecretsService(key_vault_name=self._key_vault_name) if self._key_vault_name else None

    def _get_secret(self, secret_name, fallback_env, default=None):
        """
        Retrieve a secret from SecretsService with fallback to environment variables.

        Args:
            secret_name (str): The name of the secret in Key Vault.
            fallback_env (str): The name of the environment variable to use as a fallback.
            default (Any): The default value if neither Key Vault nor environment variables provide the value.

        Returns:
            str: The value of the secret, fallback value, or default.
        """
        # Attempt to retrieve from Key Vault
        if self._secrets_service:
            try:
                secret = self._secrets_service.get_secret(secret_name, fallback_env=fallback_env)
                if secret:
                    print(f"Retrieved {secret_name} from SecretsService.")
                    return secret
            except RuntimeError as e:
                print(f"SecretsService error for {secret_name}: {e}. Falling back to {fallback_env}.")

        # Fallback to environment variables
        env_value = os.getenv(fallback_env, default)
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
        return self._get_secret("pinecone-index-name", fallback_env="PINECONE_INDEX_NAME", default="default-index")

    @property
    def pinecone_metric(self):
        return self._get_secret("pinecone-metric", fallback_env="PINECONE_METRIC", default="cosine")

    @property
    def pinecone_cloud(self):
        return self._get_secret("pinecone-cloud", fallback_env="PINECONE_CLOUD", default="aws")

    @property
    def pinecone_region(self):
        return self._get_secret("pinecone-region", fallback_env="PINECONE_REGION", default="us-east-1")

    @property
    def openai_api_key(self):
        return self._get_secret("openai-api-key", fallback_env="OPENAI_API_KEY")

    @property
    def knowledge_api_key(self):
        return self._get_secret("knowledge-api-key", fallback_env="KNOWLEDGE_API_KEY")

    @property
    def redis_host(self):
        return self._get_secret("redis-host", fallback_env="REDIS_HOST", default="localhost")

    @property
    def allowed_origins(self):
        allowed_origins = self._get_secret("allowed-origins", fallback_env="ALLOWED_ORIGINS", default="http://localhost:8080")
        return allowed_origins.split(",")

    @property
    def openai_model(self):
        return self._get_secret("openai-model", fallback_env="OPENAI_MODEL", default="gpt-3.5-turbo")

    @property
    def model_name(self):
        return self._get_secret("model-name", fallback_env="MODEL_NAME", default="sentence-transformers/all-MiniLM-L6-v2")

    @property
    def model_type(self):
        return self._get_secret("model-type", fallback_env="MODEL_TYPE", default="sentence-transformers")

    @property
    def debug_mode(self):
        return self._get_secret("debug", fallback_env="DEBUG", default="False").lower() in ["true", "1", "yes"]

    @property
    def log_level(self):
        return self._get_secret("log-level", fallback_env="LOG_LEVEL", default="info")

config = Config()

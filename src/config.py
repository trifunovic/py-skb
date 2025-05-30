from src.services.secrets_service import SecretsService
import os

class Config:
    def __init__(self):
        self._key_vault_name = os.getenv("AZURE_KEY_VAULT_NAME")
        self._secrets_service = SecretsService(key_vault_name=self._key_vault_name) if self._key_vault_name else None

    def _get_secret(self, secret_name, fallback_env, default=None):
        if self._secrets_service:
            try:
                secret = self._secrets_service.get_secret(secret_name, fallback_env=fallback_env)
                if secret:
                    print(f"Retrieved {secret_name} from Key Vault.")
                    return secret
            except RuntimeError as e:
                print(f"Key Vault error for {secret_name}: {e}. Falling back to {fallback_env}.")

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
    def pinecone_namespace(self):
        return self._get_secret("pinecone-namespace", fallback_env="PINECONE_NAMESPACE", default="default")

    @property
    def openai_api_key(self):
        return self._get_secret("openai-api-key", fallback_env="OPENAI_API_KEY")

    @property
    def openai_model(self):
        return self._get_secret("openai-model", fallback_env="OPENAI_MODEL", default="gpt-3.5-turbo")

    @property
    def knowledge_api_key(self):
        return self._get_secret("knowledge-api-key", fallback_env="KNOWLEDGE_API_KEY")

    @property
    def redis_host(self):
        return self._get_secret("redis-host", fallback_env="REDIS_HOST", default="redis")

    @property
    def redis_port(self):
        return self._get_secret("redis-port", fallback_env="REDIS_PORT", default="6379")

    @property
    def redis_use_ssl(self):
        return self._get_secret("redis-use-ssl", fallback_env="REDIS_USE_SSL", default="False").lower() in ["true", "1", "yes"]

    @property
    def redis_access_key(self):
        return self._get_secret("redis-access-key", fallback_env="REDIS_ACCESS_KEY", default=None)

    @property
    def allowed_origins(self):
        allowed_origins = self._get_secret("allowed-origins", fallback_env="ALLOWED_ORIGINS", default="*")
        return allowed_origins.split(",")

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

    @property
    def app_port(self):
        return int(self._get_secret("app-port", fallback_env="APP_PORT", default="8000"))

    @property
    def search_rate_limit(self):
        return int(self._get_secret("search-rate-limit", fallback_env="SEARCH_RATE_LIMIT", default="10"))

    @property
    def rate_limit_window_seconds(self):
        return int(self._get_secret("rate-limit-window-seconds", fallback_env="RATE_LIMIT_WINDOW_SECONDS", default="60"))

    @property
    def search_top_k(self):
        return int(self._get_secret("search-top-k", fallback_env="SEARCH_TOP_K", default="5"))

    @property
    def backend_version(self):
        try:
            version_file = os.path.join(os.path.dirname(__file__), "backend_version.txt")
            with open(version_file, "r") as f:
                return f.read().strip()
        except Exception as e:
            print(f"⚠️ Failed to read version file: {e}")
            return "0.0.0"

    def print_config(self):
        print("\n==================== Loaded Configuration ======================")
        print(f"APP Port: {self.app_port}")
        print(f"Azure Key Vault Name: {self._key_vault_name or 'Not Set'}")
        print(f"Redis Host: {self.redis_host}")
        print(f"Redis Port: {self.redis_port}")
        print(f"Redis Access Key (masked): {'*' * len(self.redis_access_key) if self.redis_access_key else 'Not Set'}")
        print(f"Pinecone API Key (masked): {'*' * len(self.pinecone_api_key) if self.pinecone_api_key else 'Not Set'}")
        print(f"Pinecone Index Name: {self.pinecone_index_name}")
        print(f"Pinecone Metric: {self.pinecone_metric}")
        print(f"Pinecone Cloud: {self.pinecone_cloud}")
        print(f"Pinecone Region: {self.pinecone_region}")
        print(f"Pinecone Namesapce: {self.pinecone_namespace}")
        print(f"OpenAI API Key (masked): {'*' * len(self.openai_api_key) if self.openai_api_key else 'Not Set'}")
        print(f"OpenAI Model: {self.openai_model}")
        print(f"Knowledge API Key (masked): {'*' * len(self.knowledge_api_key) if self.knowledge_api_key else 'Not Set'}")
        print(f"Allowed Origins: {self.allowed_origins}")
        print(f"Model Name: {self.model_name}")
        print(f"Model Type: {self.model_type}")
        print(f"Debug Mode: {self.debug_mode}")
        print(f"Log Level: {self.log_level}")
        print(f"Search Rate Limit: {self.search_rate_limit} requests per {self.rate_limit_window_seconds} seconds")
        print(f"BE version: {self.backend_version}")
        print("================================================================\n")

config = Config()

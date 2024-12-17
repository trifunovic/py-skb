from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
import threading


class SecretsService:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, key_vault_name=None):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self, key_vault_name=None):
        if self._initialized:
            return
        self.key_vault_name = key_vault_name or os.getenv("KEY_VAULT_NAME")
        
        if self.key_vault_name:
            self.key_vault_url = f"https://{self.key_vault_name}.vault.azure.net/"
            self.credential = DefaultAzureCredential()
            self.client = SecretClient(vault_url=self.key_vault_url, credential=self.credential)
        else:
            # If no Key Vault name is provided, fallback to environment variables only
            self.client = None
        self._initialized = True

    def get_secret(self, secret_name, fallback_env=None):
        """
        Retrieve a secret from Azure Key Vault or an environment variable as a fallback.

        :param secret_name: Name of the secret in Azure Key Vault.
        :param fallback_env: Name of the environment variable to use as a fallback.
        :return: The value of the secret or fallback value if available, otherwise None.
        """
        if self.client:
            try:
                secret = self.client.get_secret(secret_name)
                if secret and secret.value:
                    return secret.value
            except Exception as e:
                # Log or handle exceptions as needed (e.g., secret not found, access denied)
                pass

        # Fallback to environment variable if Key Vault is unavailable or secret is not found
        return os.getenv(fallback_env) if fallback_env else None

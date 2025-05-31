# src/utils/print_config.py

def print_config(config, embedding_service=None):
    print("\n==================== Loaded Configuration ======================")
    print(f"APP Port: {config.app_port}")
    print(f"Azure Key Vault Name: {config._key_vault_name or 'Not Set'}")
    print(f"Redis Host: {config.redis_host}")
    print(f"Redis Port: {config.redis_port}")
    print(f"Redis Access Key (masked): {'*' * len(config.redis_access_key) if config.redis_access_key else 'Not Set'}")
    print(f"Pinecone API Key (masked): {'*' * len(config.pinecone_api_key) if config.pinecone_api_key else 'Not Set'}")
    print(f"Pinecone Index Name: {config.pinecone_index_name}")
    print(f"Pinecone Metric: {config.pinecone_metric}")
    print(f"Pinecone Cloud: {config.pinecone_cloud}")
    print(f"Pinecone Region: {config.pinecone_region}")
    print(f"Pinecone Namesapce: {config.pinecone_namespace}")
    print(f"OpenAI API Key (masked): {'*' * len(config.openai_api_key) if config.openai_api_key else 'Not Set'}")
    print(f"OpenAI Model: {config.openai_model}")
    print(f"Knowledge API Key (masked): {'*' * len(config.knowledge_api_key) if config.knowledge_api_key else 'Not Set'}")
    print(f"Allowed Origins: {config.allowed_origins}")
    print(f"Model Name: {config.model_name}")
    print(f"Model Type: {config.model_type}")

    if embedding_service:
        print(f"Embedding Model Type: {embedding_service.model_type}")
        print(f"Embedding Model Name: {embedding_service.model_name}")
        print(f"Embedding Dimensions: {embedding_service.dimensions}")

    print(f"Debug Mode: {config.debug_mode}")
    print(f"Log Level: {config.log_level}")
    print(f"Search Rate Limit: {config.search_rate_limit} requests per {config.rate_limit_window_seconds} seconds")
    print(f"BE version: {config.backend_version}")
    print("================================================================\n")

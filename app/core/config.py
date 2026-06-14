from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    azure_search_endpoint: str = ""
    azure_search_api_key: str = ""
    azure_search_index_name: str = "trading-knowledge"

    azure_openai_endpoint: str = ""
    azure_openai_api_key: str = ""
    azure_openai_chat_deployment: str = "gpt-4o"
    azure_openai_embedding_deployment: str = "text-embedding-3-large"
    azure_openai_api_version: str = "2024-08-01-preview"

    azure_storage_connection_string: str = ""
    azure_storage_container: str = "trading-documents"

    max_chunk_size: int = 1000
    chunk_overlap: int = 100
    search_top_k: int = 5

    class Config:
        env_file = ".env"


settings = Settings()

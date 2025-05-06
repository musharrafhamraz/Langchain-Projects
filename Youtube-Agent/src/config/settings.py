from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    GROQ_API_KEY: str = Field(..., env="GROQ_API_KEY")
    EMBEDDING_MODEL: str = "sentence-transformers/all-mpnet-base-v2"
    LLM_MODEL: str = "llama-3-70b-8192"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    class Config:
        env_file = ".env"

settings = Settings()
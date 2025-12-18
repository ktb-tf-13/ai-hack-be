from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path
from typing import Optional

class Settings(BaseSettings):
    # Server configs
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    server_reload: bool = True
    
    # DB connection
    db_user: str = Field(default="user", alias="DB_USER")
    db_password: str = Field(default="user", alias="DB_PASSWORD")
    db_host: str = Field(default="localhost", alias="DB_HOST")
    db_port: int = Field(default=3306, alias="DB_PORT")
    db_name: str = Field(default="backend", alias="DB_NAME")
    
    # LLM
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")

    db_url: Optional[str] = None 

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8"
    )

settings = Settings()
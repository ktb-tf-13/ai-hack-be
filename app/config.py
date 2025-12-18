from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    # Server configs
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    server_reload: bool = True

    # Model configs
    model_path: str = "models/simple_model.pt"
    model_device: str = "cpu"

    # DB configs
    db_type: str = "csv"
    csv_data_path: str = "temp_table"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

# Backward compatibility for existing code that expects dictionaries
server_config = {
    "host": settings.server_host,
    "port": settings.server_port,
    "reload": settings.server_reload
}

model_config = {
    "path": settings.model_path,
    "device": settings.model_device
}

# Other variables
db_type = settings.db_type
csv_data_path = Path(__file__).parent.parent / settings.csv_data_path

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Short Drama Studio"
    env: str = "local"
    database_url: str = "sqlite:///./data/studio.db"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:8000"
    mock_when_no_key: bool = True

    openai_api_key: str | None = None
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4.1-mini"

    xai_api_key: str | None = None
    xai_base_url: str = "https://api.x.ai/v1"
    xai_model: str = "grok-3-mini"

    siliconflow_api_key: str | None = None
    siliconflow_base_url: str = "https://api.siliconflow.cn/v1"
    siliconflow_model: str = "Qwen/Qwen2.5-72B-Instruct"

    deepseek_api_key: str | None = None
    deepseek_base_url: str = "https://api.deepseek.com/v1"
    deepseek_model: str = "deepseek-chat"

    openrouter_api_key: str | None = None
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "anthropic/claude-3.5-sonnet"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

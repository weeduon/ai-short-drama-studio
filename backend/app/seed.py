from sqlalchemy.orm import Session
from .models import ModelProvider

DEFAULT_MODELS = [
    {"name": "OpenAI", "base_url": "https://api.openai.com/v1", "api_key_env": "OPENAI_API_KEY", "model_name": "gpt-4.1-mini", "purpose": "writing", "is_default": True},
    {"name": "Grok / xAI", "base_url": "https://api.x.ai/v1", "api_key_env": "XAI_API_KEY", "model_name": "grok-3-mini", "purpose": "review"},
    {"name": "SiliconFlow", "base_url": "https://api.siliconflow.cn/v1", "api_key_env": "SILICONFLOW_API_KEY", "model_name": "Qwen/Qwen2.5-72B-Instruct", "purpose": "writing"},
    {"name": "DeepSeek", "base_url": "https://api.deepseek.com/v1", "api_key_env": "DEEPSEEK_API_KEY", "model_name": "deepseek-chat", "purpose": "review"},
    {"name": "OpenRouter", "base_url": "https://openrouter.ai/api/v1", "api_key_env": "OPENROUTER_API_KEY", "model_name": "anthropic/claude-3.5-sonnet", "purpose": "review"},
]


def seed_defaults(db: Session):
    for item in DEFAULT_MODELS:
        if not db.query(ModelProvider).filter(ModelProvider.name == item["name"]).first():
            db.add(ModelProvider(provider_type="openai_compatible", enabled=True, **item))
    db.commit()

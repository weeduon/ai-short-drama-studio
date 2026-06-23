import json
import os
import re
from dataclasses import dataclass
from typing import Any
import httpx
from sqlalchemy.orm import Session
from ..config import get_settings
from ..models import ModelProvider

settings = get_settings()


@dataclass
class LLMConfig:
    name: str
    base_url: str
    api_key: str | None
    model_name: str
    provider_type: str = "openai_compatible"


def default_provider_configs() -> list[LLMConfig]:
    return [
        LLMConfig("OpenAI", settings.openai_base_url, settings.openai_api_key, settings.openai_model),
        LLMConfig("Grok / xAI", settings.xai_base_url, settings.xai_api_key, settings.xai_model),
        LLMConfig("SiliconFlow", settings.siliconflow_base_url, settings.siliconflow_api_key, settings.siliconflow_model),
        LLMConfig("DeepSeek", settings.deepseek_base_url, settings.deepseek_api_key, settings.deepseek_model),
        LLMConfig("OpenRouter", settings.openrouter_base_url, settings.openrouter_api_key, settings.openrouter_model),
    ]


def get_enabled_configs(db: Session | None = None) -> list[LLMConfig]:
    configs: list[LLMConfig] = []
    if db is not None:
        rows = db.query(ModelProvider).filter(ModelProvider.enabled == True).all()  # noqa: E712
        for row in rows:
            configs.append(
                LLMConfig(
                    name=row.name,
                    base_url=row.base_url,
                    api_key=os.getenv(row.api_key_env),
                    model_name=row.model_name,
                    provider_type=row.provider_type,
                )
            )
    if not configs:
        configs = default_provider_configs()
    return configs


def extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text).strip()
        text = re.sub(r"```$", "", text).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.S)
        if match:
            return json.loads(match.group(0))
    return {"raw": text}


async def call_openai_compatible(config: LLMConfig, messages: list[dict[str, str]], temperature: float = 0.7) -> str:
    if not config.api_key:
        raise RuntimeError(f"{config.name} 未配置 API Key")
    url = config.base_url.rstrip("/") + "/chat/completions"
    headers = {"Authorization": f"Bearer {config.api_key}", "Content-Type": "application/json"}
    payload = {"model": config.model_name, "messages": messages, "temperature": temperature}
    async with httpx.AsyncClient(timeout=90) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]


async def complete_json(
    messages: list[dict[str, str]],
    db: Session | None = None,
    preferred: str | None = None,
    fallback: dict[str, Any] | None = None,
    temperature: float = 0.7,
) -> dict[str, Any]:
    configs = get_enabled_configs(db)
    if preferred:
        configs = sorted(configs, key=lambda c: 0 if preferred.lower() in c.name.lower() else 1)

    errors: list[str] = []
    for cfg in configs:
        try:
            text = await call_openai_compatible(cfg, messages, temperature=temperature)
            result = extract_json(text)
            result["_model"] = cfg.name
            return result
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{cfg.name}: {exc}")

    if settings.mock_when_no_key and fallback is not None:
        fallback = dict(fallback)
        fallback["_model"] = "local-mock"
        fallback["_warnings"] = errors[:5]
        return fallback
    raise RuntimeError("所有模型调用失败：" + "; ".join(errors))

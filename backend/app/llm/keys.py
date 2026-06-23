import json
import os
from pathlib import Path

KEY_FILE = Path("data/model_keys.json")


def _read_all() -> dict[str, str]:
    if not KEY_FILE.exists():
        return {}
    try:
        return json.loads(KEY_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _write_all(data: dict[str, str]) -> None:
    KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
    KEY_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_keys_to_env() -> None:
    for name, value in _read_all().items():
        if value and name.isidentifier():
            os.environ.setdefault(name, value)


def resolve_api_key(env_name: str, provider_name: str | None = None) -> str | None:
    env_value = os.getenv(env_name)
    if env_value:
        return env_value
    data = _read_all()
    return data.get(env_name) or (data.get(provider_name) if provider_name else None)


def save_api_key(env_name: str, api_key: str, provider_name: str | None = None) -> None:
    data = _read_all()
    data[env_name] = api_key
    os.environ[env_name] = api_key
    if provider_name:
        data[provider_name] = api_key
    _write_all(data)


def has_api_key(env_name: str, provider_name: str | None = None) -> bool:
    return bool(resolve_api_key(env_name, provider_name))

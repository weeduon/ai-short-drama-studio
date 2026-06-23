from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..llm.keys import has_api_key, save_api_key
from ..llm.providers import LLMConfig, call_openai_compatible
from ..models import ModelProvider

router = APIRouter(prefix="/api/models", tags=["models"])


class ApiKeyPayload(BaseModel):
    api_key: str


class ModelProviderPayload(BaseModel):
    id: int | None = None
    name: str
    provider_type: str = "openai_compatible"
    base_url: str
    api_key_env: str
    model_name: str
    enabled: bool = True
    is_default: bool = False
    purpose: str = "writing"


def serialize(row: ModelProvider) -> dict:
    return {
        "id": row.id,
        "name": row.name,
        "provider_type": row.provider_type,
        "base_url": row.base_url,
        "api_key_env": row.api_key_env,
        "model_name": row.model_name,
        "enabled": row.enabled,
        "is_default": row.is_default,
        "purpose": row.purpose,
        "has_api_key": has_api_key(row.api_key_env, row.name),
        "created_at": row.created_at,
    }


@router.get("")
def list_models(db: Session = Depends(get_db)):
    rows = db.query(ModelProvider).order_by(ModelProvider.created_at.desc()).all()
    return [serialize(row) for row in rows]


@router.post("")
def upsert_model(payload: ModelProviderPayload, db: Session = Depends(get_db)):
    data = payload.model_dump(exclude={"id"})
    existing = db.get(ModelProvider, payload.id) if payload.id else None
    if not existing:
        existing = db.query(ModelProvider).filter(ModelProvider.name == payload.name).first()
    if existing:
        for key, value in data.items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        return serialize(existing)
    model = ModelProvider(**data)
    db.add(model)
    db.commit()
    db.refresh(model)
    return serialize(model)


@router.post("/{model_id}/secret")
def save_model_secret(model_id: int, payload: ApiKeyPayload, db: Session = Depends(get_db)):
    row = db.get(ModelProvider, model_id)
    if not row:
        raise HTTPException(status_code=404, detail="Model provider not found")
    key = payload.api_key.strip()
    if not key:
        raise HTTPException(status_code=400, detail="API key 不能为空")
    save_api_key(row.api_key_env, key, row.name)
    return {"ok": True, "id": row.id, "has_api_key": True}


@router.post("/{model_id}/test")
async def test_model(model_id: int, db: Session = Depends(get_db)):
    row = db.get(ModelProvider, model_id)
    if not row:
        raise HTTPException(status_code=404, detail="Model provider not found")
    cfg = LLMConfig(
        name=row.name,
        base_url=row.base_url,
        api_key=None,
        model_name=row.model_name,
        provider_type=row.provider_type,
    )
    from ..llm.keys import resolve_api_key
    cfg.api_key = resolve_api_key(row.api_key_env, row.name)
    text = await call_openai_compatible(cfg, [{"role": "user", "content": "请只回复 OK"}], temperature=0)
    return {"ok": True, "reply": text[:200]}

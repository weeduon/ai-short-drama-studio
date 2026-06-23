from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import ModelProvider
from ..schemas import ModelProviderCreate, ModelProviderOut

router = APIRouter(prefix="/api/models", tags=["models"])


@router.get("", response_model=list[ModelProviderOut])
def list_models(db: Session = Depends(get_db)):
    return db.query(ModelProvider).order_by(ModelProvider.created_at.desc()).all()


@router.post("", response_model=ModelProviderOut)
def upsert_model(payload: ModelProviderCreate, db: Session = Depends(get_db)):
    existing = db.query(ModelProvider).filter(ModelProvider.name == payload.name).first()
    if existing:
        for key, value in payload.model_dump().items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        return existing
    model = ModelProvider(**payload.model_dump())
    db.add(model)
    db.commit()
    db.refresh(model)
    return model

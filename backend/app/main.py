from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
from .database import Base, SessionLocal, engine
from .llm.keys import load_keys_to_env
from .routers import models, projects, review, roles, video
from .seed import seed_defaults

settings = get_settings()
load_keys_to_env()
Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    seed_defaults(db)

app = FastAPI(title=settings.app_name, version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router)
app.include_router(models.router)
app.include_router(roles.router)
app.include_router(review.router)
app.include_router(video.router)


@app.get("/health")
def health():
    return {"status": "ok", "app": settings.app_name, "env": settings.env}

from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    logline: str = Field(..., min_length=1)
    genre: str = "爽文短剧"
    audience: str = "抖音/快手/小红书泛娱乐用户"
    platform: str = "竖屏短剧"
    tone: str = "强反转、强情绪、网感抽象"


class ProjectOut(ProjectCreate):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ArtifactOut(BaseModel):
    id: int
    project_id: int
    stage: str
    role: str
    title: str
    content: dict[str, Any]
    score: dict[str, Any] | None = None
    created_at: datetime


class ModelProviderCreate(BaseModel):
    name: str
    provider_type: str = "openai_compatible"
    base_url: str
    api_key_env: str
    model_name: str
    enabled: bool = True
    is_default: bool = False
    purpose: str = "writing"


class ModelProviderOut(ModelProviderCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class WorkflowRunRequest(BaseModel):
    episode_count: int = Field(3, ge=1, le=80)
    target_minutes_per_episode: float = Field(1.2, ge=0.3, le=10)
    use_cross_review: bool = True
    max_revision_rounds: int = Field(1, ge=0, le=3)


class CrossReviewRequest(BaseModel):
    artifact_id: int
    dimensions: list[str] = ["钩子", "人设", "爽点", "反转", "台词", "可拍性", "合规"]


class VideoTaskCreate(BaseModel):
    project_id: int
    episode: int = 1
    scene_no: int = 1
    provider: str = "manual"
    prompt: str
    negative_prompt: str = ""
    seed: int | None = None
    ref_assets: list[dict[str, Any]] = []


class VideoTaskOut(BaseModel):
    id: int
    project_id: int
    episode: int
    scene_no: int
    provider: str
    status: str
    prompt: str
    negative_prompt: str
    seed: int | None
    ref_assets: list[dict[str, Any]]
    result_url: str | None
    error: str | None
    created_at: datetime
    updated_at: datetime

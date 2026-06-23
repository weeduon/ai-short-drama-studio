from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    logline: Mapped[str] = mapped_column(Text)
    genre: Mapped[str] = mapped_column(String(80), default="爽文短剧")
    audience: Mapped[str] = mapped_column(String(120), default="抖音/快手/小红书泛娱乐用户")
    platform: Mapped[str] = mapped_column(String(80), default="竖屏短剧")
    tone: Mapped[str] = mapped_column(String(80), default="强反转、强情绪、网感抽象")
    status: Mapped[str] = mapped_column(String(40), default="draft")

    artifacts: Mapped[list["Artifact"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    video_tasks: Mapped[list["VideoTask"]] = relationship(back_populates="project", cascade="all, delete-orphan")


class Artifact(Base, TimestampMixin):
    __tablename__ = "artifacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    stage: Mapped[str] = mapped_column(String(80), index=True)
    role: Mapped[str] = mapped_column(String(120))
    title: Mapped[str] = mapped_column(String(200))
    content_json: Mapped[str] = mapped_column(Text)
    score_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    project: Mapped[Project] = relationship(back_populates="artifacts")


class ModelProvider(Base, TimestampMixin):
    __tablename__ = "model_providers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    provider_type: Mapped[str] = mapped_column(String(80), default="openai_compatible")
    base_url: Mapped[str] = mapped_column(String(300))
    api_key_env: Mapped[str] = mapped_column(String(80))
    model_name: Mapped[str] = mapped_column(String(160))
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    purpose: Mapped[str] = mapped_column(String(80), default="writing")


class WorkflowRun(Base, TimestampMixin):
    __tablename__ = "workflow_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    status: Mapped[str] = mapped_column(String(40), default="queued")
    current_stage: Mapped[str] = mapped_column(String(80), default="pending")
    trace_json: Mapped[str] = mapped_column(Text, default="[]")


class Review(Base, TimestampMixin):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    artifact_id: Mapped[int] = mapped_column(ForeignKey("artifacts.id"), index=True)
    reviewer_model: Mapped[str] = mapped_column(String(120))
    score: Mapped[float] = mapped_column(Float, default=0)
    verdict: Mapped[str] = mapped_column(String(60), default="needs_revision")
    comments_json: Mapped[str] = mapped_column(Text)


class VideoTask(Base, TimestampMixin):
    __tablename__ = "video_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    episode: Mapped[int] = mapped_column(Integer, default=1)
    scene_no: Mapped[int] = mapped_column(Integer, default=1)
    provider: Mapped[str] = mapped_column(String(80), default="manual")
    status: Mapped[str] = mapped_column(String(40), default="queued")
    prompt: Mapped[str] = mapped_column(Text)
    negative_prompt: Mapped[str] = mapped_column(Text, default="")
    seed: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ref_assets_json: Mapped[str] = mapped_column(Text, default="[]")
    result_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)

    project: Mapped[Project] = relationship(back_populates="video_tasks")

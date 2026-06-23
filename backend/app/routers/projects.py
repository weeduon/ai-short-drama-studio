import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Artifact, Project
from ..schemas import ArtifactOut, ProjectCreate, ProjectOut, WorkflowRunRequest
from ..workflows.engine import run_workflow

router = APIRouter(prefix="/api/projects", tags=["projects"])


def artifact_to_out(item: Artifact) -> ArtifactOut:
    return ArtifactOut(
        id=item.id,
        project_id=item.project_id,
        stage=item.stage,
        role=item.role,
        title=item.title,
        content=json.loads(item.content_json),
        score=json.loads(item.score_json) if item.score_json else None,
        created_at=item.created_at,
    )


@router.post("", response_model=ProjectOut)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    project = Project(**payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).order_by(Project.created_at.desc()).all()


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("/{project_id}/artifacts", response_model=list[ArtifactOut])
def list_artifacts(project_id: int, db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    rows = db.query(Artifact).filter(Artifact.project_id == project_id).order_by(Artifact.id.asc()).all()
    return [artifact_to_out(row) for row in rows]


@router.post("/{project_id}/run", response_model=list[ArtifactOut])
async def run_project_workflow(project_id: int, payload: WorkflowRunRequest, db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    # 为了让重复运行可控，保留历史产物，不覆盖。现实世界连版本管理都没有就敢拍剧，过于刺激。
    artifacts = await run_workflow(db, project, episode_count=payload.episode_count)
    return [artifact_to_out(row) for row in artifacts]

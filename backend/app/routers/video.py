import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Project, VideoTask
from ..schemas import VideoTaskCreate, VideoTaskOut

router = APIRouter(prefix="/api/video-tasks", tags=["video-tasks"])


def task_to_out(task: VideoTask) -> VideoTaskOut:
    return VideoTaskOut(
        id=task.id,
        project_id=task.project_id,
        episode=task.episode,
        scene_no=task.scene_no,
        provider=task.provider,
        status=task.status,
        prompt=task.prompt,
        negative_prompt=task.negative_prompt,
        seed=task.seed,
        ref_assets=json.loads(task.ref_assets_json),
        result_url=task.result_url,
        error=task.error,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


@router.post("", response_model=VideoTaskOut)
def create_task(payload: VideoTaskCreate, db: Session = Depends(get_db)):
    if not db.get(Project, payload.project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    task = VideoTask(
        project_id=payload.project_id,
        episode=payload.episode,
        scene_no=payload.scene_no,
        provider=payload.provider,
        prompt=payload.prompt,
        negative_prompt=payload.negative_prompt,
        seed=payload.seed,
        ref_assets_json=json.dumps(payload.ref_assets, ensure_ascii=False),
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task_to_out(task)


@router.get("", response_model=list[VideoTaskOut])
def list_tasks(project_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(VideoTask)
    if project_id:
        query = query.filter(VideoTask.project_id == project_id)
    rows = query.order_by(VideoTask.created_at.desc()).all()
    return [task_to_out(row) for row in rows]


@router.post("/{task_id}/run", response_model=VideoTaskOut)
def run_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(VideoTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Video task not found")
    # 这里先做任务状态机。真实平台 API 差异很大，接入点集中放在这个动作里。
    task.status = "ready_for_external_video_api"
    task.result_url = "请接入 Kling/Runway/Veo/海螺/Seedance 等视频 API 后自动回填。当前任务已生成可复制的 Prompt。"
    db.commit()
    db.refresh(task)
    return task_to_out(task)

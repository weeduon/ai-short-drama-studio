import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..llm.review import review_with_models
from ..models import Artifact, Review
from ..schemas import CrossReviewRequest

router = APIRouter(prefix="/api/review", tags=["review"])


@router.post("/cross")
async def cross_review(payload: CrossReviewRequest, db: Session = Depends(get_db)):
    artifact = db.get(Artifact, payload.artifact_id)
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    content = json.loads(artifact.content_json)
    result = await review_with_models(db, content, payload.dimensions)
    artifact.score_json = json.dumps(result, ensure_ascii=False)
    for item in result.get("reviews", []):
        db.add(
            Review(
                artifact_id=artifact.id,
                reviewer_model=item.get("_model", "unknown"),
                score=float(item.get("score", 0) or 0),
                verdict=item.get("verdict", "needs_revision"),
                comments_json=json.dumps(item, ensure_ascii=False),
            )
        )
    db.commit()
    return result

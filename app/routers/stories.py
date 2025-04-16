from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import Depends, Query
from sqlalchemy import func
from app.db.models import Story
from app.schemas.schemas import StoryOut
from app.db.session import get_db
from app.dependencies.auth import api_key_auth

router = APIRouter()

@router.get("/stories", response_model=List[StoryOut])
def get_stories(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=0, le=20),
    author: Optional[str] = None,
    min_score: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    _ = Depends(api_key_auth)  # apply the API key auth
):
    query = db.query(Story)

    if author:
        query = query.filter(Story.author.ilike(f"%{author}%"))

    if min_score:
        query = query.filter(Story.score >= min_score)

    if search:
        query = query.filter(Story.title.ilike(f"%{search}%"))

    stories = query.order_by(Story.score.desc()).offset((page - 1) * limit).limit(limit).all()
    return stories

@router.get("/stories/{story_id}", response_model=StoryOut)
def get_story(
    story_id: int,
    db: Session = Depends(get_db),
    _ = Depends(api_key_auth)
):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story

@router.get("/stats/top-authors")
def get_top_authors(
    db: Session = Depends(get_db),
    _ = Depends(api_key_auth)
):
    results = (
        db.query(
            Story.author,
            func.sum(Story.score).label("total_score")
        )
        .group_by(Story.author)
        .order_by(func.sum(Story.score).desc())
        .limit(5)
        .all()
    )

    return [
        {"author": author, "total_score": total_score}
        for author, total_score in results
    ]
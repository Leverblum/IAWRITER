# app/routes/posts.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import database, schemas, models, auth, ai_service

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/generate-post", response_model=schemas.PostResponse)
def generate_post(
    prompt: schemas.PostCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    try:
        title, body, seo = ai_service.generate_post(prompt.prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando contenido: {str(e)}")

    new_post = models.Post(title=title, body=body, seo=seo, author_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/", response_model=list[schemas.PostResponse])
def get_posts(db: Session = Depends(database.get_db)):
    return db.query(models.Post).order_by(models.Post.created_at.desc()).all()

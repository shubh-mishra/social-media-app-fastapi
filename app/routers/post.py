from fastapi import FastAPI, status, Depends, APIRouter, HTTPException, Response
from typing import List, Optional
from .. import models, schemas, oauth2
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()

@router.get("/posts", response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db)):

    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()

    # results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).all()
    
    return posts

@router.get("/posts/{id}", response_model=schemas.Post)
def get_one_post(id: int, db: Session = Depends(get_db)):
    # post = find_post(id)

    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    # return {"data": post}

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    
    return post
    

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # post = post.dict()
    # id = int(len(my_posts))+1
    # post['id'] = id
    # my_posts.append(post)
    # return {"data": my_posts}

    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: str, post: schemas.PostCreate, db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # post_dict = post.dict()
    # post_dict['id'] = int(id)
    # my_posts.append(post_dict)

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()

    update_post = db.query(models.Post).filter(models.Post.id == id).first()

    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    
    if update_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    update_post.title, update_post.content = post.title, post.content
    db.commit()
    db.refresh(update_post)

    return update_post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: str, db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # index = find_post_index(id)
    
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    db.delete(post)
    db.commit()
    
    #my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
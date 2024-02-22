from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from .. database import get_db
from sqlalchemy.orm import Session
from typing import List, Annotated, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: models.User =  Depends(oauth2.get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # cur.execute("""SELECT * FROM posts""")
    # posts = cur.fetchall()
    # print(type(posts))        #<class 'list'>
    # print(current_user.email)
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    #sqlalchemy has a default join of INNER JOIN, but we need OUTER JOIN
    posts = db.query(models.Post, func.count(models.Votes.post_id).label("votes")) \
            .outerjoin(models.Votes, models.Votes.post_id == models.Post.id) \
            .filter(models.Post.title.contains(search)) \
            .group_by(models.Post.id) \
            .limit(limit) \
            .offset(skip) \
            .all()

    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User =  Depends(oauth2.get_current_user)):
    # cur.execute("""INSERT INTO posts (title, content, published) 
    #             VALUES(%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    # new_post = cur.fetchone()
    # print(new_post)
    # conn.commit()

    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # print(current_user.id)
    new_post = models.Post(**(dict(post)), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.PostOut)     #{id} --> this is called a path parameter (it is always a string), so convert it
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: models.User =  Depends(oauth2.get_current_user)):
    # cur.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cur.fetchone()
    # print(post)

    # print(current_user)
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")) \
            .outerjoin(models.Votes, models.Votes.post_id == models.Post.id) \
            .filter(models.Post.id == id)\
            .group_by(models.Post.id) \
            .first()
    
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with ID: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with ID: {id} was not found"}
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action.")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User =  Depends(oauth2.get_current_user)):
    # cur.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    # deleted_post = cur.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if not deleted_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID: {id} does not exist")
    
    if deleted_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action.")
    
    deleted_post.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User =  Depends(oauth2.get_current_user)):
    # cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #              (post.title, post.content, post.published, str(id)))
    # updated_post = cur.fetchone()
    # conn.commit()
    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    # print(updated_post_query)
    if not updated_post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID: {id} does not exist")
    
    if updated_post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action.")
    updated_post_query.update(dict(post), synchronize_session=False)
    db.commit()
    
    return updated_post_query.first()
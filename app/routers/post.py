from fastapi import FastAPI, Response, status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List,Optional
from sqlalchemy import func
from .. import models, Schemas, oauth2


router = APIRouter(
    tags = ['Posts']
)


@router.get("/posts",response_model=List[Schemas.PostOut])
#@router.get("/posts")
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cur.execute(""" select *from posts """)
    # posts = cur.fetchall()

    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    #posts = db.query(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id,isouter = True).group_by(models.Post.id).all()

    return results

@router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=Schemas.ResponsePost)
def create_posts(post: Schemas.ModelPost,db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    # # post_d = post.dict()
    # # post_d['id'] = randrange(0,1000000)
    # # my_posts.append(post_d)
    # cur.execute(""" INSERT INTO posts("title", "content") VALUES(%s, %s) returning * """,(post.title,post.content))
    # new_post = cur.fetchone()
    # con.commit()
    #new_post = models.Post(title=post.title, content=post.content)
    new_post = models.Post(owner_id = current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post

@router.get("/posts/{id}",response_model=Schemas.ResponsePost)
def get_post(id:int,db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    # cur.execute(""" SELECT * from posts where id = %s """,(str(id),))
    # post = cur.fetchone()
    #post = find_post(id)

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} was not found")
    #return {"post_detail": f"{post}"}
    return post

@router.delete("/posts/{id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cur.execute(""" DELETE FROM posts WHERE id = %s returning * """,(str(id),))
    # index = cur.fetchone()
    # con.commit()
    #index = find_post(id)

    index_query = db.query(models.Post).filter(models.Post.id == id)
    index = index_query.first()
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} was not found")
    
    if index.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    index_query.delete(synchronize_session=False)
    db.commit()
    #my_posts.pop(index)
    #return {'message': 'post was successfully deleted'} 
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("posts/{id}",response_model=Schemas.ResponsePost)
def update_post(id:int, update_post:Schemas.PostCreate,db: Session = Depends(get_db)):
    # cur.execute(""" UPDATE posts SET title = %s, content = %s Where id = %s RETURNING *""",(post.title,post.content),(str(id),))
    # index = cur.fetchone()
    # con.commit()
    #index = find_post(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} was not found")
    post_query.update(update_post.dict(),synchronize_session=False)
    db.commit()

    return  post
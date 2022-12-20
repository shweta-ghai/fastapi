# import sys
# from pathlib import Path

# file = Path("app\models.py").resolve()
# package_root_directory = file.parents[0]
# sys.path.append(str(package_root_directory))

# import models,Schemas,utils
from fastapi import FastAPI, Response, status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
import database
from .. import models, Schemas, utils

router = APIRouter(
    tags = ['Users']
)

@router.post("/users",status_code=status.HTTP_201_CREATED,response_model=Schemas.UserOut)
def create_user(user: Schemas.UserCreate,db: Session = Depends(database.get_db)):
    # hash the password- user.password
    hashed_password = utils.hash(user.password)

    user.password = hashed_password
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user

@router.get("/users/{id}",response_model=Schemas.UserOut)
def get_user(id:int,db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        details= f"User with id :{id} does not exist")
    return user
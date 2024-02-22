from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from .. database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    user.password = utils.hash_password(user.password)    #imported from utils.py
    # print(user.password)

    new_user = models.User(**(dict(user)))
    print("New User Data:", new_user.__dict__)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with ID: {id} was not found')
    return user
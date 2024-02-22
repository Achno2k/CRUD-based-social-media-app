from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
router = APIRouter(
    tags=['Authentication']
)

@router.post("/login", response_model=schemas.AccessToken)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    #Oauth2PasswordRequestForm returns some json in the format
    #{"username": "", "password": ""} --> no longer has the email field, so now email is actually called username

    # print(user_credentials.username)
    # print(user_credentials.password)


    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email not found. Please try again")
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403, detail="Invalid credentials. Please try again")
    
    access_token = oauth2.create_token({"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
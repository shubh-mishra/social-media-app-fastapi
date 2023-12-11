from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, models, utils, database, oauth2
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/login", response_model=schemas.Token)
def login(user_credential: schemas.UserCreate, db:Session = Depends(database.get_db) ):
#def login(user_credential: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db) ):

    user = db.query(models.User).filter(models.User.email == user_credential.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.orm import Session
from API.config import ACCESS_TOKEN_EXPIRE_MINUTES
import crud
import schemas
from API.dependencies import create_access_token, get_current_user, get_db, authenticate_user






auth = APIRouter()

















@auth.post("/utilisateur/", response_model=schemas.UserInDB)
def créer_un_utilisateur(
    username: str = Form(...),
    password: str = Form(...),
    email: Optional[str] = Form(None),
    full_name: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: schemas.UserInDB = Depends(get_current_user)
):
    if not username or not password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Le nom d'utilisateur et le mot de passe sont requis")

    user = schemas.UserCreate(
        username=username,
        email=email,
        full_name=full_name,
        password=password,
    )
    
    try:
        created_user = crud.create_user(db, user)
        return created_user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))












@auth.post("/token", response_model=schemas.Token)
def authentification_pour_un_jeton_d_accès(
      username: str = Form(...),
      password: str = Form(...),
      db: Session = Depends(get_db),
) -> schemas.Token:
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")











@auth.get("/utilisateur/utilisateur actuel/", response_model=schemas.User)
def voir_utilisateur_actuel(current_user: schemas.UserInDB = Depends(get_current_user)):
    return current_user


 
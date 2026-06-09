from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pymongo.database import Database

from .db import get_db
from .schemas import RegisterRequest, TokenResponse
from .security import get_password_hash, verify_password, create_access_token

router = APIRouter()

@router.post("/register", status_code=201)
def register(payload: RegisterRequest, db: Database = Depends(get_db)):
    existing = db.users.find_one({"email": payload.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_dict = {
        "email": payload.email,
        "password_hash": get_password_hash(payload.password)
    }
    result = db.users.insert_one(user_dict)
    
    return {"id": str(result.inserted_id), "email": payload.email}

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Database = Depends(get_db)):
    user = db.users.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=user["email"])
    return TokenResponse(access_token=token)

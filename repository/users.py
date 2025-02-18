from typing import TypeVar ,Generic,Optional
from sqlalchemy.orm import Session
from fastapi import Depends,Request,HTTPException
from fastapi.security import HTTPBearer,HTTPBasicCredentials
from datetime import datetime,timedelta
from jose import JWTError, jwt
from postgreConfig import ACCESS_TOKEN_EXPIRE_MINUTES,ALGORITHM,SECRET_KEY

T=TypeVar("T")

class BaseRepo():
    @staticmethod
    def insert(db:Session,model:Generic[T]):
        db.add(model)
        db.commit()
        db.refresh(model)
        
class UserRepo(BaseRepo):
    @staticmethod
    def get_by_username(db:Session, username: str,model:Generic[T]):
        return db.query(model).filter(model.username == username).first()
    
class JWTRepo(BaseRepo):
    
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
            return encoded_jwt
    def decode_access_token(token:str):
        try:
            decode_token=jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            return decode_token if decode_token["expires"] >= datetime.utcnow() else None
        except:
            return {}

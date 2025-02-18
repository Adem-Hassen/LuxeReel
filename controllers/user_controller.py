from fastapi import APIRouter,Depends
from postgreConfig import engine
from models.models import Login,Register,ResponseSchema,TokenResponse
from sqlalchemy.orm import Session
from postgreConfig import get_db
from passlib.context import CryptContext
from repository.users import UserRepo,JWTRepo
from database.database import Users
import  database.database as database

database.Base.metadata.create_all(bind=engine)

user_router = APIRouter(prefix="/api/users",tags=["Users"])

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

@user_router.post("/register")
async def register(request:Register,db:Session=Depends(get_db)) :
    try :
        _user=Users(username=request.username,email=request.email,password=pwd_context.hash(request.password),phone_number=request.phone_number,first_name=request.first_name,last_name=request.last_name)
        UserRepo.insert(db,_user)
        return ResponseSchema(code="200",status_code="Created",message="User created successfully").model_dump(exclude_none=True)
    except Exception as e:
        return ResponseSchema(code="400",status_code="Bad Request",message=str(e)).model_dump(exclude_none=True)

@user_router.post("/login")
async def login(request:Login, db:Session=Depends(get_db)):
    print(request.username)

    try:
        _user=UserRepo.get_by_username(db,request.username,Users)
        if not pwd_context.verify(request.password,_user.password):
            return ResponseSchema(code="401",status_code="Unauthorized",message="Invalid credentials").model_dump(exclude_none=True)
        token=JWTRepo.create_access_token(data={"sub":_user.username})
        return ResponseSchema(code="200",status_code="OK",message="Login successful",result=TokenResponse(access_token=token,token_type="bearer")).model_dump(exclude_none=True)
    except Exception as e:
        error_message=str(e.args)
        return ResponseSchema(code="400",status_code="Bad Request",message=error_message).model_dump(exclude_none=True) 
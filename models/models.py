from pydantic import BaseModel,Field
import torch
import torch.nn as nn
from typing import Generic,Optional, TypeVar
from pydantic.generics import GenericModel
T = TypeVar('T')

class RecRequest(BaseModel):
    user_id: int
    num_recs: int=5

class RecModel(nn.Module):
    def __init__(self, n_users, n_movies):
        super().__init__()
        self.users = nn.Embedding(n_users, 128)
        self.movies = nn.Embedding(n_movies, 128)
        self.out = nn.Linear(256, 1)

    def forward(self, users, movies):
        users_embed = self.users(users)
        movies_embed = self.movies(movies)
        output = torch.cat([users_embed, movies_embed], dim=1)
        return self.out(output)
    
class Login(BaseModel):
    username: str
    password: str

class Register(BaseModel):
    id:str
    username: str
    password: str
    email: str
    phone_number: str
    first_name: str
    last_name: str

class ResponseSchema(BaseModel):
    code:str
    status_code:str
    message:str
    result:Optional[T]=None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str




from pydantic import BaseModel
import torch
import torch.nn as nn


class RecRequest(BaseModel):
    user_id: int
    num_recs: int

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



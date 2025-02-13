from models.models import RecModel
import pandas as pd
import torch
import pickle

def load_model():
    with open("../Recommendation_System/label_encoders.pkl", "rb") as f:
        label_data = pickle.load(f)
        users_label = label_data["users_label"]
        movies_label = label_data["movies_label"]
    ratings=pd.read_csv("../Recommendation_System/dataset/ratings.csv")
    model=RecModel(n_users=len(users_label.classes_), n_movies=len(movies_label.classes_))
    model.load_state_dict(torch.load("../Recommendation_System/recommendation_model.pth"))
    return model, users_label, movies_label, ratings

def get_recommendation(user_id,top_k=5):
    model,users_label, movies_label, ratings,=load_model()
    model.eval()
    if user_id not in users_label.classes_:
        
        return {"message":f"User ID {user_id} not found in dataset."}
    all_movie_ids = ratings["movieId"].unique().tolist()
    movies=pd.read_csv("../Recommendation_System/dataset/movies.csv")
    user_idx = users_label.transform([user_id])[0]
    movie_indices = movies_label.transform(all_movie_ids)

  
    user_tensor = torch.tensor([user_idx] * len(movie_indices), dtype=torch.long)
    movie_tensor = torch.tensor(movie_indices, dtype=torch.long)
   
        
    with torch.no_grad():
        predicted_ratings =model(user_tensor, movie_tensor).squeeze()

    probabilities = torch.nn.functional.softmax(predicted_ratings, dim=0)
    top_indices = torch.multinomial(probabilities, num_samples=top_k)
    sorted_movies_idx = [movies_label.inverse_transform([i])[0] for i in top_indices]
    sorted_movies_idx = [int(idx) for idx in sorted_movies_idx]
    top_movies=movies[movies["movieId"].isin(sorted_movies_idx)].to_dict(orient="records")
    return top_movies

def get_top_movies(top_n=10, min_ratings=50):
    ratings=pd.read_csv("../Recommendation_System/dataset/ratings.csv")
    movies=pd.read_csv("../Recommendation_System/dataset/movies.csv")
    movie_counts = ratings.groupby("movieId")["rating"].agg(["mean", "count"]).reset_index()
    

    filtered_movies = movie_counts[movie_counts["count"] >= min_ratings]

 
    filtered_movies = filtered_movies.merge(movies, on="movieId")
    
    top_movies = filtered_movies.sort_values(by="mean", ascending=False).head(top_n)
    
    return top_movies.to_dict(orient="records")
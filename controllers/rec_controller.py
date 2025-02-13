from fastapi import APIRouter
from models.models import RecRequest
from services.rec_services import get_recommendation,get_top_movies

rec_router = APIRouter(prefix="/api/recommend",tags=["Recommendation"])

@rec_router.post("/get_recommendations")
def get_recommendations(request:RecRequest):
    user_id = request.user_id
    num_recs = request.num_recs
    if not user_id :
        return {"message": "User ID is required"}
    movies=get_recommendation(user_id,num_recs)
    return {"user_Id": user_id, "recommendations": movies}


@rec_router.get("/get_top_movies")
def get_best_movies():
    top_movies=get_top_movies(top_n=5)
    return {"top_movies":top_movies}

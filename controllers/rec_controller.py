from fastapi import APIRouter,Query
from database.database import db
from models.models import RecRequest
from services.rec_services import get_recommendation,get_top_movies,fetch_all_movies,fetch_filtred_movies

rec_router = APIRouter(prefix="/api/recommend",tags=["Recommendation"])

@rec_router.post("/get_recommendations")
def get_recommendations(request:RecRequest):
    user_id = request.user_id
    num_recs = request.num_recs
    if not user_id or not isinstance(user_id, int):
        return {"message": "User ID is required"}
    movies=get_recommendation(user_id,num_recs)
    return {"user_Id": user_id, "recommendations": movies}


@rec_router.get("/get_top_movies")
def get_best_movies():
    top_movies=get_top_movies(top_n=5)
    return {"top_movies":top_movies}

@rec_router.get("/all_movies")
async def get_all_movies(page: int = Query(1, ge=1), limit: int = Query(12, le=1000)):
    skip = (page - 1) * limit
    movies = await fetch_all_movies(skip=skip, limit=limit) 
    total_movies=await db["car_listings"].count_documents({})
    return {"total_movies": total_movies,"movies": movies}

@rec_router.get("/filtred_movies")
async def get_filtered_movies(title:str=Query(""), year:str=Query(""),genre:str=Query(""), page: int = Query(1, ge=1), limit: int = Query(12, le=1000)):
        skip = (page - 1) * limit
        movies,total_movies = await fetch_filtred_movies(title,genre,year, skip, limit)
        return {"total_movies": total_movies,"movies": movies}

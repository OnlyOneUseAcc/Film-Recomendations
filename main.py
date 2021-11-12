import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi

from models.WatchHistory import WatchHistory
from models.User import User
from models.Content import Content
from RecSystem.Recommendations import Recommendations
from typing import List


app = FastAPI()
recommendation_manager = Recommendations('Data/')
matrix_manager = recommendation_manager.get_matrix_manager()

NUM_SIMILAR_USERS = 100


@app.post("/watch_history/{user_id}",
          description="Add users watch history to database",
          tags=["Watch history"])
def insert_watch_history(user_id: int, watch_history: WatchHistory):
    if not matrix_manager.user_exist(user_id):
        raise HTTPException(status_code=404, detail="No such user")
    exist_watch_history = set()
    for unit in matrix_manager.get_watch_history(user_id).history:
        exist_watch_history.add(unit)

    new_watch_history = set()
    for unit in watch_history.history:
        new_watch_history.add(unit)

    new_watch_history = new_watch_history - exist_watch_history
    watch_history.history = list(new_watch_history)
    matrix_manager.insert_watch_history(watch_history)


@app.get("/watch_history/{user_id}",
         description="Get users watch history to database",
         tags=["Watch history"]
         )
def get_watch_history(user_id: int):
    if not matrix_manager.user_exist(user_id):
        raise HTTPException(status_code=404, detail="No such user")
    return matrix_manager.get_watch_history(user_id)


@app.post("/user",
          description="Register new user in system (user_id should be -1)",
          tags=["User"],
          response_model=User)
def register_user(user: User):
    registered_user = matrix_manager.insert_user(user)
    if registered_user is not None:
        return registered_user
    else:
        raise HTTPException(status_code=400)


@app.get("/user",
         description="Log in user in system",
         tags=["User"],
         response_model=User
         )
def login_user(login: int, password: str):
    if not matrix_manager.user_exist(login):
        raise HTTPException(status_code=401, detail="Auth failed")
    user = matrix_manager.get_user_info(login, password)
    if user is None:
        raise HTTPException(status_code=401, detail="Auth failed")
    else:
        return user


@app.get("/content/{content_id}",
         description="Get content item by id",
         response_model=Content,
         tags=["Content"])
def get_content(content_id: int):
    try:
        return matrix_manager.get_content(content_id)[0]
    except KeyError:
        raise HTTPException(status_code=404, detail="No such content")


@app.get("/recommendation/base",
         description="Get user recommendations based on his watch history",
         response_model=List[Content],
         tags=['Recommendation'])
def get_history_recommendation(user_id: int):
    if not matrix_manager.user_exist(user_id):
        raise HTTPException(status_code=404, detail="No such user")
    return recommendation_manager.get_rec_content(user_id, NUM_SIMILAR_USERS)


@app.get("/recommendation/type",
         description="Get most popular content in different types of content",
         tags=['Recommendation'])
def get_type_recommendation():
    return {
        'serial_with_season': recommendation_manager.get_rec_by_type("serial_with_season")['content_name'],
        'movie': recommendation_manager.get_rec_by_type("movie")['content_name'],
    }


@app.get("/recommendation/genre",
         description="Get users recommendations based on genres in his watch history",
         tags=['Recommendation'])
def get_genre_recommendation(user_id: int):
    if not matrix_manager.user_exist(user_id):
        raise HTTPException(status_code=404, detail="No such user")
    genre_rec = recommendation_manager.top_genres_per_user(user_id)
    return {
        'genres': genre_rec[1],
        'content': genre_rec[0]
    }


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Film recommendations",
        version="0.0.2",
        description="API schema for film recommendation platform",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

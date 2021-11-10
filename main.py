import uvicorn
from fastapi import FastAPI, HTTPException
from models.WatchHistory import WatchHistory
from models.User import User
from RecSystem.Recommendations import Recommendations


app = FastAPI()
recommendation_manager = Recommendations('Data/')
matrix_manager = recommendation_manager.get_matrix_manager()

NUM_SIMILAR_USERS = 100


@app.post("/watch_history/{user_id}")
def insert_watch_history(user_id: int, watch_history: WatchHistory):
    exist_watch_history = set()
    for unit in matrix_manager.get_watch_history(user_id).history:
        exist_watch_history.add(unit)

    new_watch_history = set()
    for unit in watch_history.history:
        new_watch_history.add(unit)

    new_watch_history = new_watch_history - exist_watch_history
    watch_history.history = list(new_watch_history)
    matrix_manager.insert_watch_history(watch_history)


@app.get("/watch_history/{user_id}")
def get_watch_history(user_id: int):
    return matrix_manager.get_watch_history(user_id)


@app.post("/user")
def register_user(user: User):
    registered_user = matrix_manager.insert_user(user)
    if registered_user is not None:
        return registered_user
    else:
        raise HTTPException(status_code=400)


@app.get("/user")
def login_user(login: int, password: str):
    if not matrix_manager.user_exist(login):
        raise HTTPException(status_code=401, detail="Auth failed")
    user = matrix_manager.get_user_info(login, password)
    if user is None:
        raise HTTPException(status_code=401, detail="Auth failed")
    else:
        return user


@app.get("/content/{content_id}")
def get_content(content_id: int):
    try:
        return matrix_manager.get_content(content_id)[0]
    except KeyError:
        raise HTTPException(status_code=404, detail="No such content")


@app.get("/recommendation/base")
def get_history_recommendation(user_id: int):
    return recommendation_manager.get_rec_content(user_id, NUM_SIMILAR_USERS)


@app.get("/recommendation/type")
def get_type_recommendation():
    return {
        'serial_with_season': recommendation_manager.get_rec_by_type("serial_with_season")['content_name'],
        'movie': recommendation_manager.get_rec_by_type("movie")['content_name'],
    }


@app.get("/recommendation/genre")
def get_genre_recommendation(user_id: int):
    genre_rec = recommendation_manager.top_genres_per_user(user_id)
    return {
        'genres': genre_rec[1],
        'content': genre_rec[0]
    }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

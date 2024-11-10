from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel


app = FastAPI()

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int = None


@app.get("/users")
async def get_all_users() -> list:
    return users


@app.post("/user/{username}/{age}")
async def register_user(user: User):
    user.id = 1
    if len(users):
        last_element = users[-1]
        user.id = last_element.id + 1
    users.append(user)
    return user


@app.put("/user/{user_id}/{username}/{age}")
async def update_users_info(user: User = Body()):
    try:
        for i in range(len(users)+1):
            current_user = users[i]
            if user.id == current_user.id:
                users[i] = user
                return user
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    try:
        for i in range(len(users) + 1):
            current_user = users[i]
            if user_id == current_user.id:
                return users.pop(i)
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

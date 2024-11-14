from fastapi import FastAPI, Body, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from starlette import status

app = FastAPI()
templates = Jinja2Templates(directory="templates")
users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int = None


@app.get("/")
async def get_main_page(request: Request, ) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/user/{user_id}")
async def get_users(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id - 1]})
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/user/{username}/{age}")
async def post_user(request: Request, user: User = Form()) -> HTMLResponse:
    user.id = 1
    if len(users):
        last_element = users[-1]
        user.id = last_element.id + 1
    users.append(User(id=user.id, username=user.username, age=user.age))
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user: User = Body()):
    try:
        for i in range(len(users) + 1):
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

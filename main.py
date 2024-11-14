from typing import List
from fastapi import FastAPI, Body, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from starlette import status

app = FastAPI()
templates = Jinja2Templates(directory="templates")
messages_db = []


class Message(BaseModel):
    id: int = None
    text: str


@app.get("/")
async def get_all_messages(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("message.html", {"request": request, "messages": messages_db})


@app.get("/message/{message_id}")
async def get_messages(request: Request, message_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse("message.html",
                                          {"request": request, "message": messages_db[message_id]})
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_message(request: Request, message: str = Form()) -> HTMLResponse:
    if messages_db:
        message_id = max(messages_db, key=lambda m: m.id).id + 1
    else:
        message_id = 0
    messages_db.append(Message(id=message_id, text=message))
    return templates.TemplateResponse("message.html", {"request": request, "messages": messages_db})


@app.put("/message/{messages_id}")
async def update_message(message_id: int, message: str = Body()) -> str:
    try:
        edit_message = messages_db[message_id]
        edit_message.text = message
        return "Message updated!"
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.delete("/message/{message_id}")
async def delete_message(message_id: int) -> str:
    try:
        messages_db.pop(message_id)
        return f"Message ID={message_id} deleted!"
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.delete("/")
async def delete_all_messages() -> str:
    messages_db.clear()
    return "All messages deleted"

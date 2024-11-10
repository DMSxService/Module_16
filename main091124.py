from fastapi import FastAPI, Path


app = FastAPI()

messages_db = {"0": "First post in FastApi"}


@app.get("/")
async def get_all_messages() -> dict:
    return messages_db


@app.get("/message/{message_id}")
async def get_messages(message_id: str) -> dict:
    return messages_db[message_id]


@app.post("/message")
async def create_message(message: str) -> str:
    current_index = str(int(max(messages_db, key=int))+1)
    messages_db[current_index] = message
    return "Message created!"


@app.put("/message/{messages_db}")
async def update_message(message_id: str, message: str) -> str:
    messages_db[message_id] = message
    return "Message updated."


@app.delete("/message/{message_id}")
async def delete_message(message_id: str) -> str:
    messages_db.pop(message_id)
    return f"Message with {message_id} was deleted."


@app.delete("/")
async def delete_all_messages() -> str:
    messages_db.clear()
    return "All messages deleted"


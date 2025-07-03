from fastapi import FastAPI
from pydantic import BaseModel
from agent import chat_with_agent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserMessage(BaseModel):
    message: str

@app.post("/chat")
def chat(msg: UserMessage):
    response = chat_with_agent(msg.message)
    return {"response": response}
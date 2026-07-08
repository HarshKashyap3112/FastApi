from fastapi import FastAPI
from pydantic import BaseModel

app= FastAPI()

class User(BaseModel):
    name:str
    address:str
    password:str


class response_user(BaseModel):
    name:str
    address:str

@app.get("/")
def home():
    return {
        "message":"hello this is home page !!"
    }

@app.post("/user",response_model=response_user)
def user(user:User):
    return user
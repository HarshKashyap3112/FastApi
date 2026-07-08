from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

USER=[]
class User(BaseModel):
    name:str
    age:int

@app.post("/user")
def create_user(user:User):
    USER.append(user)
    return user

@app.put("/user/{user_id}")
def updateUser(user_id:int,user:User, notify:bool):
    if user_id < len(USER):
        USER[user_id]=user
        return user
    return {"message":"user not found"}
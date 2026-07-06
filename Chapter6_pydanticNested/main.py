from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()

class Address(BaseModel):
    type:str
    city:str
    pincode:str
    
class user(BaseModel):
    name:str
    email:str
    address:Address

@app.get("/")
def read_root():
    return {"Hello World"}

@app.post("/create_user")
def create_user(user_data:user):
    return {
        "message":"this is user data ",
        "data":user_data
    }
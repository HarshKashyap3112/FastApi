from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from pydantic import BaseModel

app= FastAPI()
secret_key="mysecretkey"
ALGORITHM='HS256'
Oath_scheme=OAuth2PasswordBearer( tokenUrl="login")

fake_users={
    "harsh":{
        "username":"harsh",
        "age":24,
        "password":"1234"
    },
    "ravi":{
        "username":"ravi don",
        "age":23,
        "password":"4567"
    }
}
class User(BaseModel):
    username:str
    age:int
    password:str



@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = fake_users.get(form_data.username)

    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode(
        {"sub": form_data.username},
        secret_key,
        algorithm=ALGORITHM
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

async def get_user(token:str= Depends(Oath_scheme)):
    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[ALGORITHM]
        )
        username= payload["sub"]
        return username
    except:
        raise HTTPException(401,"Invalid authentication")
    
@app.get("/profile")
def get_profile(currentUser:str=Depends(get_user)):
    return {
        "message":f"welcome {currentUser}"
    }
from fastapi import FastAPI
from calculator import addition, substraction
app=FastAPI()

@app.get("/")
def home():
    return {"message":"this is home page !!"}

app.include_router(addition.router)
app.include_router(substraction.router)
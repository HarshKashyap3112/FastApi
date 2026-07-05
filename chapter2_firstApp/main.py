# pyrefly: ignore [missing-import]
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def home():
    return {"message":"Hello, FastAPI!"}

@app.get("/about")
def about():
    return {"message": "About Page"}

@app.get("/users")
def users():
    return [{"name":"Abdul","age":25},{"name":"Ali","age":22},{"name":"Ahmed","age":23}]
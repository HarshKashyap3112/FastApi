from fastapi import FastAPI
import uvicorn
app = FastAPI()
@app.get("/")
def home():
    return {"message":"this is home page !!"}

@app.get("/user/{user_id}")
def user(user_id:int):
    print("this is user route")
    return {"message": "hello this is user "+ str(user_id)}

if __name__ == "__main__":
    # Explicitly configure the host and manual port here
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
from fastapi import FastAPI,status,HTTPException
import uvicorn
app=FastAPI()

@app.post("/user",status_code=status.HTTP_201_CREATED)
def user():
    return {
        "message":"user is created"
    }

@app.get("/user/{user_id}",status_code=status.HTTP_200_OK)
def getUser(user_id:int):
    if user_id != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user is not present"
        )
    return {
        "userName":"harsh",
        "address":"wse"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",      # <filename>:<FastAPI instance>
        host="127.0.0.1",
        port=8000,
        reload=True
    )

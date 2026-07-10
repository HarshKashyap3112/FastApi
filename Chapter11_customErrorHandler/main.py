from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
app=FastAPI()

class unicornException(Exception):
    def __init__(self, name:str):
        self.name=name

@app.exception_handler(unicornException)
async def unicorn_exception_handler(request:Request,exc:unicornException):
        return JSONResponse(
             status_code=418,
             content={"message": f"Oops! {exc.name} did something wrong. Yikes!"},
        )

@app.get("/")
def home():
    return {
        "message":"this is home page !!"
    }

@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "voldemort":
        raise unicornException(name=name)
    return {"unicorn_name": name}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",      # <filename>:<FastAPI instance>
        host="127.0.0.1",
        port=8000,
        reload=True
    )
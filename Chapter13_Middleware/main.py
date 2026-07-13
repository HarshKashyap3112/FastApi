from fastapi import FastAPI,Request

app= FastAPI()
@app.middleware("http")
async def middlewareFunction(request:Request , call_next):
    request.state.user="admin"
    response = await call_next(request)
    return response

@app.get("/")
def home():
    return { "message":"this is home route"};

@app.get("/auth")
def getUser(request:Request):
    return request.state.user;
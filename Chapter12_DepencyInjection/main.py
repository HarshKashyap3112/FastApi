from fastapi import FastAPI, Header,HTTPException,Depends
import uvicorn
app=FastAPI()

def independentFunction():
    return {
        "message":"i am independent function "
    }

@app.get("/home")
def dependentFunction(data= Depends(independentFunction)):
    return data

#real use case below

def verifyToken(token:str = Header(None)):
    if token != "mysecrettoken":
        raise HTTPException(
            status_code=418,
            detail="Unauthorized access"
        )
    return{
        "message":"access granted"
    }


@app.get('/profile')
def getProfile( check = Depends(verifyToken)):
    check.update({'user':"harsh"})
    return check

if __name__ == "__main__":
    uvicorn.run(
        "main:app",      # <filename>:<FastAPI instance>
        host="127.0.0.1",
        port=8000,
        reload=True
    )
from fastapi import FastAPI
import asyncio
import time
# def syncronusCode():
#     time.sleep(3)
#     print("code sleep for 3 second")
#     time.sleep(2)
#     print("code sleep for 2 seconds")

# syncronusCode()

app=FastAPI()

@app.get("/home")
async def asyncCode():
    a= await asyncio.sleep(3, "this is 3 sec delay")

    return a
   

@app.get("/new")
def newFunction():
     time.sleep(20)
     return {"message":"this is 20 sec delay "}
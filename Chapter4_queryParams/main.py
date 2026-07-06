from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello World"}

@app.get("/users")
def user(name:str=None):
    return {
        "user": name
    }

@app.get("/products")
def product(name:str=None,price:float=None,quantity:int=None):
    return {
        "name": name,
        "price": price,
        "quantity": quantity
    }



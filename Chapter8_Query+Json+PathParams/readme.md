# Chapter 8: Query + JSON + Path Params

This directory contains a hands-on example demonstrating how to handle combinations of **Path Parameters**, **JSON Request Bodies**, and **Query Parameters** simultaneously within a single FastAPI endpoint.

## Overview

In FastAPI, you can combine multiple types of input parameters in a single route definition. FastAPI automatically differentiates between them using Python type hints and Pydantic models:

1. **Path Parameters**: Defined directly within the URL path (e.g., `{user_id}`).
2. **JSON Request Body**: Defined using a Pydantic model type hint (e.g., `user: User`).
3. **Query Parameters**: Any function arguments that are scalar types (like `bool`, `int`, `str`) and are **not** part of the URL path (e.g., `notify: bool`).

## Code Implementation

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# In-memory database simulation
USER = []

class User(BaseModel):
    name: str
    age: int

@app.post("/user")
def create_user(user: User):
    USER.append(user)
    return user

@app.put("/user/{user_id}")
def updateUser(user_id: int, user: User, notify: bool):
    if user_id < len(USER):
        USER[user_id] = user
        return user
    return {"message": "user not found"}
```

## Key Concepts Demonstrated

### 1. Unified Endpoint Parameters (`/user/{user_id}`)

The `updateUser` function demonstrates three distinct input sources working in tandem:

- `user_id: int` → Path Parameter (matches `{user_id}` in the route URL).
- `user: User` → JSON Body (inferred automatically because it inherits from Pydantic's `BaseModel`).
- `notify: bool` → Query Parameter (inferred because it is a scalar type not found anywhere in the path). FastAPI recognizes these categories automatically from the function signature and type hints [2][8].

### 2. Pydantic Data Validation

The `User` model ensures that any incoming request data to `POST /user` or `PUT /user/{user_id}` strictly conforms to having a string `name` and an integer `age` before hitting your endpoint logic [2].

## How to Run the Application

### Install Dependencies

Ensure you have `fastapi` and an ASGI server like `uvicorn` installed:

```bash
pip install fastapi uvicorn
```

### Run the Server

Save the code to a file named `main.py` and run:

```bash
uvicorn main:app --reload
```

### Access Interactive Documentation

Open your browser and navigate to:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

FastAPI automatically generates interactive docs for endpoints, including parameter schemas and request bodies [2][8].

## API Endpoint Guide

### Create User

- Method: `POST`
- URL: `/user`
- Body:

```json
{
  "name": "John Doe",
  "age": 28
}
```

### Update User

- Method: `PUT`
- URL: `/user/{user_id}?notify=true`  
  Example: `/user/0?notify=false`
- Path Param: `user_id` (integer index)
- Query Param: `notify` (boolean flag)
- Body:

```json
{
  "name": "John Updated",
  "age": 29
}
```
# Chapter 9: Response Model

This directory contains a hands-on example demonstrating how to use **Pydantic Response Models** in FastAPI to control the data returned from an API endpoint.

## Overview

FastAPI allows you to define a **response model** using the `response_model` parameter in route decorators. This ensures that only the fields specified in the response model are returned to the client, even if the endpoint returns additional data.

In this example:

- A `User` model is used to validate incoming request data.
- A `response_user` model is used to filter the API response.
- The `password` field is accepted in the request but excluded from the response for security.

## Code Implementation

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    address: str
    password: str

class response_user(BaseModel):
    name: str
    address: str

@app.get("/")
def home():
    return {
        "message": "hello this is home page !!"
    }

@app.post("/user", response_model=response_user)
def user(user: User):
    return user
```

## Key Concepts Demonstrated

### 1. Request Model (`User`)

The `User` model defines the structure of the incoming JSON request body. FastAPI validates the request automatically before executing the endpoint.

```python
class User(BaseModel):
    name: str
    address: str
    password: str
```

Expected request body:

```json
{
  "name": "John",
  "address": "New York",
  "password": "secret123"
}
```

---

### 2. Response Model (`response_user`)

The `response_user` model specifies what fields should be included in the API response.

```python
class response_user(BaseModel):
    name: str
    address: str
```

Since `password` is not part of this model, FastAPI automatically removes it from the response.

---

### 3. Using `response_model`

The `response_model` parameter tells FastAPI to validate and serialize the returned data according to the specified Pydantic model.

```python
@app.post("/user", response_model=response_user)
def user(user: User):
    return user
```

Although the endpoint returns the complete `User` object, the client receives only the fields defined in `response_user`.

## How to Run the Application

### Install Dependencies

Ensure you have **FastAPI** and **Uvicorn** installed:

```bash
pip install fastapi uvicorn
```

### Run the Server

Save the code in a file named `main.py` and run:

```bash
uvicorn main:app --reload
```

### Access Interactive Documentation

Open your browser and visit:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

FastAPI automatically generates interactive API documentation, including request and response schemas.

## API Endpoint Guide

### Home Endpoint

- **Method:** `GET`
- **URL:** `/`

#### Response

```json
{
  "message": "hello this is home page !!"
}
```

---

### Create User

- **Method:** `POST`
- **URL:** `/user`

#### Request Body

```json
{
  "name": "John",
  "address": "New York",
  "password": "secret123"
}
```

#### Response

```json
{
  "name": "John",
  "address": "New York"
}
```

Notice that the `password` field is omitted because the endpoint uses `response_model=response_user`.

## Why Use Response Models?

Using response models provides several benefits:

- Prevents sensitive information (such as passwords) from being exposed.
- Ensures a consistent API response structure.
- Automatically validates and serializes response data.
- Improves the generated API documentation in Swagger UI and ReDoc.
- Makes your API more secure and easier to maintain.

## Summary

This chapter demonstrates how FastAPI uses Pydantic response models to filter outgoing data. Even if your endpoint returns a complete object, the `response_model` ensures that only the specified fields are sent back to the client, making it an essential feature for building secure and well-structured APIs.
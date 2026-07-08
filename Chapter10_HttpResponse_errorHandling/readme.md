# Chapter 10: HTTP Response & Error Handling

This directory contains a hands-on example demonstrating how to use **HTTP status codes** and **exception handling** in FastAPI. It shows how to return custom HTTP responses for successful requests and how to raise appropriate errors using `HTTPException`.

## Overview

FastAPI makes it easy to return meaningful HTTP status codes and handle errors gracefully. By using the `status_code` parameter in route decorators and raising `HTTPException`, you can provide clear responses that help API clients understand whether a request was successful or why it failed.

In this example:

- A **POST** endpoint returns a **201 Created** status after creating a user.
- A **GET** endpoint returns user information when a valid user ID is provided.
- If the requested user does not exist, the API raises a **404 Not Found** error using `HTTPException`.

## Code Implementation

```python
from fastapi import FastAPI, status, HTTPException
import uvicorn

app = FastAPI()

@app.post("/user", status_code=status.HTTP_201_CREATED)
def user():
    return {
        "message": "user is created"
    }

@app.get("/user/{user_id}", status_code=status.HTTP_200_OK)
def getUser(user_id: int):
    if user_id != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user is not present"
        )

    return {
        "userName": "harsh",
        "address": "wse"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
```

## Key Concepts Demonstrated

### 1. Returning Custom HTTP Status Codes

FastAPI allows you to specify the HTTP status code returned by an endpoint using the `status_code` parameter.

```python
@app.post("/user", status_code=status.HTTP_201_CREATED)
```

When the endpoint is called successfully, the response status code is:

```http
201 Created
```

Response:

```json
{
  "message": "user is created"
}
```

Using appropriate status codes makes your API more descriptive and follows RESTful API standards.

---

### 2. Path Parameters

The `user_id` is received as a path parameter and is automatically converted to an integer by FastAPI.

```python
@app.get("/user/{user_id}")
def getUser(user_id: int):
```

Example request:

```http
GET /user/1
```

FastAPI validates the parameter type automatically. If a non-integer value is provided, it returns a validation error.

---

### 3. Raising HTTP Exceptions

FastAPI provides the `HTTPException` class for returning error responses.

```python
if user_id != 1:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="user is not present"
    )
```

Instead of returning custom dictionaries for errors, raising `HTTPException` immediately stops execution and sends a proper HTTP error response.

Error response:

```json
{
  "detail": "user is not present"
}
```

Status Code:

```http
404 Not Found
```

---

### 4. Using the `status` Module

Instead of writing numeric status codes manually, FastAPI provides readable constants through the `status` module.

Examples:

```python
status.HTTP_200_OK
status.HTTP_201_CREATED
status.HTTP_404_NOT_FOUND
```

Using these constants makes your code easier to understand and reduces the chance of mistakes.

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

Or execute the Python file directly:

```bash
python main.py
```

### Access Interactive Documentation

Open your browser and visit:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

FastAPI automatically generates interactive API documentation for all endpoints.

## API Endpoint Guide

### Create User

- **Method:** `POST`
- **URL:** `/user`

#### Success Response

**Status Code:** `201 Created`

```json
{
  "message": "user is created"
}
```

---

### Get User

- **Method:** `GET`
- **URL:** `/user/{user_id}`

#### Example Request

```http
GET /user/1
```

#### Success Response

**Status Code:** `200 OK`

```json
{
  "userName": "harsh",
  "address": "wse"
}
```

---

#### User Not Found

Example request:

```http
GET /user/2
```

Response:

**Status Code:** `404 Not Found`

```json
{
  "detail": "user is not present"
}
```

## Why Use `HTTPException`?

Using `HTTPException` offers several advantages:

- Returns proper HTTP error status codes.
- Provides meaningful error messages to API clients.
- Stops endpoint execution immediately when an error occurs.
- Follows REST API best practices.
- Automatically integrates with FastAPI's generated API documentation.

## Summary

This chapter demonstrates how FastAPI handles HTTP responses and exceptions. It shows how to return appropriate HTTP status codes using the `status_code` parameter and how to raise `HTTPException` for error scenarios. Proper status codes and exception handling make APIs more reliable, easier to understand, and compliant with RESTful standards.
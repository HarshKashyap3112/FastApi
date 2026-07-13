# FastAPI Middleware Example

This is a simple FastAPI application that demonstrates how middleware works in FastAPI, including its use cases and how it's utilized by routes.

## Overview

This application is a basic FastAPI server with HTTP middleware that demonstrates state management and request processing flow.

## Code Structure

### File: `main.py`

The application consists of a FastAPI app with the following components:

1. **Middleware**: An HTTP middleware that sets state on the request object
2. **Routes**: Two endpoints that demonstrate how middleware affects request processing

## How Middleware Works in FastAPI

### What is Middleware?

Middleware in FastAPI is a function that intercepts HTTP requests and responses, allowing you to:

- Modify requests before they reach your route handlers
- Add custom logic that runs before and after route execution
- Store state that can be accessed by multiple routes
- Perform logging, authentication, validation, or other cross-cutting concerns

### How Middleware is Registered

```python
@app.middleware("http")
async def middlewareFunction(request: Request, call_next):
    # Logic before route handler
    response = await call_next(request)
    # Logic after route handler
    return response
```

- The `@app.middleware("http")` decorator registers the function as HTTP middleware
- FastAPI will execute this middleware for every HTTP request
- The middleware receives the request and must call `call_next()` to continue to the next middleware or route handler

### Execution Flow

1. **Request enters** FastAPI
2. **Middleware runs** (your code in `middlewareFunction`)
   - This example sets `request.state.user = "admin"`
3. **Route handler executes**
   - The `/` route returns a simple message
   - The `/auth` route reads `request.state.user`
4. **Middleware runs again** (after route handler)
5. **Response returns** to client

## Use Cases for FastAPI Middleware

### 1. Authentication & Authorization
```python
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    token = request.headers.get("authorization")
    if not token:
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})
    request.state.user = decode_token(token)
    response = await call_next(request)
    return response
```

### 2. Request/Response Logging
```python
import time
from datetime import datetime

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Add custom headers to response
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Request-ID"] = generate_request_id()
    
    return response
```

### 3. Database Connection Management
```python
@app.middleware("http")
async def db_middleware(request: Request, call_next):
    request.state.db = get_db_connection()
    try:
        response = await call_next(request)
        return response
    finally:
        request.state.db.close()
```

### 4. CORS (Cross-Origin Resource Sharing)
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 5. Rate Limiting
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RequestOverLimit, rate_limit_handler)

@app.middleware("http")
@limiter.limit("5/minute")
async def rate_limit_middleware(request: Request, call_next):
    response = await call_next(request)
    return response
```

## How Middleware is Used by Routes

### Accessing Middleware State

Routes can access data stored by middleware through the `request.state` object:

```python
@app.get("/auth")
def getUser(request: Request):
    # This can set by middleware
    return request.state.user
```

### Why Use `request.state`?

- **Shared Data**: Allows state to be shared across middleware and routes
- **Request-Scoped**: State lives for the duration of a single request
- **Type Safe**: FastAPI provides type hints for request.state
- **No Global State**: Avoids issues with concurrent requests

### Practical Example

In the provided code, the middleware sets `request.state.user = "admin"`, and the `/auth` route reads this value:

```python
@app.middleware("http")
async def middlewareFunction(request: Request, call_next):
    request.state.user = "admin"  # Set by middleware
    response = await call_next(request)
    return response

@app.get("/auth")
def getUser(request: Request):
    return request.state.user  # Accessible in route
```

## Running the Application

To run this application:

1. Ensure you have FastAPI and Uvicorn installed:
   ```bash
   pip install fastapi uvicorn
   ```

2. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

3. Test the endpoints:
   - `GET /`: Returns "{ \"message\": \"this is home route\" }"
   - `GET /auth`: Returns \"admin\" (set by middleware)

## Key Takeaways

1. **Middleware is executed for every request** before and after route handlers
2. **Use `request.state`** to pass data from middleware to routes
3. **Middleware is your best friend** for cross-cutting concerns
4. **Always call `call_next()`** to continue the request flow
5. **Middleware provides a clean way** to add consistent logic across all routes

## Advanced Middleware Techniques

### Custom Exception Handling Middleware
```python
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

@app.middleware("http")
async def exception_handler_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": e.detail})
```

### Conditional Middleware Execution
```python
@app.middleware("http")
async def conditional_middleware(request: Request, call_next):
    # Only run for specific paths
    if request.url.path.startswith("/api"):
        # Process API requests
        response = await call_next(request)
        return response
    # Skip middleware for other requests
    response = await call_next(request)
    return response
```

This example demonstrates the basic concept of FastAPI middleware and shows how it can be used for various common patterns in web applications.
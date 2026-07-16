# FastAPI API Router Example

This is a simple FastAPI application that demonstrates how API routers work in FastAPI, including its use cases and how modular route organization improves code maintainability.

## Overview

This application showcases FastAPI's router feature, which allows you to organize your API endpoints into modular, reusable components. Each router handles a specific domain or functionality.

## Code Structure

The application consists of:

1. **Main Application (`main.py`)**: Entry point that initializes FastAPI and includes routers
2. **Calculator Sub-app (`calculator/` directory)**: Modular routers for mathematical operations
   - `addition.py`: Handles addition operations
   - `substraction.py`: Handles subtraction operations

## How API Routers Work in FastAPI

### What is an API Router?

An API router in FastAPI is a way to:

- Organize your API routes into logical groups
- Create reusable, modular components
- Separate concerns by functionality
- Maintain cleaner, more organized code
- Share common prefix paths across multiple endpoints

### How Routers are Created

```python
from fastapi import APIRouter

router = APIRouter(prefix="/add")  # Optional prefix for all routes

@router.post("/")
def home(a: int, b: int):
    return a + b
```

### How Routers are Included

```python
from fastapi import FastAPI
from calculator import addition, substraction

app = FastAPI()
app.include_router(addition.router)  # Include addition routes
app.include_router(substraction.router)  # Include subtraction routes
```

### Execution Flow

1. **Request enters** FastAPI
2. **All included routers are processed**
3. **Matching route finds the appropriate handler**
4. **Response returns** to client

## Use Cases for FastAPI API Routers

### 1. Modular Organization

```python
# calculator/operations.py - Mathematical operations
# auth/routes.py - Authentication endpoints
# users/routes.py - User management
# products/routes.py - Product catalog
```

### 2. Common Path Sharing

```python
# Router with shared prefix
router = APIRouter(prefix="/api/v1")

@router.get("/users")     # Becomes GET /api/v1/users
@router.get("/products")  # Becomes GET /api/v1/products
```

### 3. Reusability

```python
# Create a router once and use it in multiple apps
additional_app.include_router(auth.router)
cms_app.include_router(auth.router)
payment_app.include_router(auth.router)
```

### 4. Tag-Based Documentation

```python
router = APIRouter(
    prefix="/add",
    tags=["addition"]  # Groups in OpenAPI docs
)
```

## Accessing Router Benefits

### Why Use API Routers?

- **Organized Code**: Related routes stay together
- **Clean Separation**: Different domains in separate modules
- **Reusable Components**: Use same router in multiple apps
- **Better Documentation**: Routes grouped in OpenAPI UI
- **Scalable Design**: Easy to add new features
- **Team Collaboration**: Multiple developers can work on different routers

### Practical Example

In the provided code, routers organize functionality:

```python
# main.py
from fastapi import FastAPI
from calculator import addition, substraction

app = FastAPI()
app.include_router(addition.router)  # /add/
app.include_router(substraction.router)  # /sub/

# Available endpoints:
# POST /add/ -> Addition
# POST /sub/ -> Subtraction
```

## Router Configuration Options

### 1. Prefix

```python
router = APIRouter(prefix="/api/v1")
# All routes get /api/v1 prefix
```

### 2. Tags

```python
router = APIRouter(
    tags=["mathematics"],
    responses={404: {"description": "Not found"}}
)
```

### 3. Dependencies

```python
from fastapi import Depends, HTTPException

def verify_api_key():
    # Common authentication for all routes in this router
    pass

@app.get("/")
def add(a: int, b: int, api_key: str = Depends(verify_api_key)):
    return a + b
```

## Running the Application

To run this application:

1. Ensure you have FastAPI installed:
   ```bash
   pip install fastapi uvicorn
   ```

2. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

3. Test the endpoints:
   - `POST /add/` - Returns addition of two numbers
   - `POST /sub/` - Returns subtraction of two numbers

## Working with Multiple Routers

When including multiple routers, FastAPI searches them in the order they're included:

```python
# Order matters!
app.include_router(user.router)
app.include_router(product.router)
```

If two routes match the same path, the first one included wins.

## Advanced Router Techniques

### Router Subclassing

```python
from fastapi import APIRouter
from fastapi.responses import JSONResponse

class CustomRouter(APIRouter):
    def add_api_route(self, path, endpoint, **kwargs):
        # Add custom logic for all routes in this router
        kwargs["responses"] = {500: {"description": "Server error"}}
        super().add_api_route(path, endpoint, **kwargs)

router = CustomRouter(prefix="/add")
```

### Conditional Router Inclusion

```python
# Include routers only when needed
def setup_app(include_auth=True, include_payment=False):
    app = FastAPI()
    
    if include_auth:
        app.include_router(auth.router)
    if include_payment:
        app.include_router(payment.router)
    
    return app
```

## Key Takeaways

1. **Routers promote modular design** - Keep related routes together
2. **Use prefixes for common paths** - Avoid repetition
3. **Tags improve documentation** - Group related endpoints
4. **Routers are reusable** - Same logic can power multiple apps
5. **Inclusion order matters** - First matching route wins
6. **Dependencies can be shared** - Apply common logic to all routes
7. **Start with small routers** - Can grow into full-featured sub-applications

This example demonstrates the basics of FastAPI's router feature and shows how it enables clean, maintainable API design.
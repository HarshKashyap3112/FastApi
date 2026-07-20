# FastAPI JWT Authentication Example

This is a simple FastAPI application that demonstrates JWT (JSON Web Token) authentication and authorization using OAuth 2.0, including its implementation and how it's used by routes.

## Overview

This application is a basic FastAPI server with JWT-based authentication that demonstrates:
- User login with username/password
- JWT token generation and validation
- Protected routes using token authentication
- Token-based user authentication flow

## Code Structure

### File: `main.py`

The application consists of a FastAPI app with the following components:

1. **Authentication Endpoints**: `/login` for obtaining access tokens
2. **Protected Route**: `/profile` for accessing authenticated user data
3. **Token Validation**: Helper function to decode and validate JWT tokens
4. **User Database**: In-memory storage with two dummy users

## JWT Authentication Flow in FastAPI

### What is JWT Authentication?

JWT (JSON Web Token) authentication is a stateless authentication mechanism that:

- Uses a small self-contained token to represent user identity
- Passes user information securely between client and server
- Is widely used in modern web applications and APIs
- Includes username, expiration time, and other claims

### Authentication Process

1. **User Login**: User submits username and password to `/login`
2. **Token Generation**: Server creates a JWT with user information
3. **Token Storage**: Client stores and sends the token in subsequent requests
4. **Token Validation**: Server validates the token before allowing access
5. **Route Protection**: Protected routes reject requests without valid tokens

## Code Structure

### 1. Setup and Configuration

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from pydantic import BaseModel

# FastAPI app instance
app = FastAPI()

# JWT configuration
secret_key = "mysecretkey"  # Used to sign tokens
ALGORITHM = 'HS256'         # Hashing algorithm
Oath_scheme = OAuth2PasswordBearer(tokenUrl="login")
```

### 2. Dummy User Database

```python
fake_users = {
    "harsh": {
        "username": "harsh",
        "age": 24,
        "password": "1234"
    },
    "ravi": {
        "username": "ravi don",
        "age": 23,
        "password": "4567"
    }
}
```

### 3. Login Endpoint

```python
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Authenticate user credentials
    user = fake_users.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate JWT token
    token = jwt.encode(
        {"sub": form_data.username},  # Contains username
        secret_key,
        algorithm=ALGORITHM
    )
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }
```

### 4. Token Validation

```python
async def get_user(token: str = Depends(Oath_scheme)):
    try:
        # Decode and verify the token
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[ALGORITHM]
        )
        username = payload["sub"]  # Extract username from token
        return username
    except:
        raise HTTPException(401, "Invalid authentication")
```

### 5. Protected Route

```python
@app.get("/profile")
def get_profile(currentUser: str = Depends(get_user)):
    return {
        "message": f"Welcome {currentUser}"
    }
```

## How JWT Authentication Works in FastAPI

### Authentication Flow

1. **Send login request**: User sends username and password to `/login`
2. **Get access token**: Server returns JWT token for successful login
3. **Access protected routes**: Client stores and sends token in requests
4. **Automatic validation**: FastAPI validates token on protected routes
5. **Get user info**: Authenticated user information is available in routes

### Key Components Used

- **OAuth2PasswordBearer**: Automatically extracts token from Authorization header
- **jwt.encode**: Creates signed JWT tokens
- **jwt.decode**: Validates and decodes JWT tokens
- **Depends**: FastAPI's dependency injection for reusable authentication logic

## Testing the Application

### Steps to Run:

1. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn python-jose[cryptography]
   ```

2. **Run the application**:
   ```bash
   uvicorn main:app --reload
   ```

3. **Test the endpoints**:

   - **Login (get token)**:
     ```bash
     curl -X POST http://localhost:8000/login \
          -H "Content-Type: application/x-www-form-urlencoded" \
          --data "username=harsh&password=1234"
     ```

   - **Access profile (with token)**:
     ```bash
     curl -X GET http://localhost:8000/profile \
          -H "Authorization: Bearer <your_token_here>"
     ```

   - **Access without token**:
     ```bash
     curl -X GET http://localhost:8000/profile
     # Returns 401 error (Unauthorized)
     ```

## Why JWT Authentication?

1. **Stateless**: No server-side session storage needed
2. **Self-contained**: All user info in the token
3. **Mobile friendly**: Easy to store in mobile apps
4. **Standard**: Widely supported across platforms
5. **Fast**: Simple validation with built-in cryptographic checks

## Security Considerations

- **Secret Key**: Keep your secret key secure and never expose it
- **Short-lived tokens**: Use short expiration times
- **HTTPS**: Always use HTTPS in production
- **Token refresh**: Implement token refresh for long sessions
- **Secure storage**: Store tokens securely on the client side

## Key Takeaways

1. **JWT tokens are stateless** - all user data is in the token itself
2. **Dependency injection** - reuse authentication logic across routes
3. **FastAPI security** - built-in support for OAuth 2.0 and JWT
4. **Automatic validation** - FastAPI handles token extraction and validation
5. **Protected routes** - easily create secure endpoints using `Depends()`

This example demonstrates how to implement secure authentication using JWT tokens in FastAPI, providing a foundation for building authenticated APIs.

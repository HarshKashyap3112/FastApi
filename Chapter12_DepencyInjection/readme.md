# 📘 Chapter 12: Dependency Injection

In this chapter, we explore how to use **Dependency Injection (DI)** in FastAPI. Dependency Injection allows you to share dependencies across multiple route handlers, making it perfect for common tasks like authentication, database connections, and reusable business logic. By defining dependencies once and using them in multiple routes, you promote code reusability and clean architecture. When you access a dependency through FastAPI, the dependency is resolved exactly once per request and will be provided to dependent functions automatically.

---

## 🗂️ Project Structure

```
Chapter12_DepencyInjection/
└── main.py
```

---

## 🔑 Key Concepts

### 1. Independent vs. Dependent Functions

FastAPI provides two ways to define and use dependencies:

#### Independent Functions
Functions that can be used as dependencies without receiving special parameters:

```python
def independentFunction():
    return {"message":"i am independent function "}
```

This function returns a simple message and can be injected into any route handler.

---

#### Dependent Functions
Functions that require parameters extracted from the request (like headers, query params, etc.):

```python
def verifyToken(token:str = Header(None)):
    if token != "mysecrettoken":
        raise HTTPException(
            status_code=418,
            detail="Unauthorized access"
        )
    return{"message":"access granted"}
```

This function validates a JWT token from the `Authorization` header and returns a success message.

---

### 2. Using @app.get("/home") with Independent Dependency

Route handlers can use independent functions as dependencies to share common logic:

```python
@app.get("/home")
def dependentFunction(data= Depends(independentFunction)):
    return data
```

The `independentFunction` is called once per request and its return value is passed to `dependentFunction`.

---

### 3. Using @app.get('/profile') with Authentication Dependency

Real-world applications often require authentication for certain routes:

```python
@app.get('/profile')
def getProfile(check = Depends(verifyToken)):
    check.update({'user':"harsh"})
    return check
```

The `verifyToken` dependency:
- Extracts the token from the `Authorization` header
- Validates the token against a secret key
- Returns a success response if valid
- The profile route uses this result and adds additional user data

This pattern ensures that only authenticated users can access protected routes.

---

### 4. The Depends Parameter

The `Depends()` function marks a dependency, telling FastAPI:
1. **Where to look for the dependency** (function, class, or callable)
2. **How to resolve it** (FastAPI calls it with the appropriate parameters extracted from the request)
3. **What to pass to the dependent function** (the return value of the dependency)

All dependencies in a route are resolved before the route handler and passed automatically to their respective parameters.

---

## ▶️ Running the App

Start the development server from the `Chapter12_DepencyInjection` directory:

```bash
python main.py
```

This will start FastAPI with auto-reload enabled on http://127.0.0.1:8000.

---

## 🌐 Available Endpoints

| Method | Endpoint      | Description                                 |
| ------ | ------------- | ------------------------------------------- |
| GET    | `/home`       | Returns message from independent function   |
| GET    | `/profile`    | Returns authenticated user profile          |

---

## 🧪 Try It Out

Once the server is running, test these endpoints:

- 🏠 Home → [http://127.0.0.1:8000/home](http://127.0.0.1:8000/home)
- 🔐 Profile → [http://127.0.0.1:8000/profile](http://127.0.0.1:8000/profile) *(with Authorization: Bearer mysecrettoken header)*
- 📄 Interactive Docs → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

The Profile endpoint requires the `Authorization` header with `mysecrettoken` to work.

---

## 📝 Summary

| Concept | What You Learned |
| -------- | :--- |
| **Independent Dependencies** | Functions without request params used as injectable dependencies |
| **Dependent Dependencies** | Functions extracting request data (headers, query params) as dependencies |
| **@app.get() Injection** | Use `Depends()` to share dependency results across routes |
| **Authentication Patterns** | Build protected routes using dependencies like token verification |
| **Dependency Reuse** | Define logic once and use it in multiple endpoints |

---

**Next up → Master more complex dependency injection patterns with parametrized dependencies! 🚀**

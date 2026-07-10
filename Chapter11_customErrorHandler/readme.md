# 📘 Chapter 11: Custom Error Handler

In this chapter, we explore how to **handle custom exceptions** in FastAPI. Instead of using standard HTTP error codes (like 400, 404) for all error conditions, we'll create custom exception classes to provide more detailed error information and handle error cases in a flexible way.

---

## 🗂️ Project Structure

```
Chapter11_customErrorHandler/
└── main.py
```

---

## 🔑 Key Concepts

### 1. What Is a Custom Exception Handler?

FastAPI allows you to create **custom exception classes** and register **custom exception handlers** using the `@app.exception_handler()` decorator. This enables you to:

- Define specific error types beyond standard HTTP exceptions
- Provide detailed error messages and structured responses
- Handle error cases with custom logic and status codes

When an exception is raised in your route, FastAPI automatically converts it to a JSON response. By registering a custom exception handler, you can control this conversion to suit your needs.

---

### 2. Creating a Custom Exception Class

To create a custom exception, define a class that inherits from Python's `Exception` class:

```python
class unicornException(Exception):
    def __init__(self, name: str):
        self.name = name
```

This approach allows you to store custom properties (like the `name` field) and provides a clear way to represent application-specific errors.

---

### 3. Registering Custom Exception Handlers

To handle your custom exceptions, use the `@app.exception_handler()` decorator. This decorator registers a function that will be called when the specified exception is raised:

```python
@app.exception_handler(unicornException)
async def unicorn_exception_handler(request: Request, exc: unicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something wrong. Yikes!"},
    )
```

The handler receives the request and exception object, allowing you to:
- Set the appropriate HTTP status code (418 in this example, which means "I'm a teapot")
- Format error messages using exception properties
- Return structured JSON error responses

---

### 4. Using Custom Exceptions in Routes

Custom exceptions are raised like any other exception in your route functions:

```python
@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "voldemort":
        raise unicornException(name=name)
    return {"unicorn_name": name}
```

This creates a deliberate error condition for the "voldemort" unicorn, demonstrating how FastAPI will trigger your custom exception handler.

---

## ▶️ Running the App

Start the development server from the `Chapter11_customErrorHandler` directory:

```bash
uvicorn main:app --reload
```

The `--reload` flag enables auto-restart when code changes are detected.

---

## 🌐 Available Endpoints

| Method | Endpoint      | Description                                 |
| ------ | ------------- | ------------------------------------------- |
| GET    | `/`           | Returns a welcome message                   |
| GET    | `/unicorns/{name}` | Returns unicorn name or raises exception if name is "voldemort" |

---

## 🧪 Try It Out

Once the server is running, try these URLs in your browser:

- 🏠 Home → [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- 🦄 Unicorn Harry → [http://127.0.0.1:8000/unicorns/harry](http://127.0.0.1:8000/unicorns/harry) *(returns JSON response)*
- 🦄\ud83d\ude31 Unicorn Voldemort → [http://127.0.0.1:8000/unicorns/voldemort](http://127.0.0.1:8000/unicorns/voldemort) *(triggers 418 error with custom message)*
- 📄 Interactive Docs → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

The Voldemort request triggers your custom exception handler, returning a 418 status code with a custom error message: {"message": "Oops! voldemort did something wrong. Yikes!"}

---

## 📝 Summary

| Concept | What You Learned |
| -------- | :--- |
| **Custom Exception Classes** | Define application-specific errors extending Exception with custom properties |
| **Exception Handlers** | Use `@app.exception_handler()` to convert exceptions to structured JSON responses |
| **Status Code Control** | Set custom HTTP status codes instead of standard FastAPI error codes |
| **Error Messages** | Create detailed error messages using exception properties |
| **Route Logic** | Raise exceptions in route handlers to trigger custom error handling |

---

**Next up → Learn to handle validation errors in database integration scenarios! 🚀**

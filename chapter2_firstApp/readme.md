# 📘 Chapter 2: Your First FastAPI Application

In this chapter, we build a simple FastAPI app with multiple routes to understand the basics of how FastAPI works.

---

## 🗂️ Project Structure

```
chapter2_firstApp/
└── main.py
```

---

## 🔑 Key Concepts

### 1. Creating a FastAPI Instance

Every FastAPI project starts by creating an app instance:

```python
from fastapi import FastAPI

app = FastAPI()
```

- `FastAPI()` creates the core application object.
- All routes are registered on this `app` instance.

---

### 2. Defining Routes with Decorators

FastAPI uses **decorators** to map URL paths to Python functions.

```python
@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}
```

| Part              | Meaning                                      |
| ----------------- | -------------------------------------------- |
| `@app.get("/")`   | Handles **GET** requests to the `/` path     |
| `def home()`      | The function that runs when the route is hit  |
| `return {...}`    | FastAPI automatically converts it to **JSON** |

---

### 3. Multiple Routes

You can define as many routes as you need:

```python
@app.get("/about")
def about():
    return {"message": "About Page"}
```

Each route has:
- A **path** (e.g., `/about`)
- An **HTTP method** (e.g., `GET`)
- A **handler function** that returns a response

---

### 4. Returning JSON Data

FastAPI automatically serializes Python **dicts** and **lists** into JSON responses.

```python
@app.get("/users")
def users():
    return [
        {"name": "Abdul", "age": 25},
        {"name": "Ali", "age": 22},
        {"name": "Ahmed", "age": 23}
    ]
```

> 💡 No need to manually call `json.dumps()` — FastAPI handles it for you!

---

## ▶️ Running the App

```bash
uvicorn main:app --reload
```

---

## 🌐 Available Endpoints

| Method | Endpoint   | Description               |
| ------ | ---------- | ------------------------- |
| GET    | `/`        | Returns a welcome message |
| GET    | `/about`   | Returns about page info   |
| GET    | `/users`   | Returns a list of users   |

---

## 🧪 Try It Out

Once the server is running, visit these URLs in your browser:

- 🏠 Home → [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- ℹ️ About → [http://127.0.0.1:8000/about](http://127.0.0.1:8000/about)
- 👥 Users → [http://127.0.0.1:8000/users](http://127.0.0.1:8000/users)
- 📄 API Docs → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📝 Summary

| Concept              | What You Learned                                    |
| -------------------- | --------------------------------------------------- |
| `FastAPI()`          | Creates the application instance                    |
| `@app.get(path)`     | Registers a GET route                               |
| Return `dict`/`list` | Automatically converted to JSON                     |
| Uvicorn              | ASGI server used to run FastAPI apps                |
| `/docs`              | Auto-generated interactive API documentation        |

---

**Next up → Chapter 3! 🚀**

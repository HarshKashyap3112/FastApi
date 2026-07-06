# 📘 Chapter 3: Dynamic Routes (Path Parameters)

In this chapter, we learn how to create **dynamic routes** in FastAPI using **path parameters** — allowing a single route to handle multiple URLs.

---

## 🗂️ Project Structure

```
Chapter3_dynamicRoutes/
└── main.py
```

---

## 🔑 Key Concepts

### 1. What Are Dynamic Routes?

Instead of creating a separate route for every user (e.g., `/user/1`, `/user/2`, `/user/3`), we define **one route with a variable** in the path:

```python
@app.get("/user/{user_id}")
def user(user_id: int):
    return {"message": "hello this is user " + str(user_id)}
```

- `{user_id}` is a **path parameter** — it captures whatever value appears in that part of the URL.
- The value is automatically passed as an argument to the function.

---

### 2. Type Validation

FastAPI uses Python **type hints** to automatically validate path parameters:

```python
def user(user_id: int):
```

| URL              | Result                                          |
| ---------------- | ----------------------------------------------- |
| `/user/42`       | ✅ Works — `user_id = 42`                       |
| `/user/hello`    | ❌ Error — `"hello"` is not a valid integer      |

> 💡 If you pass an invalid type, FastAPI returns a **422 Unprocessable Entity** error with a clear message — no extra code needed!

---

### 3. Running with `uvicorn.run()`

Instead of running `uvicorn` from the command line, you can configure it directly in your script:

```python
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
```

| Parameter  | Purpose                                         |
| ---------- | ----------------------------------------------- |
| `main:app` | Module `main` and FastAPI instance `app`        |
| `host`     | IP address to bind the server to                |
| `port`     | Port number (here `5000` instead of default `8000`) |
| `reload`   | Auto-restart server when code changes           |

Now you can simply run:

```bash
python main.py
```

---

### 4. Debugging with `print()`

You can add `print()` statements inside route handlers to debug in the terminal:

```python
@app.get("/user/{user_id}")
def user(user_id: int):
    print("this is user route")
    return {"message": "hello this is user " + str(user_id)}
```

> 💡 The `print()` output appears in the **terminal** where the server is running, not in the browser.

---

## ▶️ Running the App

**Option 1** — Using Python directly:

```bash
python main.py
```

**Option 2** — Using Uvicorn CLI:

```bash
uvicorn main:app --host 127.0.0.1 --port 5000 --reload
```

---

## 🌐 Available Endpoints

| Method | Endpoint          | Description                             |
| ------ | ----------------- | --------------------------------------- |
| GET    | `/`               | Returns the home page message           |
| GET    | `/user/{user_id}` | Returns a greeting for the given user ID |

---

## 🧪 Try It Out

Once the server is running, visit these URLs in your browser:

- 🏠 Home → [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
- 👤 User 1 → [http://127.0.0.1:5000/user/1](http://127.0.0.1:5000/user/1)
- 👤 User 42 → [http://127.0.0.1:5000/user/42](http://127.0.0.1:5000/user/42)
- ❌ Invalid → [http://127.0.0.1:5000/user/hello](http://127.0.0.1:5000/user/hello) *(triggers 422 error)*
- 📄 API Docs → [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs)

---

## 📝 Summary

| Concept                | What You Learned                                          |
| ---------------------- | --------------------------------------------------------- |
| `{param}` in path      | Captures dynamic values from the URL                     |
| Type hints (`int`)     | Automatic validation and type conversion                  |
| `uvicorn.run()`        | Run the server programmatically with custom config        |
| `print()` in handlers  | Debug route execution in the terminal                     |
| 422 Error              | FastAPI auto-validates and rejects invalid parameter types |

---

**Next up → Chapter 4! 🚀**

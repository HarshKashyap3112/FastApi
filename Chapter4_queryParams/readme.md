# 📘 Chapter 4: Query Parameters

In this chapter, we learn how to use **query parameters** in FastAPI. Query parameters are key-value pairs that appear after the `?` in a URL, used to filter, sort, or configure the request.

---

## 🗂️ Project Structure

```
Chapter4_queryParams/
└── main.py
```

---

## 🔑 Key Concepts

### 1. What Are Query Parameters?

When you declare function parameters that are not part of the path parameters, FastAPI automatically interprets them as **query parameters**.

For example, in the URL:
`http://127.0.0.1:8000/users?name=harsh`

- The query parameter is `name` with the value `"harsh"`.

---

### 2. Optional Parameters and Default Values

You can make query parameters optional by assigning default values (like `None`):

```python
@app.get("/users")
def user(name: str = None):
    return {
        "user": name
    }
```

If a client visits `/users` without the `name` parameter, it defaults to `None`. If they visit `/users?name=harsh`, then `name` will be `"harsh"`.

---

### 3. Multiple Query Parameters and Type Validation

FastAPI can handle multiple query parameters simultaneously and automatically validate their types based on Python type hints:

```python
@app.get("/products")
def product(name: str = None, price: float = None, quantity: int = None):
    return {
        "name": name,
        "price": price,
        "quantity": quantity
    }
```

FastAPI handles:
- **Type Conversion:** Converts query strings to Python types (`float`, `int`, etc.).
- **Validation:** If the client provides an invalid type (e.g., `price=free`), FastAPI automatically responds with a **422 Unprocessable Entity** error.

---

## ▶️ Running the App

Run the Uvicorn server from the `Chapter4_queryParams` directory:

```bash
uvicorn main:app --reload
```

- `main:app` refers to the `main.py` file and the `app` instance of FastAPI.
- `--reload` enables auto-reload so the server restarts when code changes.

---

## 🌐 Available Endpoints

| Method | Endpoint | Query Parameters | Description |
| :--- | :--- | :--- | :--- |
| GET | `/` | None | Returns a basic greeting. |
| GET | `/users` | `name` (str, optional) | Returns the name of the user. |
| GET | `/products` | `name` (str, optional)<br>`price` (float, optional)<br>`quantity` (int, optional) | Returns product info with validation. |

---

## 🧪 Try It Out

Once the server is running, try visiting these URLs:

- 🏠 Home → [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- 👤 User Query → [http://127.0.0.1:8000/users?name=Harsh](http://127.0.0.1:8000/users?name=Harsh)
- 🛍️ Product Query → [http://127.0.0.1:8000/products?name=Haldi&price=220&quantity=1](http://127.0.0.1:8000/products?name=Haldi&price=220&quantity=1)
- ❌ Validation Error → [http://127.0.0.1:8000/products?price=invalid](http://127.0.0.1:8000/products?price=invalid) *(triggers 422 Error)*
- 📄 Interactive Docs → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📝 Summary

| Concept | What You Learned |
| :--- | :--- |
| **Query Params** | Parameters defined in function signatures that aren't in the path. |
| **Optional Params** | Defined by setting default values like `= None`. |
| **Data Validation** | FastAPI enforces type safety and conversions (e.g. `int`, `float`). |
| **Automatic Docs** | Query parameters are automatically documented in the `/docs` UI. |

---

**Next up → Combine Path and Query Parameters! 🚀**

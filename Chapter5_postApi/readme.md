# 📘 Chapter 5: POST API & Request Bodies (Pydantic)

In this chapter, we explore how to receive and process complex structured data sent by a client using **POST requests** and **Request Bodies** validated by **Pydantic** models.

---

## 🗂️ Project Structure

```
Chapter5_postApi/
└── main.py
```

---

## 🔑 Key Concepts

### 1. GET vs. POST
- **GET:** Used to retrieve data. Data is passed in the URL (via path parameters or query parameters). It has length constraints and is not suitable for sensitive data like passwords.
- **POST:** Used to send/create data. Data is sent in the **HTTP request body** (usually as JSON). It can handle large, complex, nested data structures and is much more secure for sensitive information.

---

### 2. What is Pydantic?
FastAPI uses **Pydantic** under the hood for data parsing and validation. By defining a Pydantic model, you describe the shape and constraints of the data your API expects. 

FastAPI will automatically:
1. **Read** the body of the request as JSON.
2. **Convert** the JSON types to Python types.
3. **Validate** the data (checks if types match and required fields are present).
4. **Generate** OpenAPI/Swagger schema documentation for the model.

---

### 3. Creating a Pydantic Model

To define a request body schema, import `BaseModel` from `pydantic` and create a class that inherits from it:

```python
from pydantic import BaseModel

class user(BaseModel):
    name: str
    email: str
    password: str
```
- Every attribute declared in the model is **required** by default.
- If a client sends a request missing any of these keys or with mismatched types, FastAPI automatically returns a `422 Unprocessable Entity` response.

---

### 4. Receiving the Pydantic Model in a Route

To declare a request body, declare it as a parameter in your route function using the Pydantic model type:

```python
@app.post('/user')
def user_login(user_data: user):
    return {
        "message": "this is user data ",
        "data": user_data
    }
```
- FastAPI recognizes that `user_data` has the type `user` (a subclass of `BaseModel`) and automatically parses it from the request body.
- You can access fields directly in Python (e.g., `user_data.name`, `user_data.email`).

---

## ▶️ Running the App

Start the development server using Uvicorn:

```bash
uvicorn main:app --reload
```

- `main:app` targets the `app` object in `main.py`.
- `--reload` enables auto-reload on file edits.

---

## 🌐 Available Endpoints

| Method | Endpoint | Request Body | Description |
| :--- | :--- | :--- | :--- |
| **GET** | `/` | *None* | Simple verification greeting. |
| **POST** | `/user` | `JSON (user model)` | Accepts user credentials, validates them, and returns them in the response. |

---

## 🧪 Testing the POST Endpoint (How to Test)

Since web browsers send **GET** requests by default when visiting a URL, you cannot test a POST API simply by typing the URL into the browser address bar. Instead, use one of the following methods:

### Method 1: Swagger UI (Recommended 🚀)
FastAPI auto-generates interactive documentation at `/docs`:
1. Go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.
2. Expand the `POST /user` endpoint block.
3. Click the **"Try it out"** button.
4. Modify the request body JSON:
   ```json
   {
     "name": "Harsh Kashyap",
     "email": "harsh@example.com",
     "password": "securepassword123"
   }
   ```
5. Click **"Execute"**. You will see the server's JSON response!

### Method 2: cURL (Terminal)
Run this command in a separate terminal:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/user' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Harsh Kashyap",
  "email": "harsh@example.com",
  "password": "securepassword123"
}'
```

---

## 📝 Relearn & Cheat Sheet

### Parameters Cheat Sheet
| Parameter Type | Where is it in the HTTP Request? | Declared in FastAPI function | Use Case |
| :--- | :--- | :--- | :--- |
| **Path Parameter** | inside the URL path (e.g., `/user/{id}`) | Defined inside the route path decorator | Identifying a specific resource. |
| **Query Parameter** | at the end of URL after `?` (e.g., `?name=x`) | Declared as function arguments *not* in the path | Filtering, sorting, page pagination. |
| **Request Body** | inside the HTTP payload/body (as JSON) | Declared as a Pydantic `BaseModel` argument | Creating/updating records with complex data structures. |

### Validation Errors (422 Unprocessable Entity)
If you send a request body with missing details:
```json
{
  "name": "Harsh Kashyap"
}
```
FastAPI will automatically return:
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": ["body", "password"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

**Next up → Learn to store data in databases or handle response models! 🚀**

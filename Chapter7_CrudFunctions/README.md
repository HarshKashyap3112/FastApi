# Chapter 7: CRUD Functions in FastAPI

This folder contains a complete implementation of a **CRUD (Create, Read, Update, Delete)** application using **FastAPI** and **Pydantic**. 

The application implements an in-memory database to store a list of books and exposes RESTful API endpoints to manage them.

---

## 📂 Folder Structure
* [main.py](file:///d:/FastApi/Chapter7_CrudFunctions/main.py): The main application file containing the FastAPI instance, Pydantic schema, in-memory data store, and CRUD path operations.

---

## 🛠️ Tech Stack & Concepts Covered
1. **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python.
2. **Pydantic (`BaseModel`)**: For data validation, parsing, and OpenAPI schema generation.
3. **HTTP Operations**:
   * `GET`: Retrieve resources.
   * `POST`: Create a new resource.
   * `PUT`: Update an existing resource.
   * `DELETE`: Remove a resource.
4. **In-Memory Store**: A standard Python list (`BOOKS`) to simulate a lightweight database.

---

## 📝 Code Walkthrough

### 1. The Pydantic Data Model
We define a schema using Pydantic's [BaseModel](https://docs.pydantic.dev/latest/api/base_model/) to validate the structure of the data sent in requests and returned in responses:
```python
class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
```

### 2. In-Memory Database
A simple Python list to store our book objects:
```python
BOOKS = []
```

### 3. API Endpoints (CRUD)

#### 🟢 Read Welcome Path
* **Method**: `GET`
* **Path**: `/`
* **Description**: Returns a welcome message: `{"message": "this is book app"}`.

#### 🟢 Read All Books (Retrieve)
* **Method**: `GET`
* **Path**: `/books`
* **Description**: Returns the entire `BOOKS` list.

#### 🟢 Read Single Book by ID (Retrieve)
* **Method**: `GET`
* **Path**: `/books/{book_id}`
* **Description**: Iterates through `BOOKS` to find a match for the specified `book_id`. Returns the book if found, or `{"message": "book not found"}` otherwise.

#### 🔵 Create a Book (Create)
* **Method**: `POST`
* **Path**: `/books`
* **Description**: Accepts a request body matching the `Book` model, appends it to the `BOOKS` list, and returns the added book.

#### 🟡 Update a Book (Update)
* **Method**: `PUT`
* **Path**: `/books/{book_id}`
* **Description**: Searches for a book with `book_id`. If found, updates its `title`, `author`, and `year` with the payload from `updated_book`, and returns the updated book.

#### 🔴 Delete a Book (Delete)
* **Method**: `DELETE`
* **Path**: `/books/{book_id}`
* **Description**: Searches for the book with `book_id`, removes it from the `BOOKS` list, and returns a success message.

---

## 🚀 How to Run the Application

### 1. Start the Uvicorn Server
Make sure you are in the project root or the `Chapter7_CrudFunctions` directory, then run:
```bash
uvicorn main:app --reload
```
*(Note: If you run it from the workspace root, you may need to specify the path as `uvicorn Chapter7_CrudFunctions.main:app --reload`)*

### 2. Explore the Interactive API Documentation
FastAPI automatically generates interactive Swagger and ReDoc documentation:
* **Interactive UI (Swagger)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **Static UI (ReDoc)**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

You can use the **Swagger UI** to test the endpoints directly by clicking **"Try it out"**, filling in JSON payloads, and executing requests.

# 🚀 FastAPI Installation Guide

A step-by-step guide to set up and run your first FastAPI project.

---

## Step 1: Create a Project Directory

Create a new directory for your FastAPI project and navigate into it.

```bash
mkdir fastapi-project
cd fastapi-project
```

---

## Step 2: Create a Virtual Environment

Create an isolated Python virtual environment to manage your project dependencies.

```bash
python -m venv venv
```

---

## Step 3: Activate the Virtual Environment

Activate the virtual environment before installing any packages.

**Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

> ✅ You should see `(venv)` at the beginning of your terminal prompt once activated.

---

## Step 4: Install FastAPI and Uvicorn

Install FastAPI along with Uvicorn (an ASGI server to run your app).

```bash
pip install fastapi uvicorn
```

---

## Step 5: Create `main.py`

Create the main application file in your project directory.

```bash
touch main.py
```

Or on **Windows**:
```powershell
New-Item main.py
```

---

## Step 6: Write Boilerplate Code

Open `main.py` and add the following starter code:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

---

## Step 7: Start the Server Using Uvicorn

Run the development server with auto-reload enabled.

```bash
uvicorn main:app --reload
```

- `main` → the file `main.py`
- `app` → the FastAPI instance inside `main.py`
- `--reload` → auto-restarts on code changes (development only)

> 🌐 Open your browser and visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)
>
> 📄 Interactive API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

**Happy coding! 🎉**

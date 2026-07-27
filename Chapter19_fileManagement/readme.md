# FastAPI File Management — A Beginner-Friendly Guide

> **Goal of this chapter:** Learn how to upload files to a FastAPI server, understand *why* each piece of code exists, and what every term means. Read this like a tutorial: each section explains a concept, then shows the matching code, then tells you what to observe.

---

## 1. What Are We Building?

A tiny web app that does two things:

1. Shows you a web page with a **file picker** (so you can choose a file from your computer).
2. Receives the file you selected and **saves it on the server** inside an `uploads/` folder.

That's it. But to build it, we touch several important FastAPI ideas:

| Concept | One-line meaning |
|---------|------------------|
| `FastAPI()` | The app object that holds all your routes |
| `UploadFile` | A class that represents an uploaded file |
| `File(...)` | A dependency telling FastAPI "this parameter is a file, not JSON" |
| `aiofiles` | A library for **non-blocking** (async) file writing |
| `Path` | A tool from Python's standard library to work with file paths safely |

---

## 2. The Complete Code

Here is the full `main.py` we will study line by line:

```python
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, UploadFile, File
import aiofiles
from pathlib import Path

app = FastAPI()


# Define the upload directory and ensure it exists
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.post("/uploadfiles/")
async def upload_file(file: UploadFile = File(...)):
    # Generate the file path
    file_path = UPLOAD_DIR / file.filename

    try:
        # Asynchronously open and write the file
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()      # Read file content
            await out_file.write(content)    # Write to disk
    except Exception as e:
        return {"error": f"File save failed: {str(e)}"}

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "location": str(file_path)
    }


@app.get("/")
async def main():
    content = """
    <body>
    <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
    <input name="file" type="file">
    <input type="submit">
    </form>
    </body>
    """
    return HTMLResponse(content=content)
```

---

## 3. Imports — What Each One Is For

```python
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, UploadFile, File
import aiofiles
from pathlib import Path
```

- **`HTMLResponse`** — By default FastAPI returns JSON. When we want to return raw HTML (our upload form), we wrap it in `HTMLResponse` so the browser renders it as a page instead of showing JSON text.
- **`FastAPI`** — The framework's main class. We create one instance: `app = FastAPI()`.
- **`UploadFile`** — A special class that represents the file the client sends. It gives you helpful attributes like `.filename` and methods like `.read()`.
- **`File`** — A "dependency" used as a default value (`File(...)`) that tells FastAPI: *"expect a file in the request body, not a normal field."* The `...` means "required."
- **`aiofiles`** — Normally `open()` blocks the program while writing. `aiofiles.open()` lets us `await` the write, freeing the server to handle other requests meanwhile. This matters because our function is `async`.
- **`Path`** — From Python's `pathlib`. It builds file paths in a way that works on Windows, Linux, and Mac (no manual slashes).

---

## 4. Creating the Upload Folder

```python
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
```

- `Path("uploads")` describes a folder named `uploads` next to the script.
- `.mkdir(exist_ok=True)` creates it. The `exist_ok=True` part is important: if the folder already exists, Python **does not throw an error**. Without it, the second time you run the app it would crash.

**Why do this at the top (module level)?** So the folder is guaranteed to exist before any upload request arrives.

---

## 5. The Upload Endpoint

```python
@app.post("/uploadfiles/")
async def upload_file(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename
    ...
```

### 5.1 Route decorator `@app.post("/uploadfiles/")`
This means: "when a client sends an **HTTP POST** to the URL `/uploadfiles/`, run the function below." We use POST (not GET) because the client is *sending data* to the server.

### 5.2 `async def`
Marks the function as **asynchronous**. It can `await` slow operations (like reading/writing files) without freezing the whole server.

### 5.3 `file: UploadFile = File(...)`
This is the heart of file uploads:
- `UploadFile` is the *type* of the parameter.
- `File(...)` is what makes FastAPI look for an uploaded file in the request.
- `file.filename` is the original name of the file on the client's computer (e.g., `"photo.png"`).

### 5.4 Building the destination path
```python
file_path = UPLOAD_DIR / file.filename
```
We join the uploads folder with the file name using `/` (the `Path` operator). Result: `uploads/photo.png`.

---

## 6. Saving the File Asynchronously

```python
try:
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()   # (1)
        await out_file.write(content) # (2)
except Exception as e:
    return {"error": f"File save failed: {str(e)}"}
```

Step by step:

1. **`async with aiofiles.open(file_path, 'wb')`**
   - `'wb'` means **w**rite in **b**inary mode. Binary is required because files (images, PDFs, etc.) are not plain text.
   - `async with` ensures the file is automatically closed when done, even if an error happens.

2. **`content = await file.read()`**
   - Reads the entire uploaded file into memory as bytes.
   - `await` lets the server do other work while the data is being read.

3. **`await out_file.write(content)`**
   - Writes those bytes to disk without blocking the event loop.

4. **`try / except`**
   - If anything goes wrong (no disk space, permission error, etc.), we return a friendly error message instead of crashing with a 500 error.

---

## 7. The Success Response

```python
return {
    "message": "File uploaded successfully",
    "filename": file.filename,
    "location": str(file_path)
}
```

FastAPI automatically converts this dictionary into **JSON**. The client receives confirmation plus the saved file name and its location on the server.

---

## 8. The HTML Upload Form

```python
@app.get("/")
async def main():
    content = """<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
    <input name="file" type="file">
    <input type="submit"></form>"""
    return HTMLResponse(content=content)
```

Why do we need this? So you can test uploads from a browser without writing a separate client.

Key HTML attributes explained:

- **`action="/uploadfiles/"`** — Where the form sends the data (our upload endpoint).
- **`method="post"`** — Use HTTP POST (matches our route).
- **`enctype="multipart/form-data"`** — **Critical!** This encoding is required for sending files. A normal form (`application/x-www-form-urlencoded`) cannot carry file data correctly.
- **`type="file"`** — Renders a "Choose File" button.
- **`HTMLResponse(...)`** — Sends the string as `text/html` so the browser displays a form instead of showing the raw HTML code.

---

## 9. How a Request Flows (Visual)

```
Browser (you pick a file + click submit)
        |
        |  POST /uploadfiles/  (multipart/form-data)
        v
FastAPI matches @app.post("/uploadfiles/")
        |
        v
upload_file() receives UploadFile
        |
        v
aiofiles writes bytes to uploads/<filename>
        |
        v
JSON {"message": "File uploaded successfully", ...}
        |
        v
Browser shows the confirmation
```

---

## 10. Running the Application

1. Install the requirements:
   ```bash
   pip install fastapi uvicorn aiofiles
   ```

2. Start the server (run this in the `Chapter19_fileManagement` folder):
   ```bash
   uvicorn main:app --reload
   ```
   - `main` = the file `main.py`
   - `app` = the `FastAPI()` instance inside it
   - `--reload` = restart automatically when you edit the code

3. Open your browser at **http://127.0.0.1:8000/**
   - You'll see the upload form.
   - Choose a file and submit.
   - Check the `uploads/` folder — your file should be there!

4. (Optional) Test with the automatic docs at **http://127.0.0.1:8000/docs** using the `POST /uploadfiles/` endpoint and the "Choose File" button.

---

## 11. Key Takeaways

1. **`UploadFile` + `File(...)`** is the standard FastAPI way to accept file uploads.
2. **`enctype="multipart/form-data"`** on the HTML form is mandatory for file uploads.
3. **`aiofiles`** lets you write files inside `async` functions without blocking the server.
4. **`'wb'` (binary write)** mode is needed because uploaded files are raw bytes.
5. **`Path.mkdir(exist_ok=True)`** safely creates the storage folder once at startup.
6. **`try/except`** around file operations prevents ugly crashes and returns clear errors.
7. **`HTMLResponse`** is how you return a web page instead of JSON.

---

## 12. Things to Try / Learn Next

- **Security:** The code saves the file using the client's original name. In real apps, generate a unique name (e.g., `uuid4()`) and validate the extension to avoid overwriting files or accepting dangerous uploads.
- **Streaming:** For very large files, read and write in chunks (`while chunk := await file.read(1024*1024)`) instead of loading the whole file into memory.
- **Limits:** Add a maximum file size check and reject files that are too big.
- **Static files:** Use `StaticFiles` from FastAPI to let users *download* the files they uploaded.
- **Database:** Store file metadata (name, size, upload time) in a database and keep only the path on disk.
```

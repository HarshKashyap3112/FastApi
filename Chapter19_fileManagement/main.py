
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
            content = await file.read()  # Read file content
            await out_file.write(content)  # Write to disk
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
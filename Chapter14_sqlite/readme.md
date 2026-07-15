# FastAPI SQLite Integration

This is a simple FastAPI application that demonstrates how to work with SQLite databases using Python's built-in sqlite3 module.

## Overview

This application demonstrates basic SQLite database integration with FastAPI, including database creation, table setup, and simple API endpoints to interact with the database.

## Code Structure

### File: `main.py`

The application consists of a FastAPI app with the following components:

1. **Database Connection**: Creates a SQLite connection to test.db
2. **Table Creation**: Sets up a todos table with Id, title, and completed fields
3. **Routes**: API endpoints for basic operations

## How SQLite Works in FastAPI

### What is SQLite?

SQLite is a lightweight, serverless, self-contained SQL database engine. It's commonly used in FastAPI applications for simple data storage needs because it's:

- **Embeddable**: Can be included directly in your application
- **Serverless**: Doesn't require a separate database server
- **Zero-Configuration**: No setup required
- **ACID Compliant**: Ensures data integrity

### Database Setup in FastAPI

```python
import sqlite3
from fastapi import FastAPI

app=FastAPI()
conn=sqlite3.Connection("test.db",check_same_thread=False)
cursor=conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS todos(
    Id INTEGER PRIMARY KEY,
    title TEXT,
    completed TEXT
    )
""")
conn.commit()
```

### Execution Flow

1. **Connection** establishes a connection to test.db
2. **Table Creation** creates a todos table if it doesn't exist
3. **Routes** provide access to the database

## Common Use Cases for SQLite with FastAPI

### 1. **Testing & Development**
Perfect for development and testing due to its simplicity and zero-configuration nature.

### 2. **Small Applications**
Ideal for applications that don't need the full power of a client-server database system.

### 3. **File-Based Storage**
Good for applications where the entire database needs to be stored in a single file.

## How the Application Works

### Database Schema

The application creates a `todos` table with:

- **Id**: INTEGER PRIMARY KEY (auto-incrementing)
- **title**: TEXT (the todo item description)
- **completed**: TEXT (status of completion)

### Routes

- `GET /`: Returns a confirmation message that the database has been created

## Running the Application

To run this application:

1. Ensure you have FastAPI installed:
   ```bash
   pip install fastapi uvicorn
   ```

2. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

3. Test the endpoint:
   - `GET /`: Returns "{ \"message\": \"database is created \" }"

## Key Takeaways

1. **SQLite is great for small apps**: Simple, fast, and requires no setup
2. **Connection management**: Use `check_same_thread=False` for FastAPI's async nature
3. **Database initialization**: Tables can be created directly in code for development
4. **File-based persistence**: SQLite stores data in a single .db file

## Adding More Database Features

### Adding New Todo Items

You can easily extend this to support CRUD operations:

```python
@app.post("/todos")
def create_todo(request: Request):  # Add todo to database
    return {"message": "TODO implemented"}

@app.get("/todos/{todo_id}")  
def read_todo(todo_id: int):  # Get specific todo
    return {"message": "TODO implemented"}

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int):  # Update todo
    return {"message": "TODO implemented"}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):  # Delete todo
    return {"message": "TODO implemented"}
```

## Best Practices for SQLite with FastAPI

1. **Connection Pooling**: Use connection pooling for higher throughput
2. **Transaction Management**: Implement proper transaction handling
3. **Error Handling**: Add try-catch blocks around database operations
4. **Thread Safety**: Configure `check_same_thread` appropriately for your environment
5. **Data Validation**: Validate data before inserting into the database

## When to Choose SQLite vs Other Databases

Choose SQLite when:
- You need a simple, file-based database
- You're developing or testing an application
- Database size is small to medium
- You prefer zero-configuration setup
- You need ACID compliance in a single file

Choose other databases when:
- You need high concurrency
- You need complex joins and queries
- You need robust concurrent access from multiple processes
- Your application is in production with many users

## Performance Considerations

1. **Read Performance**: Excellent for read-heavy workloads
2. **Write Performance**: Adequate for moderate write loads
3. **Memory Usage**: Minimal memory footprint
4. **Disk Usage**: Single file with compact storage

This example demonstrates the basic concept of FastAPI integration with SQLite databases and shows how to set up database connections and work with SQL data in a FastAPI application.

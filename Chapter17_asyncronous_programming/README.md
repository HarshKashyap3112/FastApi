# FastAPI Asynchronous Programming

This FastAPI application demonstrates asynchronous programming concepts in Python and FastAPI, showing the differences between async and synchronous code patterns.

## Overview

This chapter explores FastAPI's asynchronous programming model, demonstrating how async/await works in practice. You'll learn how a single-threaded event loop can handle multiple users simultaneously, how each incoming request gets its own coroutine, and how the event loop manages concurrent operations while waiting for I/O operations like database queries and external API calls.

## Key Learning Points

While learning FastAPI's asynchronous programming model, I was confused about how async and await work. I initially thought await either stopped the entire server or allowed the code below it to execute immediately. I also struggled to understand how a single-threaded event loop could handle multiple users simultaneously, how each incoming request gets its own coroutine, and how the event loop pauses and resumes coroutines while waiting for I/O operations such as database queries or external API calls. Through this, I learned the difference between blocking a thread and pausing a coroutine, and how FastAPI achieves high concurrency using Python's asyncio event loop.

## Code Structure

### File: `main.py`

The application consists of:

1. **Async Example**: `GET /home` - Demonstrates async programming with non-blocking operations
2. **Sync Example**: `GET /new` - Demonstrates traditional blocking code
3. **Comments**: Educational comments explaining async vs sync concepts

## Async vs Sync Programming

### Async Programming

Async programming uses coroutines and an event loop to achieve high concurrency. Unlike traditional thread-based concurrency, where each thread can only execute one task at a time (though multiple threads can run in parallel), async programming allows a single thread to manage multiple tasks concurrently by pausing execution at certain points (like I/O operations) and resuming when the I/O completes.

```python
from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

@app.get("/home")
async def asyncCode():
    a = await asyncio.sleep(3, "this is 3 sec delay")
    return a
```

**Async Example Key Points**:

1. **Non-blocking**: `await asyncio.sleep(3)` doesn't block the event loop
2. **Pauses execution**: The coroutine pauses while waiting for the sleep to complete
3. **Resumes when ready**: When the sleep finishes, the coroutine resumes
4. **Allows concurrency**: Multiple async operations can run simultaneously

### Sync Programming

Traditional synchronous programming blocks the thread during I/O operations, making it less efficient for I/O-bound tasks.

```python
def newFunction():
    time.sleep(20)
    return {"message": "this is 20 sec delay "}
```

**Sync Example Key Points**:

1. **Blocking**: `time.sleep(20)` blocks the entire thread
2. **Cannot handle other requests** while sleeping
3. **Inefficient** for I/O-bound operations
4. **Stops server processing** other requests

## How Async/Await Works

### The Event Loop

The asyncio event loop is the heart of async programming:

1. **Runs in single thread** but manages many concurrent tasks
2. **Schedules coroutines** (functions marked as async)
3. **Pauses** when a coroutine hits `await`
4. **Resumes** when the awaited operation completes
5. **Switches** to other ready coroutines

### Coroutines

Each HTTP request gets its own coroutine:

```python
@app.get("/home")
async def asyncCode():
    # Each request creates a new coroutine
    a = await asyncio.sleep(3, "this is 3 sec delay")
    return a
```

**Coroutine Lifecycle**:

1. **Created**: When request comes in
2. **Runs**: Starts executing until first `await`
3. **Pauses**: At `await` point, returns control to event loop
4. **Waits**: Event loop runs other coroutines
5. **Resumes**: When awaited operation completes
6. **Completes**: Coroutine finishes and returns result

### Blocking vs Pausing

**Blocking** (Synchronous):
- Thread is locked
- Cannot run other code
- Other requests must wait
- Heavy resource usage

**Pausing** (Asynchronous):
- Thread remains free
- Other tasks can run
- Request queue continues
- Efficient resource usage

## Practical Benefits

### 1. High Concurrency

With sync programming, one 20-second blocking operation would prevent all other requests from being processed:

```python
@app.get("/new")
def newFunction():
    time.sleep(20)  # Blocks everything!
    return {"message": "this is 20 sec delay "}
```

With async programming:

```python
@app.get("/home")
async def asyncCode():
    a = await asyncio.sleep(3, "this is 3 sec delay")
    return a
```

Multiple users can make requests simultaneously, and the server can handle them efficiently even while waiting for I/O.

### 2. Database Queries

Async database operations allow the server to handle requests while waiting for database responses:

```python
async def get_from_db():
    # This won't block the event loop
    result = await db_connection.fetch_one("SELECT * FROM users")
    return result
```

### 3. External API Calls

Making HTTP requests to external APIs without blocking:

```python
import aiohttp

async def get_external_data():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.example.com/data") as response:
            return await response.json()
```

## Why Use Async?

### Scenarios Where Async Shines

1. **I/O-bound operations**: Database queries, HTTP requests, file operations
2. **High concurrency**: Web servers handling many simultaneous requests
3. **Real-time applications**: Chat apps, live updates, streaming
4. **Resource efficiency**: One thread can handle thousands of concurrent connections

### Performance Benefits

1. **Reduced resource usage**: One async thread vs multiple threads
2. **Better throughput**: More requests per second
3. **Better scalability**: Handles more concurrent users
4. **Faster response times**: Concurrent processing vs sequential

## Running the Application

To run this application:

1. Ensure you have all required packages installed:

```bash
pip install fastapi uvicorn
```

2. Run the application:

```bash
uvicorn main:app --reload
```

3. Test the endpoints:

- `GET /home` - Returns result after 3-second async delay
- `GET /new` - Returns result after 20-second blocking delay

## Testing Async vs Sync

### With 10 Simultaneous Requests

**Async Version**:
- All 10 requests complete in ~3 seconds
- Server remains responsive
- No queuing delays

**Sync Version**:
- Requests complete in ~200 seconds
- Server becomes unresponsive
- Extreme queuing

### Browser Testing

You can test this by:

1. Opening multiple browser tabs
2. Making simultaneous requests to `/home` (async) and `/new` (sync)
3. Observing response times
4. Noticing server responsiveness with async vs sync endpoints

## Key Takeaways

1. **Async = Pausing**: `await` pauses execution, blocks nothing
2. **Event Loop**: Manages many concurrent tasks in one thread
3. **High Concurrency**: Single thread can handle thousands of requests
4. **Blocking vs Non-blocking**: Sync blocks, async pauses
5. **I/O Bound**: Async shines for network/disk operations
6. **Scalability**: Better performance with more users
7. **Server Responsiveness**: Async keeps server responsive during I/O
8. **Modern Web**: Essential for high-performance web applications

## Advanced Topics

### Mixing Sync and Async

When using synchronous libraries in async applications:

```python
from concurrent.futures import ThreadPoolExecutor

def blocking_function():
    # Synchronous code
    return expensive_operation()

async def async_wrapper():
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, blocking_function)
        return result
```

### Error Handling in Async

Async error handling is similar to sync but needs async context:

```python
@app.get("/home")
async def asyncCode():
    try:
        a = await asyncio.sleep(3, "this is 3 sec delay")
        return a
    except Exception as e:
        return {"error": str(e)}
```

### Best Practices

1. **Use async for I/O operations**: HTTP, database, file operations
2. **Keep sync functions simple**: For CPU-bound operations
3. **Handle errors properly**: Use try/except in async contexts
4. **Test concurrency**: Simulate multiple requests
5. **Monitor performance**: Track response times and resource usage
6. **Use fast I/O libraries**: aiofiles, aiohttp, async databases

This example demonstrates the fundamentals of FastAPI's asynchronous programming model and how it enables high-concurrency web applications while maintaining server responsiveness.

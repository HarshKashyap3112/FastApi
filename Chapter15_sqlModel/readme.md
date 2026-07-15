# FastAPI SQLModel Integration

This FastAPI application demonstrates how to use SQLModel (an SQL toolkit built on SQLAlchemy) for database interactions with SQLite.

## Overview

This advanced FastAPI application showcases SQLModel integration, providing a complete CRUD (Create, Read, Update, Delete) API for managing Hero entities. SQLModel combines the power of SQLAlchemy with Pydantic's data validation capabilities.

## Code Structure

### File: `main.py`

The application consists of a FastAPI app with the following components:

1. **Data Models**: Hero class with fields (id, name, age, secret_name)
2. **Database Setup**: SQLite engine and session management
3. **Event Handler**: Automatic database table creation on startup
4. **API Endpoints**: Complete CRUD operations for Hero entities

## How SQLModel Works in FastAPI

### What is SQLModel?

SQLModel is an open-source library that provides:

- **SQLAlchemy Integration**: Full database ORM capabilities
- **Pydantic Validation**: Automatic data validation with Pydantic models
- **Type Hints**: Native Python type hints for database columns
- **FastAPI Native**: Seamless integration with FastAPI dependency injection

### Key Features

1. **Model Definition**: Define database models as Python classes
2. **Automatic Validation**: Pydantic validation is built-in
3. **Database Operations**: CRUD operations through SQLAlchemy sessions
4. **Dependency Injection**: FastAPI sessions as dependencies

### Database Model Example

```python
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str
```

## SQLModel vs Traditional SQLAlchemy

### SQLModel Advantages

1. **Simplicity**: Less boilerplate code
2. **Validation**: Built-in Pydantic validation
3. **Type Safety**: Native Python type support
4. **FastAPI Integration**: Works seamlessly with FastAPI dependencies
5. **Automatic CRUD**: Easier implementation of basic operations

### When to Use SQLModel

- **Rapid Development**: Need quick database setup
- **RESTful APIs**: Clean validation and serialization
- **Small to Medium Apps**: Balancing simplicity with power
- **FastAPI Users**: Native FastAPI integration
- **Projects with Validations**: Need built-in data validation

## Complete CRUD API Implementation

### 1. Create Hero (`POST /heroes/`)

```python
@app.post("/heroes/")
def create_hero(hero: Hero, session: SessionDep) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero
```

**Features**:
- Automatically validates input data using Pydantic
- Uses FastAPI dependency injection for database sessions
- Returns the created hero with its generated ID
- Handles database persistence and refresh

### 2. Read All Heroes (`GET /heroes/`)

```python
@app.get("/heroes/")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes
```

**Features**:
- Pagination support with offset/limit
- Built-in validation for limit (max 100)
- Efficient querying with SQLAlchemy
- Returns list of Hero objects

### 3. Read Single Hero (`GET /heroes/{hero_id}`)

```python
@app.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: SessionDep) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero
```

**Features**:
- Efficient by-primary-key lookup
- Proper 404 handling with HTTP exceptions
- Returns single Hero object

### 4. Delete Hero (`DELETE /heroes/{hero_id}`)

```python
@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
```

**Features**:
- Clean deletion with proper error handling
- Returns success confirmation
- Proper transaction management

## Database Setup in SQLModel

### Connection Configuration

```python
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)
```

### Session Management

```python
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
```

### Startup Event

```python
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
```

## Running the Application

To run this application:

1. Ensure you have all required packages installed:
   ```bash
   pip install fastapi uvicorn sqlmodel
   ```

2. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

3. Test the endpoints:
   - `GET /heroes/`: Returns all heroes (empty initially)
   - `POST /heroes/`: Create a new hero (send JSON)
   - `GET /heroes/{id}`: Get specific hero by ID
   - `DELETE /heroes/{id}`: Delete hero by ID

## SQLModel vs Raw SQLite

### SQLModel Benefits

1. **Model Definition**: Define entities as Python classes
2. **Validation**: Built-in data validation with Pydantic
3. **Type Safety**: Native Python type hints
4. **Relationships**: Easy to define relationships
5. **Query Builder**: Powerful SQL query construction
6. **Connection Management**: Built-in session handling

### Performance Considerations

1. **Overhead**: Slightly more overhead than raw SQLite
2. **Flexibility**: Greater flexibility in data modeling
3. **Validation**: Added validation costs
4. **Query Generation**: More sophisticated query generation

## Best Practices for SQLModel with FastAPI

### 1. Model Definition Best Practices
```python
class Hero(SQLModel, table=True):
    # Use Field() for additional column options
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, description="Hero's name")
    age: int | None = Field(default=None, index=True) 
    secret_name: str = Field(min_length=1)  # Built-in validation
```

### 2. Session Management
- Use dependency injection for consistent session handling
- Implement proper error handling around database operations
- Consider connection pooling for production apps

### 3. Validation and Security
- Leverage Pydantic's built-in validation
- Use query parameters for input validation
- Implement proper error handling for database exceptions

### 4. Error Handling
```python
if not hero:
    raise HTTPException(status_code=404, detail="Hero not found")
```

### 5. Query Optimization
- Use indexes for frequently queried fields
- Implement pagination for list endpoints
- Use proper typing for better IDE support

## Key Takeaways

1. **SQLModel simplifies development** by combining SQLAlchemy and Pydantic
2. **FastAPI integration** is seamless with dependency injection
3. **Type hints** provide better IDE support and validation
4. **Model-based approach** makes code more maintainable
5. **Validation is built-in** with Pydantic
6. **Database operations** are cleaner with session management

## Advanced SQLModel Techniques

### 1. Relationships Between Models

```python
class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    heroes: list[Hero] = Relationship(back_populates="team")

class Hero(SQLModel, table=True):
    # ... other fields ...
    team_id: int | None = Field(default=None, foreign_key="team.id")
    team: Team = Relationship(back_populates="heroes")
```

### 2. Advanced Querying

```python
# Filters with relationships
heroes = session.exec(
    select(Hero).where(Hero.age > 30).join(Team)
).all()

# Complex aggregations
from sqlalchemy import func
team_stats = session.exec(
    select(Team.name, func.count(Hero.id))
    .join(Hero)
    .group_by(Team.name)
).all()
```

### 3. Custom Validators

```python
from pydantic import field_validator

class Hero(SQLModel, table=True):
    # ... other fields ...
    
    @field_validator('age')
    @classmethod
    def validate_age(cls, v):
        if v is not None and v < 0:
            raise ValueError('Age cannot be negative')
        return v
```

This example demonstrates how to use SQLModel to create a robust, type-safe, and validated database-driven FastAPI application with complete CRUD functionality.

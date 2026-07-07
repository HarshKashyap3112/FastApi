from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()
#in memory database
BOOKS=[]

class Book(BaseModel):
    id:int
    title:str
    author:str
    year:int

@app.get("/")
def read_root():
    return {"message":"this is book app"}

#read the books
@app.get("/books")
def get_books():
    return BOOKS

#create the book
@app.post("/books")
def create_book(book:Book):
    BOOKS.append(book)
    return book

@app.put("/books/{book_id}")
def update_book(book_id:int,updated_book:Book):
    for book in BOOKS:
        if book.id==book_id:
            book.title=updated_book.title
            book.author=updated_book.author
            book.year=updated_book.year
            return book
    return {"message":"book not found"}

#delete the book
@app.delete("/books/{book_id}")
def delete_book(book_id:int):
    for book in BOOKS:
        if book.id==book_id:
            BOOKS.remove(book)
            return {"message":"book deleted"}
    return {"message":"book not found"}

#get book by id 
@app.get("/books/{book_id}")
def get_book(book_id:int):
    for book in BOOKS:
        if book.id==book_id:
            return book
    return {"message":"book not found"}

    
from fastapi import FastAPI , HTTPException


app = FastAPI()


@app.get("/test")
def test():
    return {"message": "Hello, World!"}


@app.get("/add")
def add(a: int, b: int):
    return {"result": a + b}


from pydantic import BaseModel, Field , EmailStr , HttpUrl
from datetime import date


class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float = None
    
@app.post("/items/")
def create_item(item: Item):
    return {"item": item}



class User(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    age: int = Field(gt=0 ,le=100)
    github_url: HttpUrl = None
    enrollment_date: str = date
    full_name: str = None
    skills : list[str] = Field(min_length=1, max_length=10)

@app.post("/users/")
def create_user(user: User):
    return {"user": user}



books= {
    1:{
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "price": 10.99
    },
    2:{
        "id": 2,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",                 
        "price": 12.99
    },
    3:{
        "id": 3,
        "title": "1984",
        "author": "George Orwell",
        "price": 9.99
    }
}


class Book(BaseModel):
    title: str  
    author: str
    price: float
 
@app.post("/books/")    
def create_book(book: Book):
    new_id = max(books.keys()) +1
    
    books[new_id] = {
        "id": new_id,
        "title": book.title,
        "author": book.author,
        "price": book.price
    }
    return {"message": "Book created successfully", "book": books[new_id]}



@app.get("/books/{book_id}")
def get_book(book_id: int):
    book = books.get(book_id)
    if book:
        return {"book": book}
    else:
        return {"message": "Book not found"}, 404
    

@app.put("/books/{book_id}")
def replace_book(book_id: int, book: Book):
    if book_id in books:
        books[book_id] = {
            "id": book_id,
            "title": book.title,
            "author": book.author,
            "price": book.price
        }
        return {"message": "Book replaced successfully", "book": books[book_id]}
    else:
        return {"message": "Book not found"}, 404
    

from typing import Optional

class bookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None

@app.patch("/books/{book_id}")
def update_book(book_id: int, book: bookUpdate):
    if book_id not in books:
       raise HTTPException(status_code=404, detail="Book not found")
    update_data = book.model_dump(
        exclude_unset=True
    )
    
    books[book_id].update(update_data)
    return {"message": "Book updated successfully", "book": books[book_id]}

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    if book_id in books:
        del books[book_id]
        return {"message": "Book deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Book not found")
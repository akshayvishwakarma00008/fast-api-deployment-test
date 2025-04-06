from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel, Field
from starlette import status
from uuid import UUID, uuid4

app = FastAPI()

BOOKS = []

class Book:
    id : UUID
    title : str 
    author : str 
    description : str 
    rating : int 
    published_date : int
    
    def __init__(self, id: UUID, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date
        
    
    
class BookRequest(BaseModel):
    id: UUID = Field(default_factory=uuid4) 
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=10, max_length=100)
    published_date: int = Field(gt=1900, lt=2024)
    rating: int = Field(gt=-1, lt=6)
    
    model_config = {
        "json_schema_extra":{
            "example":{
                "title": "A new book",
                "author": "A new book author",
                "description": "A new book description",
                "published_date": 2020,
                "rating": 2
                
            }
        }
    }

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    # if len(BOOKS) < 1:
    #     create_books_no_api()
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read__books(book_id:int):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")
    
@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_books_by_rating(book_rating:int):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
            
    return books_to_return

@app.put("/book/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_id: UUID, book:BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS[i] = BOOKS[i] = Book(**book.model_dump())  
            # return BOOKS[i]
    raise HTTPException(status_code=404, detail="Book not found")
        
            
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if book_id == BOOKS[i].id:
            deleted_book = BOOKS.pop(i)
            # return deleted_book
    raise HTTPException(status_code=404, detail="Book not found")
    
    

@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(new_book)
    return book_request

@app.get("/book/publish/", status_code=status.HTTP_200_OK)
async def get_books_by_published_date(published_date:int):
    books_by_date = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_by_date.append(book)
    return books_by_date

# def create_books_no_api():
#     book1 = Book(
#         id="9510daba-979f-42b1-90bc-204d0e90e706",
#         title="book1",
#         author="author1",
#         description="book1 description",
#         rating="1",
#     )
#     book2 = Book(
#         id="ff716ab9-7e5b-4b9e-a4cc-04072d661d53",
#         title="book2",
#         author="author2",
#         description="book2 description",
#         rating="4",
#     )
#     book3 = Book(
#         id="a60d5219-41bd-4288-b614-e3ccfd7d3bb4",
#         title="book3",
#         author="author3",
#         description="book3 description",
#         rating="10",
#     )
#     book4 = Book(
#         id="294625d0-8d32-473f-846d-05c3fc956705",
#         title="book4",
#         author="author4",
#         description="book4 description",
#         rating="12",
#     )
    
#     BOOKS.append(book1)
#     BOOKS.append(book2)
#     BOOKS.append(book3)
#     BOOKS.append(book4)

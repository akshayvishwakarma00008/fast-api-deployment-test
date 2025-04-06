from fastapi import FastAPI
from enum import Enum
from typing import Optional

app = FastAPI()

BOOKS = {
    'book1':{'title':'Book 1', 'author':'author 1'},
    'book2':{'title':'Book 2', 'author':'author 2'},
    'book3':{'title':'Book 3', 'author':'author 3'},
    'book4':{'title':'Book 4', 'author':'author 4'},
}

class DirectionName(str, Enum):
    north = "NORTH"
    south = "SOUTH"
    east = "EAST"
    west = "WEST"

# @app.get("/direction/{direction}")
# async def get_direction(direction: DirectionName):
#     if direction == DirectionName.north:
#         return {'north':direction , 'msg': "you are on the north"}
#     if direction == DirectionName.south:
#         return {'south':direction , 'msg': "you are on the south"}
#     if direction == DirectionName.east:
#         return {'east':direction , 'msg': "you are on the east"}
#     return {'east':direction , 'msg': "you are on the west"}

@app.get("/")
async def read_all_books():
    return BOOKS
    
    
# @app.get("/books/{book_id}")
# async def read_book(book_id: int):
#     return {'title':book_id}

# #get book detail by name
# @app.get("/{book_name}")
# async def read_book_detail(book_name: str):
#     return BOOKS[book_name]
    
#query parameter
# @app.get("/")
# async def query_book_detail(book_name: Optional[str] = None):
#     if book_name:
#         new_books = BOOKS.copy()
#         del new_books[book_name]
#         return new_books
    
#     return BOOKS
    

#Post - request {using query parameter}
# @app.post("/")
# async def create_book(book_name, book_title, book_author):
#     BOOKS[book_name] = {'title': book_title, 'author': book_author}
#     return BOOKS[book_name]

#Put - request {using quey parameters}
# @app.put("/")
# async def update_book(book_name: str, book_title: str, book_author: str):
#     book_info = {'title': book_title, 'author': book_author}
#     if BOOKS[book_name]:
#         BOOKS[book_name] = book_info
#         return {
#             'statue' : True,
#             'message' : "Book updated successfully",
#             'book' : BOOKS[book_name],
#         }
    
#     return {
#         'status': False,
#         'message': "Enter correct book to update"
#     }
@app.delete("/")
async def delete_book(book_name: str):
    if BOOKS[book_name]:
        del BOOKS[book_name]
        return {
            'statue' : True,
            'message' : "Book deleted successfully",
            'book' : BOOKS,
        }
    
    return {
        'status': False,
        'message': "Enter correct book to delete"
    }
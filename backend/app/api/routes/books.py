from app.api.deps import CurrentUser, SessionDep
import uuid
from typing import Any,List

from fastapi import APIRouter,HTTPException
from sqlmodel import func,select

from app.models import Book,BookCreate,BookPublic,BooksPublic,Message

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/",response_model=BooksPublic)
def read_books(session:SessionDep,)->BooksPublic:
    """
    Retrieve Books.
    """
    count_staementt= select(func.count()).select_from(Book)
    count=session.exec(count_staementt).one()
    book_statement=select(Book)
    books=session.exec(book_statement).all()
    return BooksPublic(data=books,count=count)
    
@router.get("/{book_id}",response_model=BookPublic)
def read_book(session:SessionDep,book_id:uuid.UUID)->BookPublic:  
    """
    Get book by ID.
    """
    book=session.get(Book,book_id)
    if not book:
        raise HTTPException(status_code=404,detail="Book not found")
    return book

@router.post("/",response_model=BookPublic)
def create_book(session:SessionDep,book_in:BookCreate)->Any:
    """
    Create new book.
    """
    book=Book.model_validate(book_in)   
    session.add(book)
    session.commit()
    session.refresh(book)
    return book
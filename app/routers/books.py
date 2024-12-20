from fastapi import Depends, HTTPException , APIRouter, Form, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from app.schemas import BookCreate ,Book, UserCreate, User, UserGet
from app.db.crud import create_book_db , get_book_db , get_books_db, create_user_db, delete_book_db, edit_book_db
from app.db.database import SessionLocal
from starlette.requests import Request
from sqlalchemy.orm import Session
from typing import Annotated

templates = Jinja2Templates(directory="app/templates")

def get_db():
   db = SessionLocal()
   try:
      yield db
   finally:
      db.close()

router = APIRouter()

@router.get("/")
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/books/new/", response_class=HTMLResponse)
async def new_book_form(request: Request):
    return templates.TemplateResponse("create_book.html", {"request": request})

@router.post("/books/delete/{book_id}", response_model=Book, response_class=HTMLResponse)
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    deleted = delete_book_db(db, book_id=book_id)
    if deleted:
        return RedirectResponse(url="/books/", status_code=303)
    else:
        return RedirectResponse(url="/books/", status_code=303)

@router.get("/books/delete/", response_model=list[Book], response_class=HTMLResponse)
async def delete_all_book(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = get_books_db(db, skip=skip, limit=limit)
    return templates.TemplateResponse("book_delete.html", {"request": request, "books": books})
    

@router.post("/books/", response_model=Book)
# def create_book(book: BookCreate, db: Session = Depends(get_db)):
async def create_book(name: str =Form(...), author: str = Form(...), count_page: int = Form(...), db: Session = Depends(get_db)):
    book = BookCreate(name=name, author=author, count_page=count_page)
    create_book_db(db=db, book=book)
    return RedirectResponse(url="/books/", status_code=303)

@router.post("/usres/", response_model=UserGet)
# def create_users(user: User, db: Session = Depends(get_db)):
async def create_users(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = UserCreate(username=username, password=password)
    create_user_db(db=db, user=user)
    return RedirectResponse(url=f"/books/?message=Ви%20увійшли%20як%20{username}", status_code=303)

@router.get("/books/", response_model=list[Book], response_class=HTMLResponse)
async def read_books(request: Request, skip: int = 0, limit: int = 100, message: str = None, db: Session = Depends(get_db)):
    books = get_books_db(db, skip=skip, limit=limit)
    # return books
    if books:
        return templates.TemplateResponse("books.html", {"request": request, "books": books, "message": message})
    else:
        return templates.TemplateResponse("books.html", {"request": request, "books": None, "message": message})

@router.get("/books/{book_id}", response_model=Book, response_class=HTMLResponse)
async def read_book(request: Request, book_id: int, db: Session = Depends(get_db)):
    db_book = get_book_db(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    # return db_book
    return templates.TemplateResponse("book_detail.html", {"request": request, "book": db_book})

@router.get("/new_user/", response_class=HTMLResponse)
async def new_user_form(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})

@router.post("/book/{book_id}", response_model=Book)
async def edit_book(
    book_id: int,
    name: str = Form(...),
    author: str = Form(...),
    count_page: int = Form(...),
    db: Session = Depends(get_db)
):
    book_data = BookCreate(name=name, author=author, count_page=count_page)
    updated_book = edit_book_db(db=db, book_data=book_data, book_id=book_id)
    return RedirectResponse(url="/books/", status_code=303)

@router.get("/book/edit/all/{book_id}", response_class=HTMLResponse)
async def edit_all_book(request: Request, book_id: int, db: Session = Depends(get_db)):
    db_book = get_book_db(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return templates.TemplateResponse("edit_book.html", {"request": request, "book": db_book})
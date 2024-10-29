from sqlalchemy.orm import Session
from . import models
from app import schemas
from passlib.context import CryptContext
import secrets
from app.schemas import UserCreate, Book
from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "19109197bd5e7c289b92b2b355083ea26c71dee2085ceccc19308a7291b2ea06"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_book_db(db: Session, book: schemas.BookCreate):
    db_book = models.Book(name=book.name,author=book.author,count_page=book.count_page)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book

def delete_book_db(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    
    if db_book:
        db.delete(db_book)
        db.commit()
        return True
    else:
        return False


def get_book_db(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books_db(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def create_user_db(db: Session, user: UserCreate):
   salt = secrets.token_hex(16)
  
   hashed_password = get_password_hash(user.password + salt)
   db_user = models.User(username=user.username, password=hashed_password, salt=salt)
   db.add(db_user)
   db.commit()
   db.refresh(db_user)
   return db_user

def get_password_hash(password):
   return pwd_context.hash(password)

def edit_book_db(db: Session, book_data: Book, book_id: int):
    book = get_book_db(db, book_id)
    book.name = book_data.name
    book.author = book_data.author
    book.count_page = book_data.count_page
    db.commit()
    db.refresh(book)
    return book
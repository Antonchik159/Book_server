from app.routers import books
from fastapi import Depends, FastAPI, HTTPException
from app.db import  models
from app.db.database import  engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router=books.router)






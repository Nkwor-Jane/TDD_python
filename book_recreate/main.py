from fastapi import FastAPI
# from routers.book import book_router
from routers.user import user_router

app = FastAPI()

# app.include_router(book_router, tags=["Books"], prefix="/books")
app.include_router(user_router, prefix="/users", tags=["Users"])

@app.get("/")
def home():
    return {"message": "Hello from the books API"}

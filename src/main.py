from fastapi import FastAPI

from src.routers import auth, bookmarks, home

app = FastAPI(title="Bookmarks API")

app.include_router(auth.router)
app.include_router(bookmarks.router)
app.include_router(home.router)

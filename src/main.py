from fastapi import FastAPI

from src.routers import auth, bookmarks, home

app = FastAPI(title="Bookmarks API", summary="This is the summary of the application.",
              description="This is the description of the application.")

app.include_router(auth.router)
app.include_router(bookmarks.router)
app.include_router(home.router)

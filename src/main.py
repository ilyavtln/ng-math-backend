from fastapi import FastAPI
from starlette.responses import RedirectResponse

from src.internal import admin
from src.router import test

app = FastAPI(
    title="Math backend",
    version="1.0.1",
)

@app.get("/")
def main():
    return RedirectResponse("/docs")

# Включаем роутер /api/test
app.include_router(test.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    responses={418: {"description": "I'm a teapot"}},
)

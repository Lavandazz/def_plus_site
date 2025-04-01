import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pages import main_pages

from database.create_db import connect_db, close_db, init_db
from admin_folder import admin, admin_workers


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код для старта приложения
    await connect_db()
    yield  # Приложение работает
    # Код для завершения работы приложения
    await close_db()
app = FastAPI(lifespan=lifespan)
init_db(app)

app.mount("/static", StaticFiles(directory="static"), name="static")  # подключаем статические файлы
app.include_router(main_pages.router)
app.include_router(admin.router)
app.include_router(admin_workers.router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

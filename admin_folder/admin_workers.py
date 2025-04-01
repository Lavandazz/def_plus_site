import os
import shutil

from fastapi import APIRouter, Request, Form, HTTPException, Depends, UploadFile, File
from fastapi import Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from admin_folder.admin_verification import get_current_admin

from database.models_db import WorkerModel

cookie_name = "access_token"
templates = Jinja2Templates(directory="templates/admin_pages")
router = APIRouter()

UPLOAD_DIR = "static/workers_photo"  # Папка для хранения фото


@router.get("/admin/get_workers", response_class=HTMLResponse, tags=["workers_admin"])
async def admin_workers_get(request: Request,
                            ):
    """ Страница админки с данными о сотрудниках"""
    workers = await WorkerModel.all()
    for worker in workers:
        print(worker.photo)  # Посмотрим, что хранится в БД
    return templates.TemplateResponse('workers.html', {"request": request, 'workers': workers})


@router.get('/admin/add_worker', response_class=HTMLResponse, tags=["workers_admin"])
async def admin_dashboard(request: Request, username: str = Depends(get_current_admin)):
    """ Отправление формы для добавления услуги """
    return templates.TemplateResponse("add_worker.html", {
        "request": request, "username": username
    })

@router.post("/admin/add_worker", tags=["workers_admin"])
async def add_worker(name: str = Form(),
                     surname: str = Form(),
                     patronymic: str = Form(),
                     about_worker: str = Form(),
                     photo: UploadFile = File(...),
                     username: str = Depends(get_current_admin)
                    ):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Сохранение файла
    file_path = os.path.join(UPLOAD_DIR, photo.filename)
    print(f'file_path = {file_path}')
    with open(file_path, "wb") as f:
        shutil.copyfileobj(photo.file, f)

    # Сохранение в бд
    worker = await WorkerModel.create(name=name, surname=surname, patronymic=patronymic, about_worker=about_worker,
                                      photo=f"/static/workers_photo/{photo.filename}")
    """Добавление работника"""
    #return HTMLResponse(content="<h1>Работник добавлен</h1>")
    return RedirectResponse(url="/admin/get_workers", status_code=303)


@router.post('/admin/delete_worker/{worker_id}', response_class=HTMLResponse, tags=["workers_admin"])
async def admin_delete_worker(worker_id: int):
    """ Удаление сотрудника """
    try:
        worker = await WorkerModel.get(id=worker_id)  # Ищем сотрудника по id
        print(f'worker id = {worker_id}'
              f'worker name = {worker.name}')
        if worker:
            await worker.delete()  # Удаляем сотрудника
            return RedirectResponse(url='/admin/get_workers', status_code=303)  # Перенаправляем на страницу с сотрудниками
        return {"error": "Услуга не найдена"}  # Если услуга не найдена
    except Exception as e:
        return {"error": f"Произошла ошибка: {e}"}
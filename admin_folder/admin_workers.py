import os
import shutil
from typing import Optional

from fastapi import APIRouter, Request, Form, HTTPException, Depends, UploadFile, File
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
    """ Отправление формы для добавления сотрудника """
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
    """ Добавление (сохранение) сотрудника """
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Сохранение файла
    file_path = os.path.join(UPLOAD_DIR, photo.filename)
    print(f'file_path = {file_path}')
    with open(file_path, "wb") as f:
        shutil.copyfileobj(photo.file, f)
    about = about_worker.capitalize().split('. ')
    about_worker = '. '.join(s.capitalize() for s in about)
    # Сохранение в бд
    worker = await WorkerModel.create(name=name.capitalize().strip(),
                                      surname=surname.capitalize().strip(),
                                      patronymic=patronymic.capitalize().strip(),
                                      about_worker=about_worker.strip(),
                                      photo=f"/static/workers_photo/{photo.filename}")
    """Добавление работника"""
    return RedirectResponse(url="/admin/get_workers", status_code=303)


@router.get('/admin/edit_worker/{worker_id}', response_class=HTMLResponse, tags=["workers_admin"])
async def admin_dashboard(request: Request, worker_id: int, username: str = Depends(get_current_admin)):
    """ Отправление формы для редактирования данных о сотруднике """
    worker = await WorkerModel.get_or_none(id=worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    return templates.TemplateResponse("edit_worker.html", {
        "request": request, "worker": worker, "username": username
    })


@router.post('/admin/save_edit_worker/{worker_id}', response_class=HTMLResponse, tags=["workers_admin"])
async def admin_dashboard(worker_id: int, name: str = Form(...),
                          surname: str = Form(...),
                          patronymic: str = Form(),
                          about_worker: str = Form(...),
                          photo: Optional[UploadFile] = File(None),
                          username: str = Depends(get_current_admin)):
    """ Редактирование (сохранение) данных о сотруднике """
    worker = await WorkerModel.get_or_none(id=worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")

    worker.name = name.capitalize().strip()
    worker.surname = surname.capitalize().strip()
    worker.patronymic = patronymic.capitalize().strip()
    about_worker = about_worker.capitalize().split(". ")
    worker.about_worker = '. '.join(s.capitalize() for s in about_worker).strip()
    print(f'worker.about_worker = {worker.about_worker}')

    if photo and photo.filename:
        os.makedirs(UPLOAD_DIR, exist_ok=True)  # Создай папку, если нужно
        photo_path = os.path.join(UPLOAD_DIR, photo.filename)
        print(f'Сохранение фото сотрудника: {repr(photo_path)}')
        with open(photo_path, "wb") as f:
            shutil.copyfileobj(photo.file, f)
        worker.photo = f"/static/workers_photo/{photo.filename}"

    await worker.save()
    return RedirectResponse(url='/admin/get_workers', status_code=303)


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
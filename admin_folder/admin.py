from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi import Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from admin_folder.admin_verification import get_current_admin
from auth import verify_token, verify_password, create_tokens, hash_password
from database.models_db import ServiceTextModel, AdminModel

cookie_name = "access_token"
templates = Jinja2Templates(directory="templates/admin_pages")
router = APIRouter()


@router.get("/admin/login", response_class=HTMLResponse, tags=["admin"])
async def show_admin_login_page(request: Request):
    """ Отображает страницу входа """
    return templates.TemplateResponse("login.html", {
        "request": request
    })


@router.post("/admin/register")
async def register_admin(name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    """ Регистрация администратора """
    existing_admin = await AdminModel.get_or_none(name=name)
    if existing_admin:
        raise HTTPException(status_code=400, detail="Админ с таким логином уже существует")

    hashed_password = hash_password(password)  # хешируем пароль
    await AdminModel.create(name=name, email=email, password=hashed_password, is_admin=True)

    return {"message": "Админ зарегистрирован"}


@router.post("/admin/login")
async def admin_login(request: Request):
    """ Страница авторизации """
    form_data = await request.form()
    user_admin = form_data.get("user_admin")
    password = form_data.get("password")

    if not user_admin or not password:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Заполните все поля!"})

    admin = await AdminModel.get_or_none(name=user_admin)
    if not admin or not verify_password(password, admin.password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Неверный логин или пароль"})

    # Генерация токенов
    tokens = create_tokens(user_admin)
    response = RedirectResponse(url="/admin", status_code=303)
    response.set_cookie(key="access_token", value=tokens["main_token"], httponly=True)

    return response


@router.get("/admin", response_class=HTMLResponse, tags=["admin"])
async def admin_panel(request: Request, access_token: str = Cookie(None)):  # защищаем взод токеном
    """ Страница админ-панели """
    if not access_token:
        return RedirectResponse(url="/admin/login")  # если нет токена, перенаправление на страницу входа
    try:
        username = verify_token(access_token)  # проверяем токен
    except HTTPException:
        return RedirectResponse(url="/admin/login")  # Если токен недействителен, выкидываем

    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request, "username": username,"active_page": "services"
    })


@router.get("/admin/services", response_class=HTMLResponse, tags=["admin"])
async def admin_services(request: Request, username: str = Depends(get_current_admin)):
    """ Отображение страницы с услугами """
    services = await ServiceTextModel.all()  # получаем все услуги
    return templates.TemplateResponse("admin_services.html", {
        "request": request, "username": username, "services": services
    })


@router.get('/admin/add', response_class=HTMLResponse, tags=["admin"])
async def admin_dashboard(request: Request, username: str = Depends(get_current_admin)):
    """ Отправление формы для добавления услуги """
    return templates.TemplateResponse("add_service.html", {
        "request": request, "username": username
    })


@router.post('/admin_dashboard/add', response_class=HTMLResponse, tags=["admin"])
async def admin_dashboard_add(title: str = Form(...), description: str = Form(...)):
    """ Добавление услуги """
    await ServiceTextModel.create(title=title, description=description)
    return RedirectResponse(url='/admin/services', status_code=303)


@router.get('/admin/edit_service/{service_id}', response_class=HTMLResponse, tags=["admin"])
async def admin_dashboard_edit(request: Request, service_id: int, username: str = Depends(get_current_admin)):
    """ Редактирование услуг """
    service = await ServiceTextModel.get_or_none(id=service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Услуга не найдена")
    return templates.TemplateResponse("edit_service.html", {
        "request": request, "service": service, "username": username
    })


@router.post('/admin/save_edit_service/{service_id}', response_class=HTMLResponse, tags=["admin"])
async def admin_dashboard_edit(service_id: int, title: str = Form(...), description: str = Form(...),
                               username: str = Depends(get_current_admin)):
    """ Редактирование услуг """
    service = await ServiceTextModel.get_or_none(id=service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Услуга не найдена")

    service.title = title
    service.description = description
    await service.save()
    return RedirectResponse(url='/admin/services', status_code=303)


@router.post('/admin_dashboard/delete/{service_id}', response_class=HTMLResponse, tags=["admin"])
async def admin_dashboard_delete(service_id: int):
    """ Удаление услуги """
    try:
        service = await ServiceTextModel.get(id=service_id)  # Ищем услугу по id
        if service:
            await service.delete()  # Удаляем услугу
            return RedirectResponse(url='/admin/services', status_code=303)  # Перенаправляем на страницу с услугами
        return {"error": "Услуга не найдена"}  # Если услуга не найдена
    except Exception as e:
        return {"error": f"Произошла ошибка: {e}"}
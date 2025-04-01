from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database.contacts import contact_dict
from database.models_db import ServiceTextModel, WorkerModel
# from database.about import workers
router = APIRouter()
jinja_env = Jinja2Templates(directory="templates/home")


@router.get("/", response_class=HTMLResponse, tags=["home"], include_in_schema=True)
async def home(request: Request):
    """
    Главная страница
    возвращает HTML-код главной страницы.
    """
    return jinja_env.TemplateResponse("index.html", {"request": request, "title": "Главная"})


@router.get("/about", response_class=HTMLResponse, tags=["home"])
async def about(request: Request):
    """ Страница о нас """
    workers = await WorkerModel.all()
    return jinja_env.TemplateResponse("about.html", {"request": request, "title": "О компании",
                                                     "workers": workers})


@router.get("/services", response_class=HTMLResponse, tags=["home"])
async def services(request: Request):
    """ Страница новостей и услуг"""
    services = await ServiceTextModel.all()
    return jinja_env.TemplateResponse("services.html", {"request": request,
                                                        "services": services})


@router.get("/contacts", response_class=HTMLResponse, tags=["home"])
async def contacts(request: Request):
    """ Страница контактов """
    title = "Контакты ООО 'Дефендер плюс'"
    addresses = contact_dict
    return jinja_env.TemplateResponse("contacts.html", {"request": request,
                                                        "addresses": addresses,
                                                        "title": title})

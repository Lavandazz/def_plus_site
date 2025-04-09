from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database.contacts import contact_dict
from database.models_db import ServiceTextModel, WorkerModel, QuestionAndAnswerModel
from database.contacts import key_features, the_question_why_are_we, list_of_question_why_are_we

router = APIRouter()
jinja_env = Jinja2Templates(directory="templates/home")


@router.get("/", response_class=HTMLResponse, tags=["home"], include_in_schema=True)
async def home(request: Request):
    """
    Главная страница
    возвращает HTML-код главной страницы.
    """
    return jinja_env.TemplateResponse("index.html", {"request": request,
                                                     "title": "Главная",
                                                     "key_features": key_features,
                                                     "list_of_question_why_are_we": list_of_question_why_are_we,
                                                     "the_question_why_are_we": the_question_why_are_we})


@router.get("/about", response_class=HTMLResponse, tags=["home"])
async def about(request: Request):
    """ Страница о нас """
    workers = await WorkerModel.all()
    return jinja_env.TemplateResponse("about.html", {"request": request,
                                                     "title": "О компании",
                                                     "workers": workers})


@router.get("/questions", response_class=HTMLResponse, tags=["home"])
async def questions(request: Request):
    """ Страница с вопросами и ответами """
    questions = await QuestionAndAnswerModel.all()
    title = "Вопросы и ответы банкротство физических лиц"
    return jinja_env.TemplateResponse("questions.html", {"request": request,
                                                         "questions": questions,
                                                         "title": title})


@router.get("/services", response_class=HTMLResponse, tags=["home"])
async def services(request: Request):
    """ Страница новостей и услуг"""
    services = await ServiceTextModel.all()
    title = 'Услуга банкротство, банкротство юридические услуги,  стоимость банкротство физ лица в Москве'
    return jinja_env.TemplateResponse("services.html", {"request": request,
                                                        "title": title,
                                                        "services": services})


@router.get("/contacts", response_class=HTMLResponse, tags=["home"])
async def contacts(request: Request):
    """ Страница контактов """
    contacts_def_plus = 'Контакты ООО "Дефендер плюс"'
    title = "Контакты"
    return jinja_env.TemplateResponse("contacts.html", {"request": request,
                                                        "contact_dict": contact_dict,
                                                        "title": title,
                                                        "contacts_def_plus": contacts_def_plus})

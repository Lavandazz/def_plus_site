from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from database.models_db import ServiceTextModel, WorkerModel, QuestionAndAnswerModel, PhoneModel, AddressModel
from database.contacts import key_features, the_question_why_are_we, list_of_question_why_are_we
from .seo import keywords

router = APIRouter()
jinja_env = Jinja2Templates(directory="templates/home")


@router.get("/", response_class=HTMLResponse, tags=["home"], include_in_schema=True)
async def home(request: Request):
    """
    Главная страница
    возвращает HTML-код главной страницы.
    """
    title = "Банкротство физических лиц, юридические услуги по банкротству"
    description = "Процедура банкротства физ. лиц., юридические услуги по банкротству - Банкротство физических лиц"
    return jinja_env.TemplateResponse("index.html", {"request": request,
                                                     "title": title,
                                                     "keywords": keywords,
                                                     "description": description,
                                                     "key_features": key_features,
                                                     "list_of_question_why_are_we": list_of_question_why_are_we,
                                                     "the_question_why_are_we": the_question_why_are_we})


@router.get("/about", response_class=HTMLResponse, tags=["home"])
async def about(request: Request):
    """ Страница о нас """
    workers = await WorkerModel.all()
    description = "Помощь банкротство Компания Защитник плюс"
    title = "Банкротство физических лиц москва, компания Защитник плюс на карте"
    return jinja_env.TemplateResponse("about.html", {"request": request,
                                                     "title": title,
                                                     "new_title": "О компании",
                                                     "keywords": keywords,
                                                     "description": description,
                                                     "workers": workers})


@router.get("/questions", response_class=HTMLResponse, tags=["home"])
async def questions(request: Request):
    """ Страница с вопросами и ответами """
    all_questions = await QuestionAndAnswerModel.all()
    title = "Вопросы и ответы банкротство физических лиц"
    description = ("Отвечаем на вопросы, связанные с банкротством физических лиц, "
                   "помогаем разобраться с законами на практике.")
    return jinja_env.TemplateResponse("questions.html", {"request": request,
                                                         "all_questions": all_questions,
                                                         "title": title,
                                                         "keywords": keywords,
                                                         "description": description
                                                         })


@router.get("/legalservices", response_class=HTMLResponse, tags=["home"])
async def services(request: Request):
    """ Страница новостей и услуг"""
    all_services = await ServiceTextModel.all()
    description = "Услуга банкротство, сколько стоит банкротство физ лица в Москве, цена процедура банкротства физ лица"
    title = 'Услуга банкротство, банкротство юридические услуги,  стоимость банкротство физ лица в Москве'
    return jinja_env.TemplateResponse("services.html", {"request": request,
                                                        "title": title,
                                                        "keywords": keywords,
                                                        "description": description,
                                                        "all_services": all_services})


@router.get("/contacts", response_class=HTMLResponse, tags=["home"])
async def contacts(request: Request):
    """ Страница контактов """
    contacts_def_plus = 'Контакты ООО "Дефендер плюс"'
    new_title = "Контакты"
    description = "Банкротство физических лиц Москва, Банкротство юридически лиц Москва"
    contact_dict = await PhoneModel.all()
    address_dict = await AddressModel.all()
    return jinja_env.TemplateResponse("contacts.html", {"request": request,
                                                        "contact_dict": contact_dict,
                                                        "address_dict": address_dict,
                                                        "title": new_title,
                                                        "keywords": keywords,
                                                        "description": description,
                                                        "contacts_def_plus": contacts_def_plus})

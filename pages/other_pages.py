from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
jinja_env = Jinja2Templates(directory="templates")


@router.get("/agreement", response_class=HTMLResponse, tags=["other pages"])
async def politics(request: Request):
    """ Страница с политикой конфиденциальности """
    title = "Политика конфиденциальности"
    keywords = "конфиденциальность, обработка, персональных, данных"
    description = ("Положение о политике конфиденциальности. Отношения, связанные с обработкой персональных данных и "
                   "информации о пользователях Сайта")
    return jinja_env.TemplateResponse("other_pages/privacy_policy.html", {"request": request,
                                                                          "title": title,
                                                                          "keywords": keywords,
                                                                          "description": description})


@router.get("/osnovnye-momenty-procedury-bankrotstva", response_class=HTMLResponse, tags=["other pages"])
async def main_points_procedure(request: Request):
    """ Страница основных моментов процедуры банкротства фаз лица """
    title = "Основные моменты процедуры банкротства физических лиц"
    keywords = "гражданин, банкротство, суд, документы"
    description = "Что такое «банкротство гражданина? Банкротство физического лица"
    return jinja_env.TemplateResponse("other_pages/main_points.html", {"request": request,
                                                                       "title": title,
                                                                       "keywords": keywords,
                                                                       "description": description})


@router.get("/применение-закона-о-банкротстве", response_class=HTMLResponse, tags=["other pages"])
async def points_procedure(request: Request):
    """ Страница Как объявить себя банкротом"""
    title ='Банкротство физических лиц, юридические услуги по банкротству'
    return jinja_env.TemplateResponse("other_pages/points_procedure.html", {"request": request,
                                                                            "title": title})


@router.get("/цены-на-услуги-банкротства")
async def prices_procedure(request: Request):
    """ Страница с ценами """
    title = 'Цены на юридические услуги по банкротству'
    return jinja_env.TemplateResponse("other_pages/prices.html", {"request": request,
                                                                            "title": title})


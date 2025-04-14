from fastapi import APIRouter, Request, FastAPI
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

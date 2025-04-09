from typing import Optional
from admin_folder.admin_verification import get_current_admin
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Request, Form, HTTPException, Depends
from database.models_db import AddressModel, PhoneModel

templates = Jinja2Templates(directory="templates/admin_pages")
router = APIRouter()

@router.get("/admin/contacts", response_class=HTMLResponse, tags=["contacts"])
async def admin_contacts(request: Request,
                         username: str = Depends(get_current_admin)):
    """ Страница с контактами """
    addresses = await AddressModel.all()
    phones = await PhoneModel.all()
    return templates.TemplateResponse('admin_contacts.html', {"request": request,
                                                              "addresses": addresses,
                                                              "phones": phones})


@router.get("/admin/add_phone", response_class=HTMLResponse, tags=["contacts"])
async def admin_add_phone(request: Request,
                          username: str = Depends(get_current_admin)):
    """ Шаблон для добавления контактов """
    return templates.TemplateResponse('add_phone.html', {"request": request})


@router.get("/admin/add_contact", response_class=HTMLResponse, tags=["contacts"])
async def admin_add_contact(request: Request,
                            username: str = Depends(get_current_admin)):
    """ Шаблон для добавления контактов """
    return templates.TemplateResponse('add_contacts.html', {"request": request})


@router.post("/admin/save_add_contacts", response_class=HTMLResponse, tags=["contacts"])
async def admin_save_contacts(phone: str = Form(None),
                              city: str = Form(None),
                              street: str = Form(None),
                              house_number: str = Form(None),
                              office_number: str = Form(None),
                              metro_station: str = Form(None),
                              description: str = Form(None),
                              username: str = Depends(get_current_admin)):
    """ Сохранение контактов """
    if phone:
        await PhoneModel.create(phone=phone)
    else:
        await AddressModel.create(address=city, street=street,
                                  house_number=house_number,
                                  office_number=office_number,
                                  metro_station=metro_station,
                                  description=description)
    return RedirectResponse(url='/admin/contacts', status_code=303)


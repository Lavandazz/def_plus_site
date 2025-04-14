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
                              house_number: int = Form(None),
                              building: str = Form(None),
                              office_number: int = Form(None),
                              metro_station: str = Form(None),
                              description: str = Form(None),
                              username: str = Depends(get_current_admin)):
    """ Сохранение контактов """
    if phone:
        print(f'телефон {phone}')
        await PhoneModel.create(phone_number=phone)
    else:
        await AddressModel.create(city=city,
                                  street=street,
                                  house_number=house_number,
                                  building=building,
                                  office_number=office_number,
                                  metro_station=metro_station,
                                  description=description)

    return RedirectResponse(url='/admin/contacts', status_code=303)


@router.get("/admin/edit_phone/{phone_id}", response_class=HTMLResponse, tags=["contacts"])
async def admin_edit_phone(request: Request, phone_id: int, username: str = Depends(get_current_admin)):
    """ Редактирование телефона """
    phone = await PhoneModel.get(id=phone_id)
    print(f'phone : {phone}, phone_id: {phone_id}, phone.phone: {phone.phone_number}')
    if not phone:
        raise HTTPException(status_code=404, detail="Телефон не найден")
    return templates.TemplateResponse('edit_phone.html', {"request": request, "phone": phone})


@router.get("/admin/edit_contact/{contact_id}", response_class=HTMLResponse, tags=["contacts"])
async def admin_edit_contact(request: Request, contact_id: int, username: str = Depends(get_current_admin)):
    """ Редактирование адреса """
    address = await AddressModel.get(id=contact_id)
    if not address:
        raise HTTPException(status_code=404, detail="Адрес не найден")
    return templates.TemplateResponse('edit_contact.html', {"request": request, "address": address})


@router.post("/admin/save_edit_contacts/{contact_id}", tags=["contacts"])
async def admin_edit_contact(contact_id: int,
                             phone: str = Form(None),
                             city: str = Form(None),
                             street: str = Form(None),
                             house_number: int = Form(None),
                             building: str = Form(None),
                             office_number: int = Form(None),
                             metro_station: str = Form(None),
                             description: str = Form(None),
                             username: str = Depends(get_current_admin)):
    """ Сохранение отредактированных данных """
    if phone:
        phone_contact = await PhoneModel.get(id=contact_id)
        phone_contact.phone_number = phone
        await phone_contact.save()

    else:
        address = await AddressModel.get(id=contact_id)
        address.city = city
        address.street = street
        address.house_number = house_number
        address.building = building
        address.office_number = office_number
        address.metro_station = metro_station
        address.description = description
        await address.save()

    return RedirectResponse('/admin/contacts', status_code=303)


@router.post("admin/delete/{contact_id}", tags=["contacts"])
async def admin_delete(contact_id: int, username: str = Depends(get_current_admin)):
    """ Удаление записи телефона или адреса """
    try:
        address = await AddressModel.get(id=contact_id)
        print(f'контакт: {address}, {contact_id}')
        if address:
            await address.delete()
        else:
            phone_contact = await PhoneModel.get(id=contact_id)
            await phone_contact.delete()
        return RedirectResponse(url='/admin/contacts', status_code=303)
    except Exception as e:
        return {"error": f"Произошла ошибка удаления вопроса/адреса: {e}"}

from fastapi import Depends, HTTPException, Cookie
from typing import Optional, Any
from starlette.responses import RedirectResponse
from auth import verify_token

def get_current_admin(access_token: Optional[str] = Cookie(None)) -> str:
    """Проверка токена администратора"""
    if not access_token:
        print(f'перенаправляю')
        raise HTTPException(status_code=303, detail="Redirect", headers={"Location": "/admin/login"})

    try:
        return verify_token(access_token)
    except HTTPException:
        raise HTTPException(status_code=303, detail="Redirect", headers={"Location": "/admin/login"})


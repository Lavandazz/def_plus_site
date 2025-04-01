from datetime import timedelta, datetime, timezone
import jwt
import os
import bcrypt
from fastapi import HTTPException

secret_key = os.getenv("SECRET_KEY")
refresh_secret_key = os.getenv("REFRESH_SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    """ Хешируем пароль перед сохранением в БД """
    user_pass = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return user_pass.decode('utf-8')  # Преобразуем хеш в строку для хранения в бд


def verify_password(plain_password, hashed_password):
    """ Проверяем, совпадает ли введённый пароль с хешем в БД """
    print(f'Проверка хэша пароля {plain_password.encode()}, {hashed_password.encode()}')
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def create_all_token(data: dict, secret_key: str):
    """ Создание JWT-токена """
    data_to_encode = data.copy()
    live_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"exp": live_time})  # Добавляем в словарь время жизни токена
    encoded = jwt.encode(data_to_encode, secret_key, algorithm=algorithm)  # Кодируем токен
    return encoded


def create_tokens(username: str):
    """ Создание основного токена и рефреш """
    main_token = create_all_token({"username": username}, secret_key)
    refresh_token = create_all_token({"username": username}, refresh_secret_key)
    return {"main_token": main_token, "refresh_token": refresh_token}


def verify_token(token: str):
    """ Проверяем JWT-токен и извлекаем пользователя """
    try:
        decoded = jwt.decode(token, secret_key, algorithms=[algorithm])
        username = decoded.get('username')
        if username is None:
            raise HTTPException(status_code=401, detail='Неверный токен')
        return username  # Возвращаем имя пользователя

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Токен истёк")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Неверный токен")

# from database.models_db import AdminModel
# async def create_admin():
#     admin = await AdminModel.create(admin='admin', password=hash_password("aprilia89"))
#     print("Админ зарегистрирован!")
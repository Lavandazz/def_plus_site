import os
from dotenv import load_dotenv

# Загрузка .env
ENV_MODE = "production"  # Меняйте на "production" для основного .env
env_file = ".env.local" if ENV_MODE == "local" else ".env"
load_dotenv(env_file)

# Переменные окружения
admin_id = os.getenv("ADMIN_ID")

DATABASE_URL = (
    f"postgres://{os.getenv('DATABASE_USER')}:"
    f"{os.getenv('DATABASE_PASSWORD')}@"
    f"{os.getenv('DATABASE_HOST')}:"
    f"{int(os.getenv('DATABASE_PORT'))}/"
    f"{os.getenv('DATABASE_NAME')}"
)

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["database.models_db", "aerich.models"],  # aerich.models миграции
            "default_connection": "default",
        },
    },
}

from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "addressmodel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "city" VARCHAR(50) NOT NULL,
    "street" VARCHAR(100) NOT NULL,
    "house_number" VARCHAR(15) NOT NULL,
    "office_number" VARCHAR(5) NOT NULL,
    "metro_station" VARCHAR(30) NOT NULL,
    "description" VARCHAR(50) NOT NULL
);
        CREATE TABLE IF NOT EXISTS "phonemodel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "phone_number" VARCHAR(50) NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "addressmodel";
        DROP TABLE IF EXISTS "phonemodel";"""

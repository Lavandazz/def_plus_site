from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "questionandanswermodel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "question" VARCHAR(200) NOT NULL,
    "answer" TEXT NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "questionandanswermodel";"""

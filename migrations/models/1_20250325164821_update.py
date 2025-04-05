from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "workermodel" ADD "patronymic" VARCHAR(100) NOT NULL;
        ALTER TABLE "workermodel" ALTER COLUMN "surname" TYPE VARCHAR(100) USING "surname"::VARCHAR(100);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "workermodel" DROP COLUMN "patronymic";
        ALTER TABLE "workermodel" ALTER COLUMN "surname" TYPE VARCHAR(50) USING "surname"::VARCHAR(50);"""

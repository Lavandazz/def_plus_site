from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "addressmodel" ALTER COLUMN "building" DROP NOT NULL;
        ALTER TABLE "addressmodel" ALTER COLUMN "office_number" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "addressmodel" ALTER COLUMN "building" SET NOT NULL;
        ALTER TABLE "addressmodel" ALTER COLUMN "office_number" SET NOT NULL;"""

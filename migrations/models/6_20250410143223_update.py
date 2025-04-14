from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "addressmodel" ADD "building" VARCHAR(15) NOT NULL;
        ALTER TABLE "addressmodel" ALTER COLUMN "metro_station" TYPE VARCHAR(50) USING "metro_station"::VARCHAR(50);
        ALTER TABLE "addressmodel" ALTER COLUMN "house_number" TYPE VARCHAR(5) USING "house_number"::VARCHAR(5);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "addressmodel" DROP COLUMN "building";
        ALTER TABLE "addressmodel" ALTER COLUMN "metro_station" TYPE VARCHAR(30) USING "metro_station"::VARCHAR(30);
        ALTER TABLE "addressmodel" ALTER COLUMN "house_number" TYPE VARCHAR(15) USING "house_number"::VARCHAR(15);"""

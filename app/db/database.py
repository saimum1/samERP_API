# from dotenv import load_dotenv
# import os
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# load_dotenv() 
# SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
# if not SQLALCHEMY_DATABASE_URL:
#     raise ValueError("DATABASE_URL environment variable is not set")
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
if not MONGODB_URL:
    raise ValueError("MONGODB_URL environment variable is not set") 

client = AsyncIOMotorClient(MONGODB_URL)
db = client.get_default_database("samerpdb")

async def get_db():
    return db

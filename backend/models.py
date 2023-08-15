from pymongo import MongoClient
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

MONGO_SERVER = "mongodb://localhost:27017"
client = MongoClient(MONGO_SERVER)

database = client.get_database("Qwitter")
qweet = database.get_collection("qweet")
# qweet.update_many({}, {"$set": {"comments": []}}, upsert=False)
qweet_user = database.get_collection("user")


class Qweet(BaseModel):
    content: str
    created_at: datetime = None
    created_by: str = None
    updated_at: datetime = None


class UserBase(BaseModel):
    username: str
    email: str | None = None
    fullname: str | None = None


class UserCreate(UserBase):
    password: str


class TokenRefresh(BaseModel):
    access_token: str
    refresh_token: str

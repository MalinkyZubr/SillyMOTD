from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime


class MessageTemplate(BaseModel):
    message: str
    emotion: str
    time_date_sent: datetime

app = FastAPI()

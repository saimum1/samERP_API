from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

class ArticleRequest(BaseModel):
    topic: str
    format_instructions: str
    word_count: int = 600
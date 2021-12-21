from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from src.models.base import Model


class ArticleBase(BaseModel):
    main_title: str = Field(..., max_length=85)
    meta_title: str = Field(..., max_length=65)
    meta_description: str = Field(..., max_length=155)
    featured: bool = False
    slug: Optional[str] = None
    summary: str = Field(..., max_length=500)
    content: Optional[str] = None
    est_read_time: Optional[int] = None
    category: Optional[List[str]] = Field([])


class ArticleCreate(ArticleBase):
    main_title: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    featured: Optional[bool] = None
    slug: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    category: list = []


class ArticleUpdate(ArticleBase):
    main_title: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    featured: Optional[bool] = None
    slug: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    category: list = []
    updated_at: Optional[datetime] = datetime.utcnow()



class Article(ArticleBase):
    pass



class ArticleDB(ArticleBase, Model):
    published: bool = False




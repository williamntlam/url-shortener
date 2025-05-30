from pydantic import BaseModel, Field, Validator, ValidationError
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UrlRequestObject(BaseModel):
    url: str = Field(..., description="The URL to be shortened")

    @validator('url')
    def validate_url(cls, url):
        if not url.startswith('http'):
            raise ValueError("URL must start with http or https")
        return url
    
class UrlResponseObject(BaseModel):

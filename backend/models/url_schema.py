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
    url: str = Field(..., description="The URL to be shortened", max_length=2048)
    shortened_url: str = Field(..., description="The shortened URL", max_length=100)
    short_code: str = Field(..., description="The unique identifier for the shortened URL", max_length=10)
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When the URL was shortened")
    is_expired: bool = Field(default=False, description="Whether the shortened URL has expired")
    expiry_date: Optional[datetime] = Field(None, description="When the shortened URL will expire")
    is_one_time: bool = Field(default=False, description="Whether the URL can only be used once")
    is_active: bool = Field(default=True, description="Whether the shortened URL is currently active")

    @validator('shortened_url')
    def validate_shortened_url(cls, shortened_url):
        if not shortened_url.startswith('http'):
            raise ValueError("Shortened URL must start with http or https")
        return shortened_url

    @validator('url')
    def validate_url(cls, url):
        if not url.startswith('http'):
            raise ValueError("URL must start with http or https")
        return url
    
    @validator('created_at')
    def validate_created_at(cls, created_at):
        if created_at > datetime.utcnow():
            raise ValueError("Created date cannot be in the future")
        return created_at

    @validator('expiry_date')
    def validate_expiry_date(cls, expiry_date, values):
        if expiry_date and 'created_at' in values:
            if expiry_date <= values['created_at']:
                raise ValueError("Expiry date must be after creation date")
        return expiry_date

    @validator('short_code')
    def validate_short_code(cls, short_code):
        if not short_code.isalnum():
            raise ValueError("Short code must be alphanumeric")
        return short_code
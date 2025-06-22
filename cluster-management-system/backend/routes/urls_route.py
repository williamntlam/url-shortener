from fastapi import APIRouter, HTTPException
from models.url_schema import UrlRequestObject, UrlResponseObject
from services.url_service import get_original_url, get_analytics, delete_url, create_short_url as create_url

router = APIRouter()

@router.post("/shorten", response_model=UrlResponseObject)
async def create_short_url(url: UrlRequestObject):
    try:
        short_url = await create_url(url.original_url)
        if not short_url:
            raise HTTPException(status_code=400, detail="Failed to create short URL")
        return short_url
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{short_code}")
async def redirect_to_original(short_code: str):
    try:
        original_url = await get_original_url(short_code)
        if not original_url:
            raise HTTPException(status_code=404, detail="URL not found.")
        return {"redirection_url": original_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{short_code}/analytics")
async def get_url_analytics(short_code: str):
    try:
        analytics = await get_analytics(short_code)
        if not analytics:
            raise HTTPException(status_code=404, detail="URL not found.")
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{short_code}")
async def delete_short_url(short_code: str):
    try:
        deleted = await delete_url(short_code)
        if not deleted:
            raise HTTPException(status_code=404, detail="URL not found.")
        return {"message": f"Short URL `{short_code}` deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
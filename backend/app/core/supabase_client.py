from functools import lru_cache
from typing import Annotated

from supabase import create_client, Client
from fastapi import Depends, HTTPException, status

from app.core.config import settings


@lru_cache(maxsize=1)
def _create_supabase_client() -> Client:
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_KEY must be set in .env to use Supabase endpoints. "
            "Get these from: Supabase Dashboard > Project Settings > API"
        )
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


def get_supabase_client() -> Client:
    try:
        return _create_supabase_client()
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        )


SupabaseClientDep = Annotated[Client, Depends(get_supabase_client)]

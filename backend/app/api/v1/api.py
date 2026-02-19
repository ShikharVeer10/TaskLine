"""
API v1 Router — combines all v1 route files into a single router.
"""
from fastapi import APIRouter

from app.api.v1.routes import login, users, tasks, supabase_routes

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(tasks.router)
api_router.include_router(supabase_routes.router)

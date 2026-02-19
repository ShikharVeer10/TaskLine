import uuid

from fastapi import APIRouter, HTTPException, Query, status
from postgrest.exceptions import APIError

from app.core.supabase_client import SupabaseClientDep

router = APIRouter(prefix="/supabase", tags=["supabase"])


@router.get("/users")
def list_users_via_supabase(
    supabase: SupabaseClientDep,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
):
    """List users via the Supabase REST API. Excludes hashed_password."""
    try:
        response = (
            supabase.table("user")
            .select("id, email, full_name, is_active, is_superuser, created_at")
            .range(skip, skip + limit - 1)
            .execute()
        )
        count_response = (
            supabase.table("user")
            .select("id", count="exact")
            .execute()
        )
        return {"data": response.data, "count": count_response.count}
    except APIError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Supabase API error: {e.message}",
        )


@router.get("/users/{user_id}")
def get_user_via_supabase(user_id: uuid.UUID, supabase: SupabaseClientDep):
    """Get a single user by ID via the Supabase REST API."""
    try:
        response = (
            supabase.table("user")
            .select("id, email, full_name, is_active, is_superuser, created_at")
            .eq("id", str(user_id))
            .execute()
        )
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return response.data[0]
    except APIError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Supabase API error: {e.message}",
        )


@router.get("/tasks")
def list_tasks_via_supabase(
    supabase: SupabaseClientDep,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    owner_id: uuid.UUID | None = Query(default=None),
    task_status: str | None = Query(default=None, alias="status"),
):
    """List tasks via the Supabase REST API. Supports filtering by owner_id and status."""
    try:
        query = supabase.table("task").select(
            "id, title, description, status, priority, due_date, created_at, updated_at, owner_id"
        )
        if owner_id:
            query = query.eq("owner_id", str(owner_id))
        if task_status:
            query = query.eq("status", task_status)

        response = query.range(skip, skip + limit - 1).execute()

        count_query = supabase.table("task").select("id", count="exact")
        if owner_id:
            count_query = count_query.eq("owner_id", str(owner_id))
        if task_status:
            count_query = count_query.eq("status", task_status)
        count_response = count_query.execute()

        return {"data": response.data, "count": count_response.count}
    except APIError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Supabase API error: {e.message}",
        )


@router.get("/tasks/{task_id}")
def get_task_via_supabase(task_id: uuid.UUID, supabase: SupabaseClientDep):
    """Get a single task by ID via the Supabase REST API."""
    try:
        response = (
            supabase.table("task")
            .select("id, title, description, status, priority, due_date, created_at, updated_at, owner_id")
            .eq("id", str(task_id))
            .execute()
        )
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        return response.data[0]
    except APIError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Supabase API error: {e.message}",
        )

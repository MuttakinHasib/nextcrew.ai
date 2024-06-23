from fastapi import APIRouter


router = APIRouter(prefix="/crews", tags=["Crews"])


@router.get("")
async def get_crews():
    return []

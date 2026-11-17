from fastapi import APIRouter

from config.settings import settings
from presentation.api.dependencies import GetFillingsDep
from presentation.api.schemas import FillingRead

router = APIRouter(
    prefix=settings.api_prefix.fillings,
    tags=["Filling"],
)


@router.get("", response_model=list[FillingRead])
async def get_fillings(use_case: GetFillingsDep):
    return await use_case.execute()

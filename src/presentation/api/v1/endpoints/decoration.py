from fastapi import APIRouter

from config.settings import settings
from presentation.api.dependencies import GetDecorationDep
from presentation.api.schemas import DecorationRead

router = APIRouter(
    prefix=settings.api_prefix.decorations,
    tags=["Decoration"],
)


@router.get(
    "",
    response_model=list[DecorationRead],
)
async def get_all_decorations(use_case: GetDecorationDep):
    return await use_case.execute()

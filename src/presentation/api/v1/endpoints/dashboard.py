from fastapi import APIRouter

from presentation.api.dependencies import CurrentAdminIdDep, GetDashboardSummaryDep
from presentation.api.schemas.dashboard import DashboardSummaryRead

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardSummaryRead)
async def get_dashboard_summary(
    _: CurrentAdminIdDep,
    use_case: GetDashboardSummaryDep,
):
    return await use_case.execute()

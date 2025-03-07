from fastapi import APIRouter, Depends, status

from trainings_app.db.connection import get_repo
from trainings_app.reports.repositories import ReportRepository
from trainings_app.reports.schemas import GetReport, CreateReport

router = APIRouter(prefix='/reports', tags=['report'])


@router.post(
    path='/',
    response_model=GetReport,
    description="Add information for daily report",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
        data: CreateReport,
        repo: ReportRepository = Depends(get_repo(ReportRepository)),
):
    print("Перед вызовом create:", data.dict())
    try:
        return await repo.create(data.dict())
    except Exception as e:
        raise e

from typing import Annotated

from fastapi import APIRouter, Body, Depends

from app.api.schemas.report import ReportFromDB, ReportCreateRequest
from app.services.report_service import ReportService
from app.utils.unitofwork import IUnitOfWork, UnitOfWork

report_router = APIRouter(prefix="/report", tags=["Report"])


async def get_report_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> ReportService:
    return ReportService(uow)


@report_router.get("/reports/", response_model=list[ReportFromDB])
async def get_reports(
    report_service: ReportService = Depends(get_report_service),
    enterprise_id: int = None,
    desc: bool = False,
):
    return await report_service.get_reports(enterprise_id, desc)


@report_router.post("/reports/", response_model=ReportFromDB)
async def create_report(
    report_request_data: Annotated[ReportCreateRequest, Body()],
    report_service: ReportService = Depends(get_report_service),
) -> ReportFromDB:
    requset_dict = {
        "vehicle_id": report_request_data.vehicle_id,
        "period": report_request_data.period,
        "from_date": report_request_data.from_date,
        "till_date": report_request_data.to_date,
        "enterprise_id": report_request_data.enterprise_id,
    }
    return await report_service.create_report_by_vehicle(**requset_dict)


@report_router.get("/reports/{report_id}", response_model=ReportFromDB)
async def retrieve_report(
    report_id: int,
    report_service: ReportService = Depends(get_report_service),
) -> ReportFromDB:
    return await report_service.retrieve_report(report_id)

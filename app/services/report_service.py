from datetime import date, timedelta
from collections import defaultdict
from geopy import distance

from app.api.schemas.report import ReportFromDB, ReportCreate
from app.api.schemas.vehicle_track_point import from_geo_point_to_lat_long
from app.utils.unitofwork import IUnitOfWork
from app.utils.datetime_utils import get_period_from_datetime, get_str_key


class ReportService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_reports(self, enterprise_id: int = None, desc: bool = False) -> list[ReportFromDB]:
        async with self.uow:
            if enterprise_id:
                reports = await self.uow.report.find_all_filter_by_enterprise(
                    {"enterprise_id": [enterprise_id], "desc": desc}
                )
            else:
                reports = await self.uow.report.find_all()
            return [ReportFromDB.model_validate(report) for report in reports]

    async def retrieve_report(self, report_id: int) -> ReportFromDB:
        async with self.uow:
            report = await self.uow.report.find_one(report_id)
            return ReportFromDB.model_validate(report)

    async def create_report_by_vehicle(
        self,
        *,
        vehicle_id: int,
        period: str,
        from_date: date,
        till_date: date,
        enterprise_id: int,
    ) -> ReportFromDB:
        async with self.uow:
            trackpoints_date_dict = {
                "vehicle_id": vehicle_id,
                f"date_time_{vehicle_id}": (from_date, till_date + timedelta(days=1)),
            }
            track_points = await self.uow.vehicletrackpoint.find_all_between_datetimes(trackpoints_date_dict)

            geo_points_dict = defaultdict(list)
            serializer = from_geo_point_to_lat_long
            for tp_db in track_points:
                tp = serializer(tp_db)
                geo_points_dict[get_period_from_datetime(tp_db.date_time, period)].append([tp.long, tp.lat])

            result_value = {}
            for tp_date, points_list in geo_points_dict.items():
                if len(points_list) < 2:
                    result_value[tp_date] = 0
                    continue
                distance_list = []
                start_point = points_list[0]
                for point in points_list[1::]:
                    distance_list.append(distance.distance(start_point, point).km)
                result_value[tp_date] = round(sum(distance_list))

            dict_to_store = {}
            for key, value in sorted(result_value.items()):
                key_elems = []
                for elem in key:
                    key_elems.append(str(elem))
                dict_to_store[get_str_key(key_elems, period)] = value

            report_data = ReportCreate(
                title=f"{period} report for vehicle {vehicle_id} from {from_date} to {till_date}",
                period=period,
                from_date=from_date,
                to_date=till_date,
                report_result=dict_to_store,
                type="vehiclemileagereport",
                enterprise_id=enterprise_id,
            )
            report_dict: dict = report_data.model_dump()
            report_from_db = await self.uow.report.add_one(report_dict)
            report_to_return = ReportFromDB.model_validate(report_from_db)

            await self.uow.commit()
            return report_to_return

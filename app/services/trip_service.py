from datetime import datetime

from fastapi.exceptions import ValidationException

from app.api.schemas.trip import (
    TripCreate,
    TripFromDB,
    TripFromDBWithExtraData,
    get_address_by_point,
)
from app.api.schemas.user import UserExtended
from app.api.schemas.vehicle import VehicleFromDB
from app.api.schemas.vehicle_track_point import (
    VehicleTrackPoint,
    VehicleTrackPointGeoJSON,
    from_geo_point_to_geojson,
    from_geo_point_to_lat_long,
)
from app.utils.auth import get_users_enterpises
from app.utils.unitofwork import IUnitOfWork


class TripService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_trip(self, trip_data: TripCreate, current_user: UserExtended = None) -> TripFromDB:
        if not current_user:
            return None

        allowed_objects = get_users_enterpises(current_user)

        async with self.uow:
            vehicle_from_db = await self.uow.vehicle.find_one(trip_data.vehicle_id)
            vehicle_repr = VehicleFromDB.model_validate(vehicle_from_db)

        if current_user.role not in ["admin", "manager"] or (
            current_user.role == "manager" and vehicle_repr.enterprise_id not in allowed_objects["enterprise_id"]
        ):
            raise ValidationException(
                {
                    "vehicle_id": (
                        "You are not allowed to create a trip for this vehicle. "
                        "The vehicle does not belong to your enterprise"
                    )
                }
            )

        trip_dict: dict = trip_data.model_dump()
        async with self.uow:
            trip_from_db = await self.uow.trip.add_one(trip_dict)
            trip_to_return = TripFromDB.model_validate(trip_from_db)

            await self.uow.commit()
            return trip_to_return

    async def get_trips(
        self,
        current_user: UserExtended = None,
        geojson: bool = False,
        vehicle_id: int = None,
        from_date=None,
        till_date=None,
    ) -> list[TripFromDB]:
        async with self.uow:
            trips: list = await self.uow.trip.find_all()
            return [TripFromDB.model_validate(trip) for trip in trips]

    async def retrieve_trip(
        self,
        trip_id: int,
        current_user: UserExtended = None,
        geojson: bool = False,
        from_date: str = None,
        till_date: str = None,
    ) -> TripFromDB:
        async with self.uow:
            trip = await self.uow.trip.find_one(trip_id)
            return TripFromDB.model_validate(trip)

    async def get_trips_points_by_vehicle(
        self,
        current_user: UserExtended,
        vehicle_id: int,
        from_date: datetime,
        till_date: datetime,
        geojson: bool = False,
    ) -> list[VehicleTrackPoint | VehicleTrackPointGeoJSON]:
        if not current_user:
            return None

        allowed_objects = get_users_enterpises(current_user)
        filter_set = {
            "vehicle_id": vehicle_id,
            "from_date": from_date,
            "till_date": till_date,
        }
        async with self.uow:
            if current_user.role == "manager" and allowed_objects.get("enterprise_id"):
                trips: list = await self.uow.trip.find_all_with_filters(
                    allowed_objects=allowed_objects, filter_set=filter_set
                )
            elif current_user.role == "admin":
                trips: list = await self.uow.trip.find_all_with_filters(filter_set=filter_set)
            else:
                raise ValidationException({"enterprise_id": "You are not allowed to get objects for this enterprise"})
            trips_date_time_dict = {"vehicle_id": vehicle_id}
            for trip in trips:
                trips_date_time_dict[f"date_time_{trip.id}"] = (trip.start_date_time, trip.finish_date_time)

            track_points = await self.uow.vehicletrackpoint.find_all_between_datetimes(trips_date_time_dict)

            list_to_return = []
            serializer = from_geo_point_to_lat_long if not geojson else from_geo_point_to_geojson
            for tp_db in track_points:
                tp = serializer(tp_db)
                list_to_return.append(tp)
            return list_to_return

    async def get_trips_by_vehicle(
        self,
        current_user: UserExtended,
        vehicle_id: int,
        from_date: datetime,
        till_date: datetime,
        geojson: bool = False,
    ) -> list[TripFromDBWithExtraData]:
        if not current_user:
            return None

        allowed_objects = get_users_enterpises(current_user)
        filter_set = {
            "vehicle_id": vehicle_id,
            "from_date": from_date,
            "till_date": till_date,
        }
        async with self.uow:
            if current_user.role == "manager" and allowed_objects.get("enterprise_id"):
                trips: list = await self.uow.trip.find_all_with_filters(
                    allowed_objects=allowed_objects, filter_set=filter_set
                )
            elif current_user.role == "admin":
                trips: list = await self.uow.trip.find_all_with_filters(filter_set=filter_set)
            else:
                raise ValidationException({"enterprise_id": "You are not allowed to get objects for this enterprise"})
            trips_start_finish_dict = {}
            for trip in trips:
                trip_points = await self.uow.vehicletrackpoint.find_all_between_datetimes(
                    {f"date_time_{trip.id}": (trip.start_date_time, trip.finish_date_time)}
                )
                trips_start_finish_dict[trip.id] = (trip_points[0], trip_points[-1]) if trip_points else ()

            list_to_return = []
            for trip_db in trips:

                start_point_ser = from_geo_point_to_lat_long(trips_start_finish_dict[trip_db.id][0])
                start_point_coords = (start_point_ser.lat, start_point_ser.long)
                finish_point_ser = from_geo_point_to_lat_long(trips_start_finish_dict[trip_db.id][1])
                finish_point_coords = (finish_point_ser.lat, finish_point_ser.long)

                trip_to_represent = TripFromDBWithExtraData(
                    id=trip_db.id,
                    start_date_time=trip_db.start_date_time,
                    finish_date_time=trip_db.finish_date_time,
                    start_point_geo=start_point_coords,
                    finish_point_geo=finish_point_coords,
                    start_address=get_address_by_point(start_point_coords),
                    finish_address=get_address_by_point(finish_point_coords),
                )
                list_to_return.append(trip_to_represent)
            return list_to_return

import math
from datetime import datetime

from fastapi.exceptions import ValidationException
from pytz import timezone

from app.api.schemas.user import UserExtended
from app.api.schemas.vehicle import VehicleCreate, VehicleFromDB, VehiclePartialUpdate
from app.api.schemas.vehicle_brand import (
    VehicleBrandCreate,
    VehicleBrandFromDB,
    VehicleBrandPartialUpdate,
)
from app.api.schemas.vehicle_model import (
    VehicleBrandModel,
    VehicleModelCreate,
    VehicleModelFromDB,
    VehicleModelPartialUpdate,
)
from app.api.schemas.vehicle_track_point import (
    VehicleCreateTrackPoint,
    VehicleCreateTrackPointGeo,
    VehicleTrackPoint,
    VehicleTrackPointGeoFromDB,
    VehicleTrackPointGeoJSON,
    from_geo_point_to_geojson,
    from_geo_point_to_lat_long,
)
from app.utils.auth import get_users_enterpises
from app.utils.pagination import PagedResponseSchema, PageParams
from app.utils.unitofwork import IUnitOfWork


class VehicleBrandService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_vehicle_brand(self, vehicle_brand_data: VehicleBrandCreate) -> VehicleBrandFromDB:
        vehicle_brand_dict: dict = vehicle_brand_data.model_dump()
        async with self.uow:
            vehicle_brand_from_db = await self.uow.vehiclebrand.add_one(vehicle_brand_dict)
            vehicle_brand_to_return = VehicleBrandFromDB.model_validate(vehicle_brand_from_db)

            # если ранее возникнет ошибка при создании объектов, то изменения не сохранятся и откатятся
            await self.uow.commit()
            return vehicle_brand_to_return

    async def get_vehicle_brands(self) -> list[VehicleBrandFromDB]:
        async with self.uow:
            vehicle_brands: list = await self.uow.vehiclebrand.find_all()
            return [VehicleBrandFromDB.model_validate(vehicle_brand) for vehicle_brand in vehicle_brands]

    async def retrieve_vehicle_brands(self, vehicle_brand_id: int) -> VehicleBrandFromDB:
        async with self.uow:
            vehicle_brand = await self.uow.vehiclebrand.find_one(vehicle_brand_id)
            return VehicleBrandFromDB.model_validate(vehicle_brand)

    async def update_vehicle_brand(self, vehicle_brand_id: int, vehicle_brand_data: VehicleBrandCreate):
        vehicle_brand_dict: dict = vehicle_brand_data.model_dump()
        async with self.uow:
            vehicle_brand_from_db = await self.uow.vehiclebrand.update_one(vehicle_brand_id, vehicle_brand_dict)
            vehicle_brand_to_return = VehicleBrandFromDB.model_validate(vehicle_brand_from_db)

            await self.uow.commit()
            return vehicle_brand_to_return

    async def partial_update_vehicle_brand(self, vehicle_brand_id: int, vehicle_brand_data: VehicleBrandPartialUpdate):
        vehicle_brand_dict: dict = vehicle_brand_data.model_dump(exclude_unset=True)
        async with self.uow:
            vehicle_brand_from_db = await self.uow.vehiclebrand.update_one(vehicle_brand_id, vehicle_brand_dict)
            vehicle_brand_to_return = VehicleBrandFromDB.model_validate(vehicle_brand_from_db)

            await self.uow.commit()
            return vehicle_brand_to_return

    async def delete_vehicle_brand(self, vehicle_brand_id: int):
        async with self.uow:
            vehicle_brand_from_db = await self.uow.vehiclebrand.delete_one(vehicle_brand_id)
            vehicle_brand_to_return = VehicleBrandFromDB.model_validate(vehicle_brand_from_db)

            await self.uow.commit()
            return vehicle_brand_to_return


class VehicleModelService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_vehicle_model(self, vehicle_model_data: VehicleModelCreate) -> VehicleModelFromDB:
        vehicle_model_dict: dict = vehicle_model_data.model_dump()
        async with self.uow:
            vehicle_model_from_db = await self.uow.vehiclemodel.add_one(vehicle_model_dict)
            vehicle_model_to_return = VehicleModelFromDB.model_validate(vehicle_model_from_db)

            # если ранее возникнет ошибка при создании объектов, то изменения не сохранятся и откатятся
            await self.uow.commit()
            return vehicle_model_to_return

    async def get_vehicle_models(self) -> list[VehicleModelFromDB]:
        async with self.uow:
            vehicle_models: list = await self.uow.vehiclemodel.find_all_brandmodels()
            return [VehicleModelFromDB.model_validate(vehicle_model) for vehicle_model in vehicle_models]

    async def get_vehicle_brandmodels(self) -> list[VehicleBrandModel]:
        async with self.uow:
            vehicle_brandmodels: list = await self.uow.vehiclemodel.find_all_brandmodels()
            brandmodels_list = []
            for vehicle_brandmodel in vehicle_brandmodels:
                brandmodel = VehicleBrandModel(
                    id=vehicle_brandmodel.id,
                    exact_model_name=vehicle_brandmodel.exact_model_name,
                    brand_name=vehicle_brandmodel.brand.brand_name,
                )
                brandmodels_list.append(brandmodel)
            return brandmodels_list

    async def retrieve_vehicle_models(self, vehicle_model_id: int) -> VehicleModelFromDB:
        async with self.uow:
            vehicle_model = await self.uow.vehiclemodel.find_one(vehicle_model_id)
            return VehicleModelFromDB.model_validate(vehicle_model)

    async def update_vehicle_model(self, vehicle_model_id: int, vehicle_model_data: VehicleModelCreate):
        vehicle_model_dict: dict = vehicle_model_data.model_dump()
        async with self.uow:
            vehicle_model_from_db = await self.uow.vehiclemodel.update_one(vehicle_model_id, vehicle_model_dict)
            vehicle_model_to_return = VehicleModelFromDB.model_validate(vehicle_model_from_db)

            await self.uow.commit()
            return vehicle_model_to_return

    async def partial_update_vehicle_model(self, vehicle_model_id: int, vehicle_model_data: VehicleModelPartialUpdate):
        vehicle_model_dict: dict = vehicle_model_data.model_dump(exclude_unset=True)
        async with self.uow:
            vehicle_model_from_db = await self.uow.vehiclemodel.update_one(vehicle_model_id, vehicle_model_dict)
            vehicle_model_to_return = VehicleModelFromDB.model_validate(vehicle_model_from_db)

            await self.uow.commit()
            return vehicle_model_to_return

    async def delete_vehicle_model(self, vehicle_model_id: int):
        async with self.uow:
            vehicle_model_from_db = await self.uow.vehiclemodel.delete_one(vehicle_model_id)
            vehicle_model_to_return = VehicleModelFromDB.model_validate(vehicle_model_from_db)

            await self.uow.commit()
            return vehicle_model_to_return


class VehicleService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_vehicle(
        self,
        vehicle_data: VehicleCreate,
        current_user: UserExtended = None,
    ) -> VehicleFromDB:
        if not current_user:
            return None

        allowed_objects = get_users_enterpises(current_user)
        vehicle_dict: dict = vehicle_data.model_dump_with_tz_align()
        if current_user.role not in ["admin", "manager"] or (
            current_user.role == "manager"
            and vehicle_dict["enterprise_id"]
            and vehicle_dict["enterprise_id"] not in allowed_objects["enterprise_id"]
        ):
            raise ValidationException({"enterprise_id": "You are not allowed to create a vehicle for this enterprise"})

        async with self.uow:
            vehicle_created = await self.uow.vehicle.add_one(vehicle_dict)
            # если ранее возникнет ошибка при создании объектов, то изменения не сохранятся и откатятся
            await self.uow.commit()

            vehicle_from_db = await self.uow.vehicle.find_one(vehicle_created)
            vehicle_to_return = VehicleFromDB.model_validate(vehicle_from_db)

            return vehicle_to_return

    async def get_vehicles(
        self, current_user: UserExtended = None, page_params: PageParams = None, enterprise_id: int = None
    ) -> PagedResponseSchema[VehicleFromDB]:
        if not current_user:
            return None

        allowed_objects = get_users_enterpises(current_user)
        async with self.uow:
            if enterprise_id is not None and (
                (current_user.role == "manager" and enterprise_id in allowed_objects.get("enterprise_id"))
                or current_user.role == "admin"
            ):
                allowed_objects["enterprise_id"] = [enterprise_id]
            elif current_user.role == "admin":
                allowed_objects = None
            elif current_user.role == "manager" and allowed_objects.get("enterprise_id") is None:
                raise ValidationException({"enterprise_id": "You are not allowed to get vehicles for this enterprise"})
            vehicles: list = await self.uow.vehicle.find_all_with_brandmodel_filter_by_enterprise(allowed_objects)
            from_index = page_params.page * page_params.size
            to_index = (page_params.page + 1) * page_params.size
            return PagedResponseSchema(
                total=math.ceil(len(vehicles) / page_params.size) - 1,
                page=page_params.page,
                size=page_params.size,
                results=[
                    VehicleFromDB.model_validate_datetime_with_tz(vehicle, vehicle.enterprise.company_timezone.value)
                    for vehicle in vehicles[from_index:to_index]
                ],
            )

    async def retrieve_vehicles(self, vehicle_id: int, current_user: UserExtended = None) -> VehicleFromDB:
        if not current_user:
            return None

        allowed_objects = get_users_enterpises(current_user)
        async with self.uow:
            vehicle = await self.uow.vehicle.find_one(vehicle_id)
            if current_user.role not in ["admin", "manager"] or (
                current_user.role == "manager"
                and vehicle.enterprise_id
                and vehicle.enterprise_id not in allowed_objects["enterprise_id"]
            ):
                raise ValidationException(
                    {"enterprise_id": "You are not allowed to update a vehicle for this enterprise"}
                )
            return VehicleFromDB.model_validate_datetime_with_tz(vehicle, vehicle.enterprise.company_timezone.value)

    async def update_vehicle(
        self,
        vehicle_id: int,
        vehicle_data: VehicleCreate,
        current_user: UserExtended = None,
    ):
        if not current_user:
            return None

        allowed_objects = get_users_enterpises(current_user)
        vehicle_dict: dict = vehicle_data.model_dump_with_tz_align()
        if current_user.role not in ["admin", "manager"] or (
            current_user.role == "manager"
            and vehicle_dict["enterprise_id"]
            and vehicle_dict["enterprise_id"] not in allowed_objects["enterprise_id"]
        ):
            raise ValidationException({"enterprise_id": "You are not allowed to update a vehicle for this enterprise"})

        async with self.uow:
            vehicle_from_db = await self.uow.vehicle.update_one(vehicle_id, vehicle_dict)
            vehicle_to_return = VehicleFromDB.model_validate(vehicle_from_db)

            await self.uow.commit()
            return vehicle_to_return

    async def partial_update_vehicle(
        self,
        vehicle_id: int,
        vehicle_data: VehiclePartialUpdate,
        current_user: UserExtended = None,
    ):
        if not current_user:
            return None

        allowed_objects = get_users_enterpises(current_user)
        async with self.uow:
            vehicle = await self.uow.vehicle.find_one(vehicle_id)

            if current_user.role not in ["admin", "manager"] or (
                current_user.role == "manager"
                and vehicle.enterprise_id
                and vehicle.enterprise_id not in allowed_objects["enterprise_id"]
            ):
                raise ValidationException(
                    {"enterprise_id": "You are not allowed to update a vehicle for this enterprise"}
                )
            company_tz = vehicle.enterprise.company_timezone.value

        vehicle_dict: dict = vehicle_data.model_dump_with_tz_align(tz=company_tz, exclude_unset=True)
        async with self.uow:
            vehicle_from_db = await self.uow.vehicle.update_one(vehicle_id, vehicle_dict)
            vehicle_to_return = VehicleFromDB.model_validate(vehicle_from_db)

            await self.uow.commit()
            return vehicle_to_return

    async def delete_vehicle(
        self,
        vehicle_id: int,
        current_user: UserExtended = None,
    ):
        if not current_user:
            return None

        allowed_objects = get_users_enterpises(current_user)
        async with self.uow:
            vehicle = await self.uow.vehicle.find_one(vehicle_id)

            if current_user.role not in ["admin", "manager"] or (
                current_user.role == "manager"
                and vehicle.enterprise_id
                and vehicle.enterprise_id not in allowed_objects["enterprise_id"]
            ):
                raise ValidationException(
                    {"enterprise_id": "You are not allowed to delete a vehicle for this enterprise"}
                )

        async with self.uow:
            vehicle_from_db = await self.uow.vehicle.delete_one(vehicle_id)
            vehicle_to_return = VehicleFromDB.model_validate(vehicle_from_db)

            await self.uow.commit()
            return vehicle_to_return


class VehicleTrackPointService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_vehicle_track_point(
        self,
        vehicle_track_point_data: VehicleCreateTrackPoint,
        current_user: UserExtended = None,
    ) -> VehicleTrackPointGeoFromDB:
        if not current_user:
            return None

        allowed_objects = get_users_enterpises(current_user)

        async with self.uow:
            vehicle_from_db = await self.uow.vehicle.find_one(vehicle_track_point_data.vehicle_id)
            vehicle_repr = VehicleFromDB.model_validate(vehicle_from_db)

        if current_user.role not in ["admin", "manager"] or (
            current_user.role == "manager" and vehicle_repr.enterprise_id not in allowed_objects["enterprise_id"]
        ):
            raise ValidationException(
                {
                    "vehicle_id": (
                        "You are not allowed to create a track point for this vehicle. "
                        "The vehicle does not belong to your enterprise"
                    )
                }
            )

        vehicle_track_point_geo_data = VehicleCreateTrackPointGeo(
            date_time=vehicle_track_point_data.date_time,
            geotag=f"POINT({vehicle_track_point_data.long} {vehicle_track_point_data.lat})",
            vehicle_id=vehicle_track_point_data.vehicle_id,
        )

        vehicle_tp_dict: dict = vehicle_track_point_geo_data.model_dump()  # add Mixin to align timezone

        async with self.uow:
            vehicle_track_point_created = await self.uow.vehicletrackpoint.add_one(vehicle_tp_dict)
            track_point_to_return = VehicleTrackPointGeoFromDB.model_validate(vehicle_track_point_created)
            await self.uow.commit()

            return track_point_to_return

    async def get_vehicle_track_points(
        self,
        current_user: UserExtended = None,
        geojson: bool = False,
        vehicle_id: int = None,
        from_date: str = None,
        till_date: str = None,
    ) -> list[VehicleTrackPoint | VehicleTrackPointGeoJSON]:
        from main import SERVER_TIME_ZONE

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
                track_points: list = await self.uow.vehicletrackpoint.find_all_with_filters(
                    allowed_objects=allowed_objects, filter_set=filter_set
                )
            elif current_user.role == "admin":
                track_points: list = await self.uow.vehicletrackpoint.find_all_with_filters(filter_set=filter_set)
            else:
                raise ValidationException({"enterprise_id": "You are not allowed to get objects for this enterprise"})

            if from_date and till_date:
                from_date_loc = datetime.strptime(from_date, "%Y-%m-%d %H:%M:%S")
                till_date_loc = datetime.strptime(till_date, "%Y-%m-%d %H:%M:%S")
            list_to_return = []
            serializer = from_geo_point_to_lat_long if not geojson else from_geo_point_to_geojson
            for tp_db in track_points:
                enterprize_tz = tp_db.vehicle.enterprise.company_timezone.value
                if from_date and till_date:
                    from_date_utc = (
                        timezone(enterprize_tz).localize(from_date_loc).astimezone(tz=timezone(SERVER_TIME_ZONE))
                    )
                    till_date_utc = (
                        timezone(enterprize_tz).localize(till_date_loc).astimezone(tz=timezone(SERVER_TIME_ZONE))
                    )
                if (
                    from_date
                    and till_date
                    and from_date_utc <= tp_db.date_time <= till_date_utc
                    or not (from_date and till_date)
                ):
                    tp = serializer(tp_db, tz=enterprize_tz)
                    list_to_return.append(tp)
            return list_to_return

    async def retrieve_vehicle_track_point(
        self,
        track_point_id: int,
        current_user: UserExtended = None,
        geojson: bool = False,
    ) -> VehicleTrackPoint | VehicleTrackPointGeoJSON:
        if not current_user:
            return None

        allowed_objects = get_users_enterpises(current_user)
        async with self.uow:
            if current_user.role == "manager" and allowed_objects.get("enterprise_id"):
                track_point = await self.uow.vehicletrackpoint.find_one_by_eneterprise(track_point_id, allowed_objects)
            elif current_user.role == "admin":
                track_point = await self.uow.vehicletrackpoint.find_one(track_point_id)
            else:
                raise ValidationException({"enterprise_id": "You are not allowed to get objects for this enterprise"})

            serializer = from_geo_point_to_lat_long if not geojson else from_geo_point_to_geojson
            return serializer(track_point, tz=track_point.vehicle.enterprise.company_timezone.value)

import math

from fastapi.exceptions import ValidationException

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
        vehicle_dict: dict = vehicle_data.model_dump()
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
        self, current_user: UserExtended = None, page_params: PageParams = None
    ) -> PagedResponseSchema[VehicleFromDB]:
        if not current_user:
            return None

        allowed_objects = get_users_enterpises(current_user)
        async with self.uow:
            if current_user.role == "manager" and allowed_objects.get("enterprise_id"):
                vehicles: list = await self.uow.vehicle.find_all_with_brandmodel_filter_by_enterprise(allowed_objects)
            elif current_user.role == "admin":
                vehicles: list = await self.uow.vehicle.find_all_with_brandmodel()
            else:
                raise ValidationException({"enterprise_id": "You are not allowed to get vehicles for this enterprise"})
            from_index = page_params.page * page_params.size
            to_index = (page_params.page + 1) * page_params.size
            return PagedResponseSchema(
                total=math.ceil(len(vehicles) / page_params.size) - 1,
                page=page_params.page,
                size=page_params.size,
                results=[VehicleFromDB.model_validate(vehicle) for vehicle in vehicles[from_index:to_index]],
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
            return VehicleFromDB.model_validate(vehicle)

    async def update_vehicle(
        self,
        vehicle_id: int,
        vehicle_data: VehicleCreate,
        current_user: UserExtended = None,
    ):
        if not current_user:
            return None

        allowed_objects = get_users_enterpises(current_user)
        vehicle_dict: dict = vehicle_data.model_dump()
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

        vehicle_dict: dict = vehicle_data.model_dump(exclude_unset=True)
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

from fastapi.exceptions import ValidationException

from app.api.schemas.enterprise import (
    EnterpriseCreate,
    EnterpriseFromDB,
    EnterprisePartialUpdate,
)
from app.api.schemas.user import UserExtended
from app.utils.auth import get_users_enterpises
from app.utils.unitofwork import IUnitOfWork


class EnterpriseService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_enterprises(
        self,
        current_user: UserExtended = None,
    ) -> list[EnterpriseFromDB]:
        if not current_user:
            return None

        allowed_objects = get_users_enterpises(current_user)
        async with self.uow:
            if current_user.role == "manager" and allowed_objects.get("enterprise_id"):
                enterprises: list = await self.uow.enterprise.find_all_filter_by_enterprise(allowed_objects)
            elif current_user.role == "admin":
                enterprises: list = await self.uow.enterprise.find_all()
            else:
                raise ValidationException({"enterprise_id": "You are not allowed to get enterprises."})
            return [EnterpriseFromDB.model_validate(enterprise) for enterprise in enterprises]

    async def add_enterprise(
        self,
        enterprise_data: EnterpriseCreate,
        current_user: UserExtended = None,
    ) -> EnterpriseFromDB:
        if not current_user:
            return None
        if current_user.role not in ["admin", "manager"]:
            raise ValidationException({"enterprise_id": "You are not allowed to create a enterprise"})

        enterprise_dict: dict = enterprise_data.model_dump()
        users_ids = enterprise_dict.pop("users", [])
        users_ids.append(current_user.id)
        async with self.uow:
            enterprise_from_db = await self.uow.enterprise.add_one(enterprise_dict)
            enterprise_users = await self.uow.user.find_all_filter_by_id(users_ids)
            enterprise_from_db.users = enterprise_users
            enterprise_to_return = EnterpriseFromDB.model_validate(enterprise_from_db)

            await self.uow.commit()

            return enterprise_to_return

    async def retrieve_enterprises(self, enterprise_id: int, current_user: UserExtended = None) -> EnterpriseFromDB:
        if not current_user:
            return None

        allowed_objects = get_users_enterpises(current_user)
        async with self.uow:
            enterprise = await self.uow.enterprise.find_one(enterprise_id)
            if current_user.role not in ["admin", "manager"] or (
                current_user.role == "manager" and enterprise and enterprise.id not in allowed_objects["enterprise_id"]
            ):
                raise ValidationException({"enterprise_id": "You are not allowed to retrieve a enterprise."})
            return EnterpriseFromDB.model_validate(enterprise)

    async def update_enterprise(
        self,
        enterprise_id: int,
        enterprise_data: EnterpriseCreate,
        current_user: UserExtended = None,
    ):
        if not current_user:
            return None

        allowed_objects = get_users_enterpises(current_user)
        if current_user.role not in ["admin", "manager"] or (
            current_user.role == "manager" and enterprise_id not in allowed_objects["enterprise_id"]
        ):
            raise ValidationException(
                {"enterprise_id": "You are not allowed to update a enterprise for this enterprise"}
            )

        enterprise_dict: dict = enterprise_data.model_dump()
        users_ids = enterprise_dict.pop("users", [])
        async with self.uow:
            enterprise_from_db = await self.uow.enterprise.update_one(enterprise_id, enterprise_dict)
            enterprise_users = await self.uow.user.find_all_filter_by_id(users_ids)
            enterprise_from_db.users = enterprise_users
            enterprise_to_return = EnterpriseFromDB.model_validate(enterprise_from_db)

            await self.uow.commit()
            return enterprise_to_return

    async def partial_update_enterprise(
        self,
        enterprise_id: int,
        enterprise_data: EnterprisePartialUpdate,
        current_user: UserExtended = None,
    ):
        if not current_user:
            return None

        allowed_objects = get_users_enterpises(current_user)
        if current_user.role not in ["admin", "manager"] or (
            current_user.role == "manager" and enterprise_id not in allowed_objects["enterprise_id"]
        ):
            raise ValidationException(
                {"enterprise_id": "You are not allowed to update a enterprise for this enterprise"}
            )

        enterprise_dict: dict = enterprise_data.model_dump(exclude_unset=True)
        users_ids = enterprise_dict.pop("users", [])
        async with self.uow:
            if enterprise_dict:
                enterprise_from_db = await self.uow.enterprise.update_one(enterprise_id, enterprise_dict)
            else:
                enterprise_from_db = await self.uow.enterprise.find_one(enterprise_id)
            if users_ids:
                enterprise_users = await self.uow.user.find_all_filter_by_id(users_ids)
                enterprise_from_db.users = enterprise_users
            enterprise_to_return = EnterpriseFromDB.model_validate(enterprise_from_db)

            await self.uow.commit()
            return enterprise_to_return

    async def delete_enterprise(
        self,
        enterprise_id: int,
        current_user: UserExtended = None,
    ):
        if not current_user:
            return None

        allowed_objects = get_users_enterpises(current_user)
        if current_user.role not in ["admin", "manager"] or (
            current_user.role == "manager" and enterprise_id not in allowed_objects["enterprise_id"]
        ):
            raise ValidationException(
                {"enterprise_id": "You are not allowed to delete this enterprise or enterprise does not exist."}
            )

        async with self.uow:
            enterprise_from_db = await self.uow.enterprise.delete_one(enterprise_id)
            enterprise_to_return = EnterpriseFromDB.model_validate(enterprise_from_db)

            await self.uow.commit()
            return enterprise_to_return

from sqlalchemy import Column, ForeignKey, Table

from app.db.database import Base

manager_enterprise_association_table = Table(
    "manger_enterprise_association_table",
    Base.metadata,
    Column("manager_id", ForeignKey("public.manager.id"), primary_key=True),
    Column("enterprise_id", ForeignKey("public.enterprise.id"), primary_key=True),
    schema="public",
)

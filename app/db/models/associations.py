from sqlalchemy import Column, ForeignKey, Table

from app.db.database import Base

user_enterprise_association_table = Table(
    "user_enterprise_association_table",
    Base.metadata,
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE"), primary_key=True),
    Column("enterprise_id", ForeignKey("enterprise.id", ondelete="CASCADE"), primary_key=True),
)

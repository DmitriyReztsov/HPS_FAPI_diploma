from sqlalchemy import BigInteger, String, TypeDecorator
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.db.models.associations import user_enterprise_association_table
from app.utils.auth import get_password_hash


class HashedPassword(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if isinstance(value, str):
            return get_password_hash(value)
        return None

    def process_result_value(self, value, dialect):
        return value


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(HashedPassword, nullable=False)
    disabled: Mapped[bool] = mapped_column(default=False)
    role: Mapped[str] = mapped_column(default="manager", nullable=True)

    enterprises: Mapped[list["Enterprise"]] = relationship(  # noqa F821 # type: ignore
        "Enterprise", secondary=user_enterprise_association_table, back_populates="users", lazy="immediate"
    )

    def __str__(self):
        return self.get_full_name

    @hybrid_property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

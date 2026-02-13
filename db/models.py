import datetime

from sqlalchemy import BigInteger, String, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .engine import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int] = mapped_column(Integer)
    where: Mapped[str] = mapped_column(String(50))
    comment: Mapped[str | None] = mapped_column(String, nullable=True)



from datetime import time

from sqlalchemy import Index, Integer, SmallInteger, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TimezoneDict(Base):
    __tablename__ = "timezone_dict"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    timezone_name: Mapped[str | None] = mapped_column(String(255))
    timezone: Mapped[time | None] = mapped_column(Time(timezone=True))


class PropertyCodeDict(Base):
    __tablename__ = "property_code_dict"

    __table_args__ = (
        Index("idx_property_code_dict_code", "code"),
        Index("idx_property_code_dict_group_code_code", "group_code", "code"),
    )

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    group_code: Mapped[str] = mapped_column(String(30), nullable=False)
    code: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[str | None] = mapped_column(String(100))


class RolesDict(Base):
    __tablename__ = "roles_dict"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[str] = mapped_column(String(60), nullable=False)


class FunctionsDict(Base):
    __tablename__ = "functions_dict"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(30), nullable=False)
    version: Mapped[int] = mapped_column(SmallInteger, nullable=False)


class SettingsDict(Base):
    __tablename__ = "settings_dict"

    __table_args__ = (Index("idx_settings_dict_code", "code"),)

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)


class StatusDict(Base):
    __tablename__ = "status_dict"

    __table_args__ = (Index("idx_status_dict_code", "code"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(16), nullable=False)
    name: Mapped[str] = mapped_column(String(60), nullable=False)


class ShablonDict(Base):
    __tablename__ = "shablon_dict"

    __table_args__ = (Index("idx_shablon_dict_code", "code"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[str | None] = mapped_column(Text)


class Reports(Base):
    __tablename__ = "reports"

    __table_args__ = (
        Index("idx_reports_code", "code"),
        Index("idx_reports_code_version", "code", "version"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)


class Modules(Base):
    __tablename__ = "modules"

    __table_args__ = (Index("idx_modules_code", "code"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[str] = mapped_column(String(60), nullable=False)

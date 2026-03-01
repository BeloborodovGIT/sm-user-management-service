from datetime import date

from sqlalchemy import Date, ForeignKey, Index, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Setting(Base):
    __tablename__ = "settings"

    __table_args__ = (
        Index("idx_settings_setting_code_id", "setting_code_id"),
        Index("idx_settings_active_from", "active_from"),
        Index("idx_settings_active_to", "active_to"),
        Index("idx_settings_active_from_active_to", "active_from", "active_to"),
        Index(
            "idx_settings_property_code_id_active_from_active_to",
            "setting_code_id",
            "active_from",
            "active_to",
        ),
        Index("idx_settings_setting_code_id_active_to", "setting_code_id", "active_to"),
    )

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    setting_code_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("settings_dict.id"), nullable=False
    )
    value: Mapped[str] = mapped_column(String(255), nullable=False)
    active_from: Mapped[date] = mapped_column(Date, nullable=False)
    active_to: Mapped[date | None] = mapped_column(Date)


class RoleFunction(Base):
    __tablename__ = "role_functions"

    __table_args__ = (
        Index("idx_role_functions_role_id", "role_id"),
        Index("idx_role_functions_function_code_id", "function_code_id"),
    )

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    role_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("roles_dict.id"), nullable=False
    )
    function_code_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("functions_dict.id"), nullable=False
    )

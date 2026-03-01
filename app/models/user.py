from datetime import date

from sqlalchemy import BigInteger, Boolean, Date, ForeignKey, Index, Integer, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class UserGroup(Base):
    __tablename__ = "user_groups"

    __table_args__ = (Index("idx_user_groups_company_id", "company_id"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("companies.id"), nullable=False
    )
    group_name: Mapped[str] = mapped_column(String(255), nullable=False)
    comment: Mapped[str | None] = mapped_column(String(1000))


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        Index("idx_users_group_id", "group_id"),
        Index("idx_users_timezone_id", "timezone_id"),
        Index("idx_users_company_id", "company_id"),
        Index("idx_users_username", "username"),
        Index("idx_users_company_id_group_id", "company_id", "group_id"),
        Index("idx_users_username_user_lock", "username", "user_lock"),
        Index("idx_users_id_company_id", "id", "company_id"),
        Index("idx_users_id_group_id", "id", "group_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("companies.id"), nullable=False
    )
    group_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user_groups.id"), nullable=False
    )
    timezone_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("timezone_dict.id"), nullable=False
    )
    username: Mapped[str] = mapped_column(String(60), nullable=False)
    firtsname: Mapped[str] = mapped_column(String(60), nullable=False)  # оригинальная опечатка из схемы
    lastname: Mapped[str] = mapped_column(String(60), nullable=False)
    patronymic: Mapped[str | None] = mapped_column(String(60))
    created_date: Mapped[date] = mapped_column(Date, nullable=False)
    user_lock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    comment: Mapped[str | None] = mapped_column(String(1000))


class UserProperties(Base):
    __tablename__ = "user_properties"

    __table_args__ = (
        Index("idx_user_properties_property_id", "user_id"),
        Index(
            "idx_user_properties_property_id_property_code_id",
            "user_id",
            "property_code_id",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=False
    )
    property_code_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("property_code_dict.id"), nullable=False, unique=True
    )
    value: Mapped[str | None] = mapped_column(String(255))


class UserRole(Base):
    __tablename__ = "user_roles"

    __table_args__ = (
        Index("idx_user_roles_user_id", "user_id"),
        Index("idx_user_roles_role_id", "role_id"),
        Index(
            "idx_user_roles_user_id_role_id_active_to",
            "user_id",
            "role_id",
            "active_to",
        ),
        Index("idx_user_roles_active_from", "active_from"),
        Index("idx_user_roles_active_to", "active_to"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=False
    )
    role_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("roles_dict.id"), nullable=False
    )
    active_from: Mapped[date] = mapped_column(Date, nullable=False)
    active_to: Mapped[date | None] = mapped_column(Date)


class UserSending(Base):
    __tablename__ = "user_sendings"

    __table_args__ = (
        Index("idx_user_sendings_user_id", "user_id"),
        Index("idx_user_sendings_status_id", "status_id"),
        Index(
            "idx_user_sendings_user_id_status_id_created_date",
            "user_id",
            "status_id",
            "created_date",
        ),
        Index("idx_user_sendings_created_date", "created_date"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=False, unique=True
    )
    status_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("status_dict.id"), nullable=False
    )
    created_date: Mapped[date] = mapped_column(Date, nullable=False)
    message: Mapped[str] = mapped_column(String(4000), nullable=False)


class UserReportLink(Base):
    __tablename__ = "user_report_links"

    __table_args__ = (
        Index("idx_user_report_links_user_id", "user_id"),
        Index("idx_user_report_links_report_id", "report_id"),
        Index("idx_user_report_links_created_date", "created_date"),
        Index("idx_user_report_links_acive_from", "acive_from"),
        Index("idx_user_report_links_active_to", "active_to"),
        Index("idx_user_report_links_acive_from_active_to", "acive_from", "active_to"),
        Index("idx_user_report_links_user_id_active_to", "user_id", "active_to"),
        Index(
            "idx_user_report_links_user_id_acive_from_active_to",
            "user_id",
            "acive_from",
            "active_to",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=False
    )
    report_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("reports.id"), nullable=False
    )
    created_date: Mapped[date] = mapped_column(Date, nullable=False)
    acive_from: Mapped[date] = mapped_column(Date, nullable=False)  # оригинальная опечатка из схемы
    active_to: Mapped[date | None] = mapped_column(Date)

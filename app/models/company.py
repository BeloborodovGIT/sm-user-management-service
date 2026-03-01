from datetime import date

from sqlalchemy import BigInteger, Date, ForeignKey, Index, Integer, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Company(Base):
    __tablename__ = "companies"

    __table_args__ = (
        Index("idx_companies_inn", "inn"),
        Index("idx_companies_kpp", "kpp"),
        Index("idx_companies_ogrn", "ogrn"),
        Index("idx_companies_bic", "bic"),
        Index("idx_companies_property_id", "property_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    property_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("property_code_dict.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_date: Mapped[date] = mapped_column(Date, nullable=False)
    inn: Mapped[str] = mapped_column(String(16), nullable=False)
    kpp: Mapped[str] = mapped_column(String(9), nullable=False)
    ogrn: Mapped[str | None] = mapped_column(String(13))
    bic: Mapped[str | None] = mapped_column(String(9))


class CompanyProperties(Base):
    __tablename__ = "company_properties"

    __table_args__ = (
        Index("idx_company_properties_company_id", "company_id"),
        Index(
            "idx_company_properties_company_id_property_code_id",
            "company_id",
            "property_code_id",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("companies.id"), nullable=False
    )
    property_code_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("property_code_dict.id"), nullable=False, unique=True
    )
    value: Mapped[str | None] = mapped_column(String(255))


class Department(Base):
    __tablename__ = "departments"

    __table_args__ = (
        Index("idx_departments_code", "code"),
        Index("idx_departments_company_id", "company_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("companies.id"), nullable=False
    )
    code: Mapped[int] = mapped_column(BigInteger, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_date: Mapped[date] = mapped_column(Date, nullable=False)


class License(Base):
    __tablename__ = "license"

    __table_args__ = (
        Index("idx_license_company_id", "company_id"),
        Index("idx_license_company_id_active_from", "company_id", "active_from"),
        Index("idx_license_active_from_active_to", "active_from", "active_to"),
        Index(
            "idx_license_company_id_active_from_active_to",
            "company_id",
            "active_from",
            "active_to",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("companies.id"), nullable=False
    )
    lisense_key: Mapped[str] = mapped_column(String(1000), nullable=False)
    active_from: Mapped[date] = mapped_column(Date, nullable=False)
    active_to: Mapped[date] = mapped_column(Date, nullable=False)


class ModuleCompanyLink(Base):
    __tablename__ = "module_company_links"

    __table_args__ = (
        Index("idx_module_company_links_company_id", "company_id"),
        Index("idx_module_company_links_module_id", "module_id"),
        Index("idx_module_company_links_active_from", "active_from"),
        Index("idx_module_company_links_active_to", "active_to"),
        Index(
            "idx_module_company_links_company_id_active_from_active_to",
            "company_id",
            "active_from",
            "active_to",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    module_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("modules.id"), nullable=False
    )
    company_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("companies.id"), nullable=False
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    active_from: Mapped[date] = mapped_column(Date, nullable=False)
    active_to: Mapped[date | None] = mapped_column(Date)

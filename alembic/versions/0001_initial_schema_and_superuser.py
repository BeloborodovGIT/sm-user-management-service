"""Initial schema and superuser seed.

Revision ID: 0001
Revises:
Create Date: 2026-03-01
"""
from datetime import date, time, timedelta, timezone
from typing import Sequence, Union

from alembic import op
from passlib.context import CryptContext
import sqlalchemy as sa

from app.config import settings

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto",
)


def upgrade() -> None:
    # --- dictionary tables ---
    op.create_table(
        "timezone_dict",
        sa.Column(
            "id", sa.SmallInteger,
            primary_key=True, autoincrement=True,
        ),
        sa.Column(
            "timezone_name", sa.String(255),
            nullable=True,
        ),
        sa.Column(
            "timezone",
            sa.Time(timezone=True),
            nullable=True,
        ),
    )

    op.create_table(
        "property_code_dict",
        sa.Column(
            "id", sa.SmallInteger,
            primary_key=True, autoincrement=True,
        ),
        sa.Column(
            "group_code", sa.String(30),
            nullable=False,
        ),
        sa.Column(
            "code", sa.String(30), nullable=False,
        ),
        sa.Column(
            "name", sa.String(100), nullable=True,
        ),
    )
    op.create_index(
        "idx_property_code_dict_code",
        "property_code_dict", ["code"],
    )
    op.create_index(
        "idx_property_code_dict_group_code_code",
        "property_code_dict",
        ["group_code", "code"],
    )

    op.create_table(
        "roles_dict",
        sa.Column(
            "id", sa.SmallInteger,
            primary_key=True, autoincrement=True,
        ),
        sa.Column(
            "code", sa.String(30), nullable=False,
        ),
        sa.Column(
            "name", sa.String(60), nullable=False,
        ),
    )

    op.create_table(
        "functions_dict",
        sa.Column(
            "id", sa.SmallInteger,
            primary_key=True, autoincrement=True,
        ),
        sa.Column(
            "code", sa.String(30), nullable=False,
        ),
        sa.Column(
            "version", sa.SmallInteger,
            nullable=False,
        ),
    )

    op.create_table(
        "settings_dict",
        sa.Column(
            "id", sa.SmallInteger,
            primary_key=True, autoincrement=True,
        ),
        sa.Column(
            "code", sa.String(30), nullable=False,
        ),
        sa.Column(
            "name", sa.String(255), nullable=False,
        ),
    )
    op.create_index(
        "idx_settings_dict_code",
        "settings_dict", ["code"],
    )

    op.create_table(
        "status_dict",
        sa.Column(
            "id", sa.Integer, primary_key=True,
        ),
        sa.Column(
            "code", sa.String(16), nullable=False,
        ),
        sa.Column(
            "name", sa.String(60), nullable=False,
        ),
    )
    op.create_index(
        "idx_status_dict_code",
        "status_dict", ["code"],
    )

    op.create_table(
        "shablon_dict",
        sa.Column(
            "id", sa.Integer, primary_key=True,
        ),
        sa.Column(
            "code", sa.String(30), nullable=False,
        ),
        sa.Column(
            "name", sa.String(255), nullable=False,
        ),
        sa.Column("value", sa.Text, nullable=True),
    )
    op.create_index(
        "idx_shablon_dict_code",
        "shablon_dict", ["code"],
    )

    op.create_table(
        "reports",
        sa.Column(
            "id", sa.Integer, primary_key=True,
        ),
        sa.Column(
            "code", sa.String(30), nullable=False,
        ),
        sa.Column(
            "name", sa.String, nullable=False,
        ),
        sa.Column(
            "version", sa.Integer, nullable=False,
        ),
    )
    op.create_index(
        "idx_reports_code", "reports", ["code"],
    )
    op.create_index(
        "idx_reports_code_version",
        "reports", ["code", "version"],
    )

    op.create_table(
        "modules",
        sa.Column(
            "id", sa.Integer, primary_key=True,
        ),
        sa.Column(
            "code", sa.String(30), nullable=False,
        ),
        sa.Column(
            "name", sa.String(60), nullable=False,
        ),
    )
    op.create_index(
        "idx_modules_code", "modules", ["code"],
    )

    # --- companies ---
    op.create_table(
        "companies",
        sa.Column(
            "id", sa.BigInteger,
            primary_key=True, autoincrement=True,
        ),
        sa.Column(
            "property_id", sa.SmallInteger,
            sa.ForeignKey(
                "property_code_dict.id",
                ondelete="RESTRICT",
            ),
            nullable=False,
        ),
        sa.Column(
            "name", sa.String(255), nullable=False,
        ),
        sa.Column("created_date", sa.Date, nullable=False),
        sa.Column(
            "inn", sa.String(16), nullable=False,
        ),
        sa.Column(
            "kpp", sa.String(9), nullable=False,
        ),
        sa.Column(
            "ogrn", sa.String(13), nullable=True,
        ),
        sa.Column(
            "bic", sa.String(9), nullable=True,
        ),
    )
    op.create_index(
        "idx_companies_inn", "companies", ["inn"],
    )
    op.create_index(
        "idx_companies_kpp", "companies", ["kpp"],
    )
    op.create_index(
        "idx_companies_ogrn", "companies", ["ogrn"],
    )
    op.create_index(
        "idx_companies_bic", "companies", ["bic"],
    )
    op.create_index(
        "idx_companies_property_id",
        "companies", ["property_id"],
    )

    op.create_table(
        "company_properties",
        sa.Column(
            "id", sa.BigInteger,
            primary_key=True, autoincrement=True,
        ),
        sa.Column(
            "company_id", sa.BigInteger,
            sa.ForeignKey(
                "companies.id", ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "property_code_id", sa.SmallInteger,
            sa.ForeignKey(
                "property_code_dict.id",
                ondelete="RESTRICT",
            ),
            nullable=False, unique=True,
        ),
        sa.Column(
            "value", sa.String(255), nullable=True,
        ),
    )
    op.create_index(
        "idx_company_properties_company_id",
        "company_properties", ["company_id"],
    )
    op.create_index(
        "idx_company_properties_company_id_property_code_id",
        "company_properties",
        ["company_id", "property_code_id"],
    )

    op.create_table(
        "departments",
        sa.Column(
            "id", sa.BigInteger,
            primary_key=True, autoincrement=True,
        ),
        sa.Column(
            "company_id", sa.BigInteger,
            sa.ForeignKey(
                "companies.id", ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "code", sa.BigInteger, nullable=False,
        ),
        sa.Column(
            "name", sa.String(255), nullable=False,
        ),
        sa.Column(
            "created_date", sa.Date, nullable=False,
        ),
    )
    op.create_index(
        "idx_departments_code",
        "departments", ["code"],
    )
    op.create_index(
        "idx_departments_company_id",
        "departments", ["company_id"],
    )

    op.create_table(
        "license",
        sa.Column(
            "id", sa.BigInteger,
            primary_key=True, autoincrement=True,
        ),
        sa.Column(
            "company_id", sa.BigInteger,
            sa.ForeignKey(
                "companies.id", ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "lisense_key", sa.String(1000),
            nullable=False,
        ),
        sa.Column(
            "active_from", sa.Date, nullable=False,
        ),
        sa.Column(
            "active_to", sa.Date, nullable=False,
        ),
    )
    op.create_index(
        "idx_license_company_id",
        "license", ["company_id"],
    )
    op.create_index(
        "idx_license_company_id_active_from",
        "license", ["company_id", "active_from"],
    )
    op.create_index(
        "idx_license_active_from_active_to",
        "license", ["active_from", "active_to"],
    )
    op.create_index(
        "idx_license_company_id_active_from_active_to",
        "license",
        ["company_id", "active_from", "active_to"],
    )

    op.create_table(
        "module_company_links",
        sa.Column(
            "id", sa.BigInteger,
            primary_key=True, autoincrement=True,
        ),
        sa.Column(
            "module_id", sa.Integer,
            sa.ForeignKey(
                "modules.id", ondelete="RESTRICT",
            ),
            nullable=False,
        ),
        sa.Column(
            "company_id", sa.BigInteger,
            sa.ForeignKey(
                "companies.id", ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "position", sa.Integer, nullable=False,
        ),
        sa.Column(
            "active_from", sa.Date, nullable=False,
        ),
        sa.Column(
            "active_to", sa.Date, nullable=True,
        ),
    )
    op.create_index(
        "idx_module_company_links_company_id",
        "module_company_links", ["company_id"],
    )
    op.create_index(
        "idx_module_company_links_module_id",
        "module_company_links", ["module_id"],
    )
    op.create_index(
        "idx_module_company_links_active_from",
        "module_company_links", ["active_from"],
    )
    op.create_index(
        "idx_module_company_links_active_to",
        "module_company_links", ["active_to"],
    )
    op.create_index(
        "idx_module_company_links_company_id_active_from_active_to",
        "module_company_links",
        ["company_id", "active_from", "active_to"],
    )

    # --- user_groups ---
    op.create_table(
        "user_groups",
        sa.Column(
            "id", sa.BigInteger,
            primary_key=True, autoincrement=True,
        ),
        sa.Column(
            "company_id", sa.BigInteger,
            sa.ForeignKey(
                "companies.id", ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "group_name", sa.String(255),
            nullable=False,
        ),
        sa.Column(
            "comment", sa.String(1000),
            nullable=True,
        ),
    )
    op.create_index(
        "idx_user_groups_company_id",
        "user_groups", ["company_id"],
    )

    # --- users ---
    op.create_table(
        "users",
        sa.Column(
            "id", sa.BigInteger,
            primary_key=True, autoincrement=True,
        ),
        sa.Column(
            "company_id", sa.BigInteger,
            sa.ForeignKey(
                "companies.id", ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "group_id", sa.BigInteger,
            sa.ForeignKey(
                "user_groups.id", ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "timezone_id", sa.SmallInteger,
            sa.ForeignKey(
                "timezone_dict.id",
                ondelete="RESTRICT",
            ),
            nullable=False,
        ),
        sa.Column(
            "username", sa.String(60),
            nullable=False,
        ),
        sa.Column(
            "firtsname", sa.String(60),
            nullable=False,
        ),
        sa.Column(
            "lastname", sa.String(60),
            nullable=False,
        ),
        sa.Column(
            "patronymic", sa.String(60),
            nullable=True,
        ),
        sa.Column(
            "created_date", sa.Date, nullable=False,
        ),
        sa.Column(
            "user_lock", sa.Boolean,
            nullable=False, server_default="false",
        ),
        sa.Column(
            "password", sa.String(255),
            nullable=False,
        ),
        sa.Column(
            "comment", sa.String(1000),
            nullable=True,
        ),
    )
    op.create_index(
        "idx_users_group_id",
        "users", ["group_id"],
    )
    op.create_index(
        "idx_users_timezone_id",
        "users", ["timezone_id"],
    )
    op.create_index(
        "idx_users_company_id",
        "users", ["company_id"],
    )
    op.create_index(
        "idx_users_username",
        "users", ["username"],
    )
    op.create_index(
        "idx_users_company_id_group_id",
        "users", ["company_id", "group_id"],
    )
    op.create_index(
        "idx_users_username_user_lock",
        "users", ["username", "user_lock"],
    )

    # --- user child tables ---
    op.create_table(
        "user_properties",
        sa.Column(
            "id", sa.BigInteger,
            primary_key=True, autoincrement=True,
        ),
        sa.Column(
            "user_id", sa.BigInteger,
            sa.ForeignKey(
                "users.id", ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "property_code_id", sa.SmallInteger,
            sa.ForeignKey(
                "property_code_dict.id",
                ondelete="RESTRICT",
            ),
            nullable=False, unique=True,
        ),
        sa.Column(
            "value", sa.String(255), nullable=True,
        ),
    )
    op.create_index(
        "idx_user_properties_property_id",
        "user_properties", ["user_id"],
    )
    op.create_index(
        "idx_user_properties_property_id_property_code_id",
        "user_properties",
        ["user_id", "property_code_id"],
    )

    op.create_table(
        "user_roles",
        sa.Column(
            "id", sa.Integer,
            primary_key=True, autoincrement=True,
        ),
        sa.Column(
            "user_id", sa.BigInteger,
            sa.ForeignKey(
                "users.id", ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "role_id", sa.SmallInteger,
            sa.ForeignKey(
                "roles_dict.id", ondelete="RESTRICT",
            ),
            nullable=False,
        ),
        sa.Column(
            "active_from", sa.Date, nullable=False,
        ),
        sa.Column(
            "active_to", sa.Date, nullable=True,
        ),
    )
    op.create_index(
        "idx_user_roles_user_id",
        "user_roles", ["user_id"],
    )
    op.create_index(
        "idx_user_roles_role_id",
        "user_roles", ["role_id"],
    )
    op.create_index(
        "idx_user_roles_user_id_role_id_active_to",
        "user_roles",
        ["user_id", "role_id", "active_to"],
    )
    op.create_index(
        "idx_user_roles_active_from",
        "user_roles", ["active_from"],
    )
    op.create_index(
        "idx_user_roles_active_to",
        "user_roles", ["active_to"],
    )

    op.create_table(
        "user_sendings",
        sa.Column(
            "id", sa.BigInteger,
            primary_key=True, autoincrement=True,
        ),
        sa.Column(
            "user_id", sa.BigInteger,
            sa.ForeignKey(
                "users.id", ondelete="CASCADE",
            ),
            nullable=False, unique=True,
        ),
        sa.Column(
            "status_id", sa.Integer,
            sa.ForeignKey(
                "status_dict.id",
                ondelete="RESTRICT",
            ),
            nullable=False,
        ),
        sa.Column(
            "created_date", sa.Date, nullable=False,
        ),
        sa.Column(
            "message", sa.String(4000),
            nullable=False,
        ),
    )
    op.create_index(
        "idx_user_sendings_user_id",
        "user_sendings", ["user_id"],
    )
    op.create_index(
        "idx_user_sendings_status_id",
        "user_sendings", ["status_id"],
    )
    op.create_index(
        "idx_user_sendings_user_id_status_id_created_date",
        "user_sendings",
        ["user_id", "status_id", "created_date"],
    )
    op.create_index(
        "idx_user_sendings_created_date",
        "user_sendings", ["created_date"],
    )

    op.create_table(
        "user_report_links",
        sa.Column(
            "id", sa.BigInteger,
            primary_key=True, autoincrement=True,
        ),
        sa.Column(
            "user_id", sa.BigInteger,
            sa.ForeignKey(
                "users.id", ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "report_id", sa.Integer,
            sa.ForeignKey(
                "reports.id", ondelete="RESTRICT",
            ),
            nullable=False,
        ),
        sa.Column(
            "created_date", sa.Date, nullable=False,
        ),
        sa.Column(
            "acive_from", sa.Date, nullable=False,
        ),
        sa.Column(
            "active_to", sa.Date, nullable=True,
        ),
    )
    op.create_index(
        "idx_user_report_links_user_id",
        "user_report_links", ["user_id"],
    )
    op.create_index(
        "idx_user_report_links_report_id",
        "user_report_links", ["report_id"],
    )
    op.create_index(
        "idx_user_report_links_created_date",
        "user_report_links", ["created_date"],
    )
    op.create_index(
        "idx_user_report_links_acive_from",
        "user_report_links", ["acive_from"],
    )
    op.create_index(
        "idx_user_report_links_active_to",
        "user_report_links", ["active_to"],
    )
    op.create_index(
        "idx_user_report_links_acive_from_active_to",
        "user_report_links",
        ["acive_from", "active_to"],
    )
    op.create_index(
        "idx_user_report_links_user_id_active_to",
        "user_report_links",
        ["user_id", "active_to"],
    )
    op.create_index(
        "idx_user_report_links_user_id_acive_from_active_to",
        "user_report_links",
        ["user_id", "acive_from", "active_to"],
    )

    # --- settings ---
    op.create_table(
        "settings",
        sa.Column(
            "id", sa.SmallInteger,
            primary_key=True, autoincrement=True,
        ),
        sa.Column(
            "setting_code_id", sa.SmallInteger,
            sa.ForeignKey(
                "settings_dict.id",
                ondelete="RESTRICT",
            ),
            nullable=False,
        ),
        sa.Column(
            "value", sa.String(255), nullable=False,
        ),
        sa.Column(
            "active_from", sa.Date, nullable=False,
        ),
        sa.Column(
            "active_to", sa.Date, nullable=True,
        ),
    )
    op.create_index(
        "idx_settings_setting_code_id",
        "settings", ["setting_code_id"],
    )
    op.create_index(
        "idx_settings_active_from",
        "settings", ["active_from"],
    )
    op.create_index(
        "idx_settings_active_to",
        "settings", ["active_to"],
    )
    op.create_index(
        "idx_settings_active_from_active_to",
        "settings", ["active_from", "active_to"],
    )
    op.create_index(
        "idx_settings_property_code_id_active_from_active_to",
        "settings",
        ["setting_code_id", "active_from", "active_to"],
    )
    op.create_index(
        "idx_settings_setting_code_id_active_to",
        "settings", ["setting_code_id", "active_to"],
    )

    # --- role_functions ---
    op.create_table(
        "role_functions",
        sa.Column(
            "id", sa.SmallInteger,
            primary_key=True, autoincrement=True,
        ),
        sa.Column(
            "role_id", sa.SmallInteger,
            sa.ForeignKey(
                "roles_dict.id", ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "function_code_id", sa.SmallInteger,
            sa.ForeignKey(
                "functions_dict.id",
                ondelete="RESTRICT",
            ),
            nullable=False,
        ),
    )
    op.create_index(
        "idx_role_functions_role_id",
        "role_functions", ["role_id"],
    )
    op.create_index(
        "idx_role_functions_function_code_id",
        "role_functions", ["function_code_id"],
    )

    # ========================================
    # Seed: superuser role + default admin
    # ========================================
    today = date.today()

    # timezone
    op.execute(
        sa.text(
            "INSERT INTO timezone_dict "
            "(timezone_name, timezone) "
            "VALUES (:tz_name, :tz_val)"
        ).bindparams(
            tz_name="UTC",
            tz_val=time(0, 0, tzinfo=timezone.utc),
        )
    )

    # property_code_dict
    op.execute(
        sa.text(
            "INSERT INTO property_code_dict "
            "(group_code, code, name) "
            "VALUES (:gc, :code, :name)"
        ).bindparams(
            gc="SYSTEM", code="DEFAULT",
            name="Default",
        )
    )

    # roles_dict — superuser
    op.execute(
        sa.text(
            "INSERT INTO roles_dict (code, name) "
            "VALUES (:code, :name)"
        ).bindparams(
            code="superuser", name="Superuser",
        )
    )

    # company
    op.execute(
        sa.text(
            "INSERT INTO companies "
            "(property_id, name, created_date, "
            "inn, kpp) "
            "VALUES ("
            "(SELECT id FROM property_code_dict "
            "WHERE code='DEFAULT' LIMIT 1), "
            ":name, :dt, :inn, :kpp)"
        ).bindparams(
            name="System", dt=today,
            inn="0000000000", kpp="000000000",
        )
    )

    # user_group
    op.execute(
        sa.text(
            "INSERT INTO user_groups "
            "(company_id, group_name) "
            "VALUES ("
            "(SELECT id FROM companies "
            "WHERE name='System' LIMIT 1), "
            ":gn)"
        ).bindparams(gn="Administrators")
    )

    # admin user
    hashed_pw = pwd_context.hash(
        settings.default_superuser_password,
    )
    op.execute(
        sa.text(
            "INSERT INTO users "
            "(company_id, group_id, timezone_id, "
            "username, firtsname, lastname, "
            "created_date, user_lock, password) "
            "VALUES ("
            "(SELECT id FROM companies "
            "WHERE name='System' LIMIT 1), "
            "(SELECT id FROM user_groups "
            "WHERE group_name='Administrators' "
            "LIMIT 1), "
            "(SELECT id FROM timezone_dict "
            "WHERE timezone_name='UTC' LIMIT 1), "
            ":uname, :fname, :lname, "
            ":dt, false, :pw)"
        ).bindparams(
            uname=settings.default_superuser_username,
            fname="Admin", lname="Admin",
            dt=today, pw=hashed_pw,
        )
    )

    # user_role — assign superuser
    op.execute(
        sa.text(
            "INSERT INTO user_roles "
            "(user_id, role_id, active_from) "
            "VALUES ("
            "(SELECT id FROM users "
            "WHERE username=:uname LIMIT 1), "
            "(SELECT id FROM roles_dict "
            "WHERE code='superuser' LIMIT 1), "
            ":dt)"
        ).bindparams(
            uname=settings.default_superuser_username,
            dt=today,
        )
    )


def downgrade() -> None:
    op.drop_table("user_report_links")
    op.drop_table("user_sendings")
    op.drop_table("user_roles")
    op.drop_table("user_properties")
    op.drop_table("users")
    op.drop_table("user_groups")
    op.drop_table("role_functions")
    op.drop_table("settings")
    op.drop_table("module_company_links")
    op.drop_table("license")
    op.drop_table("departments")
    op.drop_table("company_properties")
    op.drop_table("companies")
    op.drop_table("modules")
    op.drop_table("reports")
    op.drop_table("shablon_dict")
    op.drop_table("status_dict")
    op.drop_table("settings_dict")
    op.drop_table("functions_dict")
    op.drop_table("roles_dict")
    op.drop_table("property_code_dict")
    op.drop_table("timezone_dict")

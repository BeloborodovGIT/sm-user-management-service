# Импорт всех моделей нужен для Alembic autogenerate
from app.models.dictionaries import (  # noqa: F401
    FunctionsDict,
    Modules,
    PropertyCodeDict,
    Reports,
    RolesDict,
    SettingsDict,
    ShablonDict,
    StatusDict,
    TimezoneDict,
)
from app.models.company import (  # noqa: F401
    Company,
    CompanyProperties,
    Department,
    License,
    ModuleCompanyLink,
)
from app.models.user import (  # noqa: F401
    User,
    UserGroup,
    UserProperties,
    UserReportLink,
    UserRole,
    UserSending,
)
from app.models.settings import RoleFunction, Setting  # noqa: F401

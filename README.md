# User Management Service

REST API сервис управления пользователями, компаниями, группами и ролями.
Построен на FastAPI + SQLAlchemy (async) + PostgreSQL.

## Стек

- **Python 3.12**, **FastAPI**, **Uvicorn**
- **SQLAlchemy 2.0** (async, asyncpg)
- **Alembic** — миграции
- **PostgreSQL 16**
- **JWT** — аутентификация (python-jose)
- **bcrypt** — хеширование паролей (passlib)
- **Pydantic v2** — валидация

## Быстрый старт

### Docker (рекомендуется)

```bash
docker-compose up --build
```

Сервис поднимется на `http://localhost:8000`.
При старте контейнера автоматически:
1. Применяются Alembic-миграции (`alembic upgrade head`)
2. Создаются все таблицы, справочники и суперюзер

### Локально

```bash
# 1. Поднять PostgreSQL
docker-compose up -d db

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Применить миграции
alembic upgrade head

# 4. Запустить
uvicorn app.main:app --reload
```

## Конфигурация

Все параметры читаются из переменных окружения или файла `.env`:

| Переменная | По умолчанию | Описание |
|---|---|---|
| `DATABASE_URL` | `postgresql+asyncpg://user:password@localhost:5432/user_management` | Строка подключения к БД |
| `SECRET_KEY` | `test-secret` | Секрет для подписи JWT |
| `ALGORITHM` | `HS256` | Алгоритм JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Время жизни токена (мин) |
| `DEBUG` | `false` | Логирование SQL-запросов |
| `DEFAULT_SUPERUSER_USERNAME` | `admin` | Логин суперюзера |
| `DEFAULT_SUPERUSER_PASSWORD` | `changeme` | Пароль суперюзера |

## Суперюзер

При первой миграции создаётся пользователь `admin` / `changeme` с ролью
`superuser`. Этот пользователь имеет доступ ко всем эндпоинтам.

Логин и пароль настраиваются через переменные окружения
`DEFAULT_SUPERUSER_USERNAME` и `DEFAULT_SUPERUSER_PASSWORD`.

## Авторизация

Сервис использует JWT Bearer-токены. Модель доступа:

| Уровень | Описание |
|---|---|
| **Публичный** | Не требует токена |
| **Свой профиль / суперюзер** | Пользователь видит и редактирует только себя; суперюзер — любого |
| **Своя компания / суперюзер** | Пользователь видит свою компанию; суперюзер — любую |
| **Только суперюзер** | Доступ только у пользователей с активной ролью `superuser` |

При self-edit обычный пользователь не может менять поля:
`user_lock`, `group_id`, `company_id`, `timezone_id`.

## API Endpoints

Базовый путь: `/api/v1`

### Auth

| Метод | Путь | Доступ | Описание |
|---|---|---|---|
| POST | `/auth/login` | Публичный | Получить JWT-токен |

**Запрос:**
```json
{ "username": "admin", "password": "changeme" }
```
**Ответ:**
```json
{ "access_token": "eyJ...", "token_type": "bearer" }
```

### Users

| Метод | Путь | Доступ | Описание |
|---|---|---|---|
| POST | `/users/` | Суперюзер | Создать пользователя |
| GET | `/users/` | Суперюзер | Список пользователей |
| GET | `/users/{id}` | Свой / суперюзер | Получить пользователя |
| PATCH | `/users/{id}` | Свой / суперюзер | Обновить пользователя |
| DELETE | `/users/{id}` | Суперюзер | Удалить пользователя |
| GET | `/users/{id}/roles` | Свой / суперюзер | Роли пользователя |
| POST | `/users/{id}/roles` | Суперюзер | Назначить роль |

### Companies

| Метод | Путь | Доступ | Описание |
|---|---|---|---|
| POST | `/companies/` | Публичный | Регистрация компании |
| GET | `/companies/` | Суперюзер | Список компаний |
| GET | `/companies/{id}` | Своя / суперюзер | Получить компанию |
| PATCH | `/companies/{id}` | Суперюзер | Обновить компанию |
| DELETE | `/companies/{id}` | Суперюзер | Удалить компанию |

### Groups

| Метод | Путь | Доступ | Описание |
|---|---|---|---|
| POST | `/groups/` | Суперюзер | Создать группу |
| GET | `/groups/?company_id=` | Суперюзер | Список групп |
| GET | `/groups/{id}` | Суперюзер | Получить группу |
| PATCH | `/groups/{id}` | Суперюзер | Обновить группу |
| DELETE | `/groups/{id}` | Суперюзер | Удалить группу |

### Roles

| Метод | Путь | Доступ | Описание |
|---|---|---|---|
| GET | `/roles/` | Суперюзер | Список ролей |
| GET | `/roles/{id}` | Суперюзер | Получить роль |
| GET | `/roles/{id}/functions` | Суперюзер | Функции роли |
| POST | `/roles/{id}/functions` | Суперюзер | Добавить функцию |
| DELETE | `/roles/{id}/functions/{fid}` | Суперюзер | Удалить функцию |

### Settings

| Метод | Путь | Доступ | Описание |
|---|---|---|---|
| GET | `/settings/` | Суперюзер | Список настроек |
| POST | `/settings/` | Суперюзер | Создать настройку |
| GET | `/settings/{id}` | Суперюзер | Получить настройку |
| PATCH | `/settings/{id}` | Суперюзер | Обновить настройку |
| DELETE | `/settings/{id}` | Суперюзер | Удалить настройку |

### Пагинация

Все list-эндпоинты поддерживают параметры:
- `offset` (>= 0, по умолчанию 0)
- `limit` (1..1000, по умолчанию 100)

## Структура проекта

```
app/
├── main.py              # FastAPI-приложение, lifespan, роутеры
├── config.py            # Настройки из .env / переменных окружения
├── database.py          # Async engine, Base, get_db()
├── auth/
│   ├── jwt.py           # create_access_token, decode_access_token
│   └── dependencies.py  # get_current_user, get_superuser, get_self_or_superuser
├── models/
│   ├── __init__.py      # Импорт всех моделей (для Alembic)
│   ├── dictionaries.py  # TimezoneDict, PropertyCodeDict, RolesDict, ...
│   ├── company.py       # Company, CompanyProperties, Department, License, ...
│   ├── user.py          # User, UserGroup, UserRole, UserProperties, ...
│   └── settings.py      # Setting, RoleFunction
├── schemas/             # Pydantic-схемы (валидация ввода/вывода)
├── repositories/        # Слой доступа к данным (SQLAlchemy queries)
├── services/            # Бизнес-логика
└── routers/             # FastAPI-роутеры (HTTP endpoints)

alembic/
├── env.py               # Async Alembic environment
└── versions/
    └── 0001_initial_schema_and_superuser.py  # Схема + seed
```

## Миграции

```bash
# Применить все миграции
alembic upgrade head

# Откатить последнюю
alembic downgrade -1

# Создать новую миграцию
alembic revision --autogenerate -m "описание"
```

## Схема БД

### Справочники
- `timezone_dict` — часовые пояса
- `property_code_dict` — коды свойств
- `roles_dict` — роли (включая `superuser`)
- `functions_dict` — функции
- `settings_dict` — коды настроек
- `status_dict` — статусы
- `shablon_dict` — шаблоны
- `reports` — отчёты
- `modules` — модули

### Основные таблицы
- `companies` — компании
- `user_groups` — группы пользователей (привязаны к компании)
- `users` — пользователи
- `user_roles` — назначения ролей (с временными окнами `active_from` / `active_to`)
- `role_functions` — привязка функций к ролям
- `settings` — настройки (с временными окнами)

### FK-политики
- **CASCADE** — дочерние записи (user_roles, user_properties, departments, licenses и т.д.)
- **RESTRICT** — ссылки на справочники (нельзя удалить запись справочника, пока на неё ссылаются)

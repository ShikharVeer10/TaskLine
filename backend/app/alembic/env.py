from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool, create_engine
from sqlmodel import SQLModel
from app.core.config import settings
from app.models import User, Task

config = context.config

# Set up Python logging from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# This is the metadata that Alembic uses to detect changes
target_metadata = SQLModel.metadata


def _get_engine_kwargs() -> dict:
    kwargs: dict = {"poolclass": pool.NullPool}
    if settings.DB_ENGINE == "postgresql":
        kwargs["connect_args"] = {"sslmode": "require"}
    return kwargs


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(settings.DATABASE_URL, **_get_engine_kwargs())

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# Determine which mode to run in
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

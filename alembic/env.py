from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool

# 👇 مهم: استيراد Base + engine
from app.data.postgres import Base, engine

# 👇 مهم: استيراد كل الـ models
from app.data import models  # noqa: F401

# Alembic Config
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 👇 دي أهم سطر في الملف كله
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in offline mode"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in online mode"""

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

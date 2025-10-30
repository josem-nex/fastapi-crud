import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

from core.config import get_settings
from db.base import Base
from models import *

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
settings = get_settings()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = async_engine_from_config(
        {"sqlalchemy.url": settings.database_url},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async def _do_run_migrations(connection):
        def _run_migrations_sync(sync_conn):
            context.configure(
                connection=sync_conn,
                target_metadata=target_metadata,
                compare_type=True,
            )
            with context.begin_transaction():
                context.run_migrations()

        await connection.run_sync(_run_migrations_sync)

    async def _run():
        async with connectable.connect() as connection:
            await _do_run_migrations(connection)
        await connectable.dispose()

    asyncio.run(_run())

run_migrations_online()
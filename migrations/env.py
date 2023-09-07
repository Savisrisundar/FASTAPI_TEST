from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sys import modules
from alembic import context
from test_app.core.db import Base
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
target_metadata.naming_convention={
    "ix":"ix_%(column_0_label)s",
    "uq":"uq_%(table_name)s_%(column_0_name)s",
    "ck":"ck_%(table_name)s_%(constraint_name)s",
    "fk":"fk_%(table_name)s_%(column_0_name)" "s_%(referred_table_name)s",
    "pk":"pk_%(table_name)s",
}
from test_app.users.models import User

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    if "pytest" in modules:
        url=os.getenv("DB_SYNC_TEST_CONNECTION_STR")
    else:
        url=os.getenv("DB_SYNC_CONNECTION_STR")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    config_section=config.get_section(config.config_ini_section)
    if "pytest" in modules:
        url= os.getenv("DB_SYNC_TEST_CONNECTION_STR")
    else:
        url= os.getenv("DB_SYNC_CONNECTION_STR")
        
    config_section["sqlalchemy.url"]=url
    connectable = engine_from_config(
        config_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

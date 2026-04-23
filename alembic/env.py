import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context


# adendos nossos
import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from geoalchemy2.alembic_helpers import include_object as geo_include_object
from geoalchemy2.alembic_helpers import render_item

from backend.app.database.database import Base
from backend.app.database.models import Unidade, Paciente
import geoalchemy2


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


def custom_include_object(obj, name, type_, reflected, compare_to):
    postgis_tables = {
        "spatial_ref_sys", "topology", "layer", "addr", "cousub", "county", 
        "state", "zcta5", "tract", "tabblock", "bg", "faces", "edges", 
        "addrfeat", "place", "featnames", "zip_lookup", "zip_lookup_all", 
        "zip_lookup_base", "county_lookup", "countysub_lookup", 
        "direction_lookup", "geocode_settings", "geocode_settings_default", 
        "loader_lookuptables", "loader_platform", "loader_variables", 
        "pagc_gaz", "pagc_lex", "pagc_rules", "place_lookup", 
        "secondary_unit_lookup", "state_lookup", "street_type_lookup", 
        "zip_state", "zip_state_loc", "tabblock20"
    }
    if type_ == "table" and name in postgis_tables:
        return False

    return geo_include_object(obj, name, type_, reflected, compare_to)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata, include_object=custom_include_object, render_item=render_item)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

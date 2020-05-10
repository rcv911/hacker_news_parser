from __future__ import with_statement
from alembic import context
from logging.config import fileConfig

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
import os
import sys

sys.path.append(os.getcwd())
print(os.getcwd())
# Interpret the config file for Python logging.
# This line sets up loggers basically.
config = context.config
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
url = config.get_main_option("sqlalchemy.url")
print(url)
from connection import Connection
from models._base import Base

con = Connection(dsn=url)
engine = con.engine
target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline():
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
        url=url, compare_type=True, target_metadata=target_metadata,
        literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def include_object(object, name, type_, reflected, compare_to):
    print(name, target_metadata.schema)
    if type_ == 'table' and object.schema in (target_metadata.schema, ''):
        print(object, name, type_, reflected, compare_to)
        return True
    elif type_ == 'column' and object.table.schema in (
    target_metadata.schema, ''):
        print(object, name, type_, reflected, compare_to)
        return True
    else:
        return False


def run_migrations_online():
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema=target_metadata.schema,
            include_schemas=True,
            compare_type=True,
            include_object=include_object
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

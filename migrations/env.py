from logging.config import fileConfig
from alembic import context
from fast_zero.models import Base
from fast_zero.settings import Settings

config = context.config
config.set_main_option('sqlalchemy.url', Settings().DATABASE_URL)


if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata    

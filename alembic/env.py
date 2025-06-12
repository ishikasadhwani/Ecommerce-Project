import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# ✅ 1. Add your app folder to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ✅ 2. Load environment variables
from dotenv import load_dotenv
load_dotenv()

# ✅ 3. Import your Base and models
from app.core.database import Base
from app.auth.models import User, PasswordResetToken
from app.products.models import Product
from app.cart.models import CartItem
from app.orders.models import Order, OrderItem

# ✅ 4. Set up Alembic config
config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# ✅ 5. Logging setup
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ 6. Target metadata for autogeneration
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

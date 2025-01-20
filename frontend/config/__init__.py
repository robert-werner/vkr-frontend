import os

DATABASE_URL = f"postgresql+asyncpg://{os.environ["POSTGRESQL_USERNAME"]}:{os.environ["POSTGRESQL_PASSWORD"]}@localhost:{os.environ["POSTGRESQL_PORT"]}/vkr"
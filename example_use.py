import asyncio

import asyncpg

from migrations import (
    Migrator,
    SqlFile,
)


async def main():
    # 1. Настройка подключения
    dsn = "postgresql://myuser:mypassword@localhost:5433/migrations_db"
    conn: asyncpg.Connection = await asyncpg.connect(dsn)

    # 2. Определение списка миграций (порядок имеет значение!)
    migrations = [
        SqlFile("example_migrations/create_users.sql"),
        SqlFile("example_migrations/folder1/add_column_name_users.sql"),
        SqlFile("example_migrations/folder1/folder2/create_cart.sql"),
        SqlFile("example_migrations/folder3/create_cart2.sql"),
    ]

    # 3. Инициализация и запуск
    migrator = Migrator(connection=conn, log=True)
    
    try:
        await migrator.apply_all(migrations)
        await migrator.print_applied_migrations()
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())

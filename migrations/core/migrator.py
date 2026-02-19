from pathlib import Path

from asyncpg import Connection

from migrations.core.sqlfile import SqlFile
from migrations.core.log import MigrationLog


class Migrator:
    
    BASE_SQL_DIR = Path(__file__).parent.parent / "sql"

    def __init__(
        self,
        connection: Connection,
        log: bool | None = None
    ):
        self.log: MigrationLog = MigrationLog(log or False)
        self.connection: Connection = connection

    async def apply_all(self, migrations: list[SqlFile]) -> None:
        migration_checksum: dict[str, str] = {}
        sql_setup = await SqlFile(self.BASE_SQL_DIR / "create_table_migrations.sql").read()
        sql_insert = await SqlFile(self.BASE_SQL_DIR / "insert_migration.sql").read()
        sql_update_filename = await SqlFile(self.BASE_SQL_DIR / "update_filename.sql").read()
        sql_update_abspath = await SqlFile(self.BASE_SQL_DIR / "update_abspath.sql").read()
        sql_check = await SqlFile(self.BASE_SQL_DIR / "check_migration.sql").read()

        count_applied: int = 0
        count_skipped: int = 0
        current_migration: str = "initialization"
        abs_path: str = "/"

        await self.connection.execute(sql_setup)

        try:
            async with self.connection.transaction():
                for migration in migrations:
                    sql_checksum = await migration.get_checksum()
                    abs_path = str(migration.path.absolute())
                    
                    current_migration = migration.path.name

                    row = await self.connection.fetchrow(sql_check, sql_checksum)

                    is_active_transaction = sql_checksum in migration_checksum
                    if is_active_transaction:
                        duplicate_migration = migration_checksum[sql_checksum]
                        self.log.skipped(abs_path)
                        count_skipped += 1
                        self.log.message("Duplicate SQL:" \
                                         f"\n    1. {duplicate_migration}" \
                                         f"\n    2. {abs_path}")
                    elif row is None:
                        # if no record is found, apply migration and add to the table
                        await self.connection.execute(await migration.read())
                        await self.connection.execute(sql_insert, current_migration, abs_path, sql_checksum)
                        self.log.applied(abs_path)
                        migration_checksum[sql_checksum] = abs_path
                        count_applied += 1
                    else:
                        message_log = ""
                        # If found, skip it; if the filename is different, update it in the DB
                        if row["filename"] != current_migration:
                            message_log += f"    Update filename [\n        {row['filename']} -> \n        {current_migration}\n    ]"
                            await self.connection.execute(sql_update_filename, current_migration, sql_checksum)
                        if row["abs_path"] != abs_path:
                            message_log += f"\n    Update ABS Path [\n        {row['abs_path']} -> \n        {abs_path}\n    ]"
                            await self.connection.execute(sql_update_abspath, abs_path, sql_checksum)
                        if message_log != "":
                            self.log.message(f"info migration:\n{message_log}")
                        self.log.skipped(abs_path)
                        count_skipped += 1
        except Exception as error:
            self.log.failed(abs_path)
            self.log.error(error)
            raise error
        finally:
            self.log.result(len(migrations), count_applied, count_skipped)

    async def print_applied_migrations(self) -> None:
        sql_query = await SqlFile(self.BASE_SQL_DIR / "select_applied_migrations.sql").read()

        rows = await self.connection.fetch(sql_query)

        if not rows:
            self.log.message("No migrations have been applied yet.")
            return

        for row in rows:
            applied_at = row["applied_at"].strftime("%Y-%m-%d %H:%M:%S")
            short_hash = row["checksum"][:8]
            abs_path = row["abs_path"]
            self.log.message(f"{applied_at} | {short_hash} | {abs_path}")
        return

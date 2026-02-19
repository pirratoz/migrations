SELECT
    *
FROM schema_migrations
WHERE
    checksum = $1;
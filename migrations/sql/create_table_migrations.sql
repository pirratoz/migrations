CREATE TABLE IF NOT EXISTS schema_migrations (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL,
    abs_path TEXT NOT NULL,
    checksum VARCHAR(64) NOT NULL UNIQUE,
    applied_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (now() AT TIME ZONE 'UTC')
);

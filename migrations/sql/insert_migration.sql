INSERT INTO schema_migrations (filename, abs_path, checksum)
VALUES ($1, $2, $3)
ON CONFLICT (checksum) DO NOTHING;

UPDATE schema_migrations 
SET
    abs_path = $1
WHERE checksum = $2;

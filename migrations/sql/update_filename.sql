UPDATE schema_migrations 
SET
    filename = $1
WHERE checksum = $2;

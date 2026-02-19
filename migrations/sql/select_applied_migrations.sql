SELECT 
    filename,
    abs_path, 
    checksum, 
    applied_at 
FROM 
    schema_migrations 
ORDER BY 
    applied_at ASC;
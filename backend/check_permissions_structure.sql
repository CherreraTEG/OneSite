-- Script SQL para verificar la estructura de permisos
-- Ejecutar en el cliente SQL apropiado

-- 1. Verificar si existe la tabla user_company_permission
SELECT 
    CASE 
        WHEN EXISTS (
            SELECT 1 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'user_company_permission'
        ) 
        THEN 'Tabla user_company_permission EXISTE' 
        ELSE 'Tabla user_company_permission NO EXISTE' 
    END AS status_tabla;

-- 2. Ver estructura de la tabla (si existe)
SELECT 
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE,
    COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'user_company_permission'
ORDER BY ORDINAL_POSITION;

-- 3. Contar registros existentes
SELECT COUNT(*) as total_permisos FROM user_company_permission;

-- 4. Ver algunos ejemplos de permisos (si existen)
SELECT TOP 5 
    user_id,
    company_id
FROM user_company_permission;

-- 5. Ver empresas activas disponibles
SELECT TOP 5
    id_Company,
    Company,
    BU,
    Estado_Cargue
FROM TheEliteGroup_Parameters.Companies 
WHERE Estado_Cargue = 1;

-- 6. Ejemplo de cómo insertar permisos de prueba
-- DESCOMENTAR Y AJUSTAR IDs SEGÚN SEA NECESARIO:
-- INSERT INTO user_company_permission (user_id, company_id) VALUES (1, 1);
-- INSERT INTO user_company_permission (user_id, company_id) VALUES (1, 2);
-- Script para crear la tabla de empresas
-- Ejecutar en SQL Server

-- Crear la tabla companies
CREATE TABLE companies (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL,
    code NVARCHAR(50) NOT NULL UNIQUE,
    description NVARCHAR(500) NULL,
    is_active BIT NOT NULL DEFAULT 1,
    created_at DATETIME2 DEFAULT GETDATE() NOT NULL,
    updated_at DATETIME2 DEFAULT GETDATE() NOT NULL
);

-- Crear índices para mejorar el rendimiento
CREATE INDEX IX_companies_name ON companies(name);
CREATE INDEX IX_companies_code ON companies(code);
CREATE INDEX IX_companies_is_active ON companies(is_active);

-- Insertar datos de ejemplo
INSERT INTO companies (name, code, description, is_active) VALUES
('Elite Flower', 'ELF', 'Empresa líder en exportación de flores', 1),
('FlorAndina', 'FLA', 'Especialistas en flores andinas', 1),
('Agroelite', 'AGE', 'Agroindustria de élite', 1),
('Flores del Valle', 'FDV', 'Flores cultivadas en el valle', 1),
('ExportFlora', 'EXF', 'Exportadores de flora colombiana', 1);

-- Crear trigger para actualizar automáticamente updated_at
CREATE TRIGGER TR_companies_updated_at
ON companies
AFTER UPDATE
AS
BEGIN
    UPDATE companies 
    SET updated_at = GETDATE()
    FROM companies c
    INNER JOIN inserted i ON c.id = i.id;
END;

-- Verificar la creación
SELECT * FROM companies; 
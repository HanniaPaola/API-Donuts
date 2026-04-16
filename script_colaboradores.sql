-- ============================================================================
-- Script para insertar datos de prueba de colaboradores (Donuts)
-- ============================================================================
-- Tabla: colaboradores
-- Campos: display_name, handle, bio, specialty, product_count, sales_count, is_online, status
-- ============================================================================

USE tienda_db;

-- Limpiar datos existentes (opcional)
-- TRUNCATE TABLE colaboradores;

-- Insertar colaboradores de prueba (coinciden con datos in-memory del frontend)
INSERT INTO colaboradores (display_name, handle, bio, specialty, product_count, sales_count, is_online, status) 
VALUES 
  (
    'Mariana Lopez',
    '@maria.donas',
    'Especialista en donas artesanales con glaseados únicos y rellenos caseros.',
    'donas',
    12,
    320,
    1,
    'active'
  ),
  (
    'Carlos Mendez',
    '@carlos.galletas',
    'Galletas con chips de chocolate y recetas de la abuela, horneadas cada mañana.',
    'galletas',
    8,
    156,
    1,
    'active'
  ),
  (
    'Ana Ruiz',
    '@ana.bebidas',
    'Smoothies, cafés fríos y bebidas vegetales para acompañar tu dulce favorito.',
    'bebidas',
    15,
    410,
    0,
    'active'
  ),
  (
    'Laura Vega',
    '@laura.donas',
    'Donas veganas y opciones sin gluten con ingredientes locales.',
    'donas',
    10,
    198,
    1,
    'active'
  );

-- Verificar inserción
SELECT * FROM colaboradores;

-- ============================================================================
-- Línea a ejecutar desde PowerShell:
-- mysql -u root -p tienda_db < script_colaboradores.sql
-- (Luego ingresar contraseña cuando se solicite)
-- 
-- O desde MySQL Workbench:
-- 1. Copy-paste todo el contenido en una nueva query
-- 2. Presionar Ctrl+Enter para ejecutar
-- ============================================================================

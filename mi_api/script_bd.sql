-- script_bd.sql
-- Script de creación de base de datos y tablas para la API Donuts
-- Compatible con MySQL 5.7+

-- ==================== CREAR BASE DE DATOS ====================
CREATE DATABASE IF NOT EXISTS tienda_db;
USE tienda_db;

-- ==================== TABLA: USUARIO_ADMIN ====================
CREATE TABLE IF NOT EXISTS usuario_admin (
    id_admin INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==================== TABLA: USUARIO_COMPRADOR ====================
CREATE TABLE IF NOT EXISTS usuario_comprador (
    id_comprador INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==================== TABLA: PRODUCTO ====================
CREATE TABLE IF NOT EXISTS producto (
    id_producto INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(150) NOT NULL,
    precio FLOAT NOT NULL,
    categoria VARCHAR(100),
    stock_disponible INT DEFAULT 0,
    id_admin INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_producto_admin FOREIGN KEY (id_admin) REFERENCES usuario_admin(id_admin) ON DELETE CASCADE,
    INDEX idx_nombre (nombre),
    INDEX idx_categoria (categoria),
    INDEX idx_id_admin (id_admin)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==================== TABLA: CARRITO ====================
CREATE TABLE IF NOT EXISTS carrito (
    id_carrito INT PRIMARY KEY AUTO_INCREMENT,
    subtotal FLOAT DEFAULT 0.0,
    cantidad_items INT DEFAULT 0,
    id_comprador INT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_carrito_comprador FOREIGN KEY (id_comprador) REFERENCES usuario_comprador(id_comprador) ON DELETE CASCADE,
    INDEX idx_id_comprador (id_comprador)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==================== TABLA: CARRITO_PRODUCTO ====================
CREATE TABLE IF NOT EXISTS carrito_producto (
    id_carrito_producto INT PRIMARY KEY AUTO_INCREMENT,
    id_carrito INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT DEFAULT 1,
    precio_unitario FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_carrito_producto_carrito FOREIGN KEY (id_carrito) REFERENCES carrito(id_carrito) ON DELETE CASCADE,
    CONSTRAINT fk_carrito_producto_producto FOREIGN KEY (id_producto) REFERENCES producto(id_producto) ON DELETE CASCADE,
    UNIQUE KEY uk_carrito_producto (id_carrito, id_producto),
    INDEX idx_id_carrito (id_carrito),
    INDEX idx_id_producto (id_producto)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==================== TABLA: PEDIDO ====================
CREATE TABLE IF NOT EXISTS pedido (
    id_pedido INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    precio_total FLOAT NOT NULL,
    metodo_pago VARCHAR(50) NOT NULL,
    id_comprador INT NOT NULL,
    id_producto INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pedido_comprador FOREIGN KEY (id_comprador) REFERENCES usuario_comprador(id_comprador) ON DELETE CASCADE,
    CONSTRAINT fk_pedido_producto FOREIGN KEY (id_producto) REFERENCES producto(id_producto) ON DELETE CASCADE,
    INDEX idx_id_comprador (id_comprador),
    INDEX idx_id_producto (id_producto),
    INDEX idx_fecha (fecha)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==================== ÍNDICES ADICIONALES ====================
-- Para optimizar búsquedas frecuentes
ALTER TABLE usuario_admin ADD INDEX idx_created_at (created_at);
ALTER TABLE usuario_comprador ADD INDEX idx_created_at (created_at);

-- ==================== DATOS DE PRUEBA (OPCIONAL) ====================
-- Descomenta si quieres insertar datos de prueba

-- INSERT INTO usuario_admin (nombre, contrasena) 
-- VALUES ('admin', '$2b$12$abcdefghijklmnopqrstuvwxyz...');  -- Contrasena hasheada

-- INSERT INTO usuario_comprador (nombre, contrasena) 
-- VALUES ('comprador1', '$2b$12$abcdefghijklmnopqrstuvwxyz...');  -- Contrasena hasheada

-- ==================== VERIFICACIÓN ====================
-- Para verificar que todo se creó correctamente, ejecuta:
-- SHOW TABLES;
-- DESCRIBE usuario_admin;
-- DESCRIBE usuario_comprador;
-- DESCRIBE producto;
-- DESCRIBE carrito;
-- DESCRIBE carrito_producto;
-- DESCRIBE pedido;

-- ============================================================================
-- API Donuts — script completo de base de datos (MySQL 5.7+)
-- Incluye: creación de BD, tablas, índices y datos iniciales de colaboradores.
-- Ejecutar una vez en limpio, o solo la parte de datos si las tablas ya existen.
-- ============================================================================

CREATE DATABASE IF NOT EXISTS tienda_db;
USE tienda_db;

-- ==================== USUARIO_ADMIN ====================
CREATE TABLE IF NOT EXISTS usuario_admin (
    id_admin INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==================== USUARIO_COMPRADOR ====================
CREATE TABLE IF NOT EXISTS usuario_comprador (
    id_comprador INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==================== COLABORADORES (DoniDeli / frontend) ====================
CREATE TABLE IF NOT EXISTS colaboradores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(120) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NULL,
    display_name VARCHAR(100) NOT NULL,
    handle VARCHAR(50) NOT NULL UNIQUE,
    bio VARCHAR(500),
    specialty VARCHAR(50) NOT NULL,
    product_count INT DEFAULT 0,
    sales_count INT DEFAULT 0,
    is_online TINYINT(1) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active',
    INDEX idx_specialty (specialty),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==================== PRODUCTO ====================
CREATE TABLE IF NOT EXISTS producto (
    id_producto INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(150) NOT NULL,
    precio FLOAT NOT NULL,
    categoria VARCHAR(100),
    stock_disponible INT DEFAULT 0,
    id_admin INT NOT NULL,
    id_colaborador INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_producto_admin FOREIGN KEY (id_admin) REFERENCES usuario_admin(id_admin) ON DELETE CASCADE,
    CONSTRAINT fk_producto_colaborador FOREIGN KEY (id_colaborador) REFERENCES colaboradores(id) ON DELETE SET NULL,
    INDEX idx_nombre (nombre),
    INDEX idx_categoria (categoria),
    INDEX idx_id_admin (id_admin),
    INDEX idx_id_colaborador (id_colaborador)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==================== CARRITO ====================
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

-- ==================== CARRITO_PRODUCTO ====================
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

-- ==================== PEDIDO (cabecera) ====================
CREATE TABLE IF NOT EXISTS pedido (
    id_pedido INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    precio_total FLOAT NOT NULL,
    metodo_pago VARCHAR(50) NOT NULL,
    id_comprador INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pedido_comprador FOREIGN KEY (id_comprador) REFERENCES usuario_comprador(id_comprador) ON DELETE CASCADE,
    INDEX idx_id_comprador (id_comprador),
    INDEX idx_fecha (fecha)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==================== PEDIDO_ITEMS (líneas del pedido) ====================
CREATE TABLE IF NOT EXISTS pedido_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_pedido INT NOT NULL,
    id_producto INT NOT NULL,
    producto_nombre VARCHAR(150) NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario FLOAT NOT NULL,
    subtotal FLOAT NOT NULL,
    CONSTRAINT fk_pi_pedido FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido) ON DELETE CASCADE,
    CONSTRAINT fk_pi_producto FOREIGN KEY (id_producto) REFERENCES producto(id_producto) ON DELETE RESTRICT,
    INDEX idx_id_pedido (id_pedido),
    INDEX idx_id_producto (id_producto)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==================== DATOS INICIALES: USUARIOS (login local / DoniDeli) ====================
-- Contraseñas: comprador@donideli.com → buyer123 | admin@donideli.com → admin123 (bcrypt)
INSERT IGNORE INTO usuario_admin (nombre, contrasena) VALUES
(
  'admin@donideli.com',
  '$2b$12$ML4j1HTJLi/.jdfH7xcMuOPA8MPu5E4zKh3II4IU3zez8V30Mr4WS'
);

INSERT IGNORE INTO usuario_comprador (nombre, contrasena) VALUES
(
  'comprador@donideli.com',
  '$2b$12$3MMF4fh7SiI9/9OMXVbt9eQcpWJumxV.UbDz7kfKIGJUivv5SKlN2'
);

INSERT INTO carrito (id_comprador, subtotal, cantidad_items)
SELECT c.id_comprador, 0, 0
FROM usuario_comprador c
WHERE c.nombre = 'comprador@donideli.com'
  AND NOT EXISTS (SELECT 1 FROM carrito k WHERE k.id_comprador = c.id_comprador);

-- ==================== DATOS INICIALES: COLABORADORES ====================
INSERT INTO colaboradores (
    email, display_name, handle, bio, specialty, product_count, sales_count, is_online, status
) VALUES
  (
    'mariana@donideli.com',
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
    'carlos@donideli.com',
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
    'ana@donideli.com',
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
    'laura@donideli.com',
    'Laura Vega',
    '@laura.donas',
    'Donas veganas y opciones sin gluten con ingredientes locales.',
    'donas',
    10,
    198,
    1,
    'active'
  ),
  (
    'admin@donideli.com',
    'Admin DoniDeli',
    '@admin.donideli',
    'Gestión oficial de DoniDeli. Donas, galletas y bebidas directas del equipo fundador.',
    'donas',
    14,
    530,
    1,
    'active'
  );

-- Verificación
SHOW TABLES;
SELECT * FROM colaboradores;

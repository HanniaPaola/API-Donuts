# README.md

# 🍩 API Donuts - REST API con FastAPI

Una API REST completa para gestión de tienda de donuts con autenticación JWT, arquitectura en capas y base de datos MySQL.

## 📋 Características

- ✅ **Arquitectura en 4 capas** (Presentación, Servicios, Repositorios, Modelos)
- ✅ **Autenticación JWT** con Bearer tokens
- ✅ **Contraseñas hasheadas** con bcrypt
- ✅ **Gestión de productos** (CRUD)
- ✅ **Carrito de compras** con persistencia
- ✅ **Sistema de pedidos** con control de stock
- ✅ **Documentación automática** con Swagger (OpenAPI)
- ✅ **CORS habilitado** para peticiones desde cualquier origen
- ✅ **Validación de datos** con Pydantic
- ✅ **Base de datos MySQL** con SQLAlchemy ORM

## 🛠️ Stack Tecnológico

- **Python** 3.8.6
- **FastAPI** 0.95.2
- **SQLAlchemy** 1.4.46 (ORM)
- **PyMySQL** 1.0.2 (Conector MySQL)
- **Pydantic** 1.10.11 (Validación)
- **Uvicorn** 0.21.0 (Servidor ASGI)
- **JWT** para autenticación
- **Bcrypt** para hashing de contraseñas

## 📁 Estructura de Proyecto

```
mi_api/
├── main.py                        ← Punto de entrada FastAPI
├── database.py                    ← Configuración SQLAlchemy + MySQL
├── auth.py                        ← JWT y hashing de contraseñas
│
├── models/                        ← CAPA 4: Modelos ORM
│   ├── __init__.py
│   ├── usuario_comprador.py
│   ├── usuario_admin.py
│   ├── producto.py
│   ├── carrito.py
│   ├── carrito_producto.py
│   └── pedido.py
│
├── schemas/                       ← CAPA 4: Esquemas Pydantic
│   ├── __init__.py
│   ├── usuario_comprador.py
│   ├── usuario_admin.py
│   ├── producto.py
│   ├── carrito.py
│   └── pedido.py
│
├── repositories/                  ← CAPA 3: Acceso a datos
│   ├── __init__.py
│   ├── usuario_comprador_repo.py
│   ├── usuario_admin_repo.py
│   ├── producto_repo.py
│   ├── carrito_repo.py
│   └── pedido_repo.py
│
├── services/                      ← CAPA 2: Lógica de negocio
│   ├── __init__.py
│   ├── usuario_comprador_service.py
│   ├── usuario_admin_service.py
│   ├── producto_service.py
│   ├── carrito_service.py
│   └── pedido_service.py
│
├── routers/                       ← CAPA 1: Endpoints HTTP
│   ├── __init__.py
│   ├── compradores.py
│   ├── admins.py
│   ├── productos.py
│   ├── carrito.py
│   └── pedidos.py
│
├── requirements.txt
├── script_bd.sql
└── .env.example
```

## 🚀 Instalación y Configuración

### 1. Crear la base de datos MySQL

```sql
-- Ejecutar el script SQL en tu cliente MySQL
mysql -u root < script_bd.sql
```

O manualmente:

```sql
CREATE DATABASE tienda_db;
USE tienda_db;
-- (Luego ejecutar el contenido de script_bd.sql)
```

### 2. Instalar dependencias Python

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
copy .env.example .env

# Editar .env con tus valores
# (Principalmente DB_PASSWORD si tienes)
```

### 4. Ejecutar el servidor

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**La API estará disponible en:** `http://127.0.0.1:8000`

**Documentación interactiva:** `http://127.0.0.1:8000/docs`

## 📚 Endpoints Disponibles

### 🔐 Autenticación (Sin protección)

#### Compradores
- `POST /compradores/registro` - Registrar nuevo comprador
- `POST /compradores/login` - Login y obtener token JWT
- `GET /compradores/{id}` - Obtener datos del comprador

#### Administradores
- `POST /admins/registro` - Registrar nuevo admin
- `POST /admins/login` - Login admin y obtener token JWT

### 📦 Productos (Solo lectura sin token)

- `GET /productos` - Listar todos los productos
- `GET /productos/{id}` - Obtener un producto específico
- `POST /productos` - Crear producto (⚠️ Requiere token admin)
- `PUT /productos/{id}` - Actualizar producto (⚠️ Requiere token admin)
- `DELETE /productos/{id}` - Eliminar producto (⚠️ Requiere token admin)

### 🛒 Carrito (⚠️ Requiere token comprador)

- `GET /carrito/{id_comprador}` - Ver carrito
- `POST /carrito/{id_comprador}/agregar` - Agregar producto
- `DELETE /carrito/{id_comprador}/quitar/{id_producto}` - Quitar producto

### 📋 Pedidos (⚠️ Requiere token comprador)

- `POST /pedidos` - Crear pedido desde carrito
- `GET /pedidos/{id_comprador}` - Historial de pedidos
- `GET /pedidos/detalle/{id_pedido}` - Detalle de un pedido

## 🔑 Autenticación JWT

### Cómo usar los tokens

1. **Registrarse o hacer login** para obtener un token:

```bash
POST /compradores/login
{
  "nombre": "usuario",
  "contrasena": "password123"
}

Respuesta:
{
  "id_comprador": 1,
  "nombre": "usuario",
  "token": "eyJhbGc...",
  "tipo_token": "bearer"
}
```

2. **Usar el token** en headers de requests protegidos:

```bash
Authorization: Bearer eyJhbGc...
```

### En Swagger (http://127.0.0.1:8000/docs)

- Haz clic en "Authorize" 🔒
- Paste el token: `Bearer eyJhbGc...`
- Los endpoints protegidos ahora funcionarán

## 📝 Ejemplos de Uso

### Ejemplo 1: Registrar un comprador

```bash
curl -X POST "http://127.0.0.1:8000/compradores/registro" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "juan_perez",
    "contrasena": "password123"
  }'
```

### Ejemplo 2: Login y obtener token

```bash
curl -X POST "http://127.0.0.1:8000/compradores/login" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "juan_perez",
    "contrasena": "password123"
  }'
```

Respuesta:
```json
{
  "id_comprador": 1,
  "nombre": "juan_perez",
  "token": "eyJhbGc...",
  "tipo_token": "bearer"
}
```

### Ejemplo 3: Agregar producto al carrito (requiere token)

```bash
curl -X POST "http://127.0.0.1:8000/carrito/1/agregar" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGc..." \
  -d '{
    "id_producto": 1,
    "cantidad": 2
  }'
```

### Ejemplo 4: Crear un pedido

```bash
curl -X POST "http://127.0.0.1:8000/pedidos" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGc..." \
  -d '{
    "metodo_pago": "tarjeta"
  }'
```

## 🏗️ Arquitectura en Capas Explicada

La API sigue una arquitectura de **4 capas** con un flujo de dependencias estricto:

```
Router (Capa 1: Presentación HTTP)
   ↓
Service (Capa 2: Lógica de negocio)
   ↓
Repository (Capa 3: Acceso a datos)
   ↓
Model/DB (Capa 4: Base de datos)
```

### ¿Por qué esta arquitectura?

- **Separación de responsabilidades**: Cada capa tiene una responsabilidad clara
- **Fácil de mantener**: Cambios en BD no afectan los routers
- **Testeable**: Cada capa se puede testear por separado
- **Escalable**: Fácil agregar nuevas funcionalidades
- **Reutilizable**: Los servicios pueden usarse en múltiples routers

## 🔒 Seguridad

### Contraseñas

- Se hashean con **bcrypt** (algoritmo salted hash)
- **NUNCA** se guardan en texto plano
- Verificación segura con `verify_password()`

### JWT

- Tokens con expiración (24 horas por defecto)
- Verificación en cada request protegido
- Usa algoritmo HS256

### CORS

- Habilitado para todos los orígenes (cambiar en producción)
- Protege endpoints sensibles con autenticación

## 🧪 Casos de Validación

La API valida automáticamente:

### Usuarios
- ✅ Nombre no vacío y único
- ✅ Contraseña mínimo 6 caracteres
- ✅ Contraseña correcta en login

### Productos
- ✅ Nombre no vacío
- ✅ Precio mayor a 0
- ✅ Stock no negativo
- ✅ Solo el admin creador puede modificar

### Carrito
- ✅ Producto existe
- ✅ Stock suficiente
- ✅ Cantidad positiva
- ✅ El comprador puede ver solo su carrito

### Pedidos
- ✅ Carrito no vacío
- ✅ Stock suficiente al crear pedido
- ✅ Descuento de stock automático
- ✅ El comprador puede ver solo sus pedidos

## 🐛 Troubleshooting

### "Connection refused" a MySQL

```bash
# Verificar que MySQL esté ejecutándose
# Windows: Verificar Services
# Linux: sudo systemctl status mysql
# macOS: brew services list
```

### "No such table" error

```bash
# Ejecutar el script SQL
mysql -u root < script_bd.sql

# O desde Python:
from database import crear_tablas
crear_tablas()
```

### Token inválido

```bash
# Asegúrate de incluir "Bearer " antes del token
Authorization: Bearer eyJhbGc...  # ✅ Correcto
Authorization: eyJhbGc...        # ❌ Incorrecto
```

## 📦 Desarrollo

### Instalar dependencias de desarrollo

```bash
pip install pytest pytest-asyncio httpx
```

### Ejecutar con recarga automática

```bash
uvicorn main:app --reload
```

### Generar nuevas migraciones (si usas Alembic)

```bash
alembic revision --autogenerate -m "descripcion"
```

## 📄 Licencia

MIT

## 👨‍💻 Autor

API REST creada con FastAPI, SQLAlchemy y MySQL

---

**Última actualización:** 14 de Abril de 2026

**Estado:** ✅ Producción lista

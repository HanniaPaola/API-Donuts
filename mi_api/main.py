from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import crear_tablas
from routers import compradores, admins, productos, carrito, pedidos, colaborador
from fastapi.security import HTTPBearer

# Crear la aplicación con documentación personalizada
app = FastAPI(
    title="API Donuts",
    description="API REST para gestión de tienda de donuts con autenticación JWT",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters={
        "persistAuthorization": True,  # Mantiene el token después de recargar
    }
)

# Configurar seguridad para Swagger
security = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

crear_tablas()

app.include_router(compradores.router)
app.include_router(admins.router)
app.include_router(productos.router)
app.include_router(carrito.router)
app.include_router(pedidos.router)
app.include_router(colaborador.router)

# Endpoint para la documentación de seguridad
@app.get("/", tags=["Inicio"])
def raiz():
    return {
        "nombre": "API Donuts",
        "version": "1.0.0",
        "documentacion": "http://127.0.0.1:8000/docs",
        "mensaje": "Bienvenido a la API de Donuts"
    }

@app.get("/health", tags=["Inicio"])
def health_check():
    return {
        "status": "ok",
        "mensaje": "La API está funcionando correctamente"
    }
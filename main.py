import asyncio
import logging
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

from database import crear_tablas
from exception_handlers import register_exception_handlers
from logging_config import setup_logging
from routers import compradores, admins, productos, carrito, pedidos, colaborador, chat

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Espera a que MariaDB acepte conexiones antes de create_all (evita crash loop en Fly)."""
    last_exc: BaseException | None = None
    for attempt in range(30):
        try:
            crear_tablas()
            last_exc = None
            break
        except BaseException as exc:
            last_exc = exc
            logger.warning(
                "crear_tablas intento %s/30: %s",
                attempt + 1,
                exc,
            )
            await asyncio.sleep(2)
    if last_exc is not None:
        logger.exception("No se pudo inicializar el esquema en la base de datos")
        raise last_exc
    yield


app = FastAPI(
    title="API Donuts",
    description="API REST para gestión de tienda de donuts con autenticación JWT",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters={
        "persistAuthorization": True,
    },
    lifespan=lifespan,
)

security = HTTPBearer()


@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    """Propaga X-Request-ID para correlación en logs y monitoreo."""
    rid = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.request_id = rid
    response = await call_next(request)
    response.headers["X-Request-ID"] = rid
    return response


register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(compradores.router)
app.include_router(admins.router)
app.include_router(productos.router)
app.include_router(carrito.router)
app.include_router(pedidos.router)
app.include_router(colaborador.router)
app.include_router(chat.router)


@app.get("/", tags=["Inicio"])
def raiz():
    return {
        "nombre": "API Donuts",
        "version": "1.0.0",
        "documentacion": "/docs",
        "mensaje": "Bienvenido a la API de Donuts",
    }


@app.get("/health", tags=["Inicio"])
def health_check():
    return {
        "status": "ok",
        "mensaje": "La API está funcionando correctamente",
    }

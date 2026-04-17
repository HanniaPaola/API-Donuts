# routers/compradores.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from services import usuario_comprador_service
from schemas import (
    UsuarioCompradorCreate,
    UsuarioCompradorLogin,
    UsuarioCompradorResponse
)
import traceback

router = APIRouter(
    prefix="/compradores",
    tags=["Compradores"]
)

@router.post("/registro", response_model=dict, status_code=status.HTTP_201_CREATED)
def registrar_comprador(
    datos: UsuarioCompradorCreate,
    db: Session = Depends(get_db)
):
    try:
        print(f"Intentando registrar comprador: {datos.nombre}")
        resultado = usuario_comprador_service.registrar_comprador(
            db,
            datos.nombre,
            datos.contrasena
        )
        print(f"Registro exitoso: {resultado}")
        return resultado
    except ValueError as e:
        print(f"Error de validación: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error inesperado: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar comprador: {str(e)}"
        )

@router.post("/login", response_model=dict)
def login_comprador(
    datos: UsuarioCompradorLogin,
    db: Session = Depends(get_db)
):
    try:
        username = datos.username
        if not username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debe proporcionar nombre o email"
            )
            
        resultado = usuario_comprador_service.login_comprador(
            db,
            username,
            datos.contrasena
        )
        return resultado
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en login: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al hacer login: {str(e)}"
        )

@router.get("/{id_comprador}", response_model=UsuarioCompradorResponse)
def obtener_comprador(
    id_comprador: int,
    db: Session = Depends(get_db)
):
    try:
        resultado = usuario_comprador_service.obtener_comprador(db, id_comprador)
        return resultado
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error al obtener comprador: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener comprador"
        )
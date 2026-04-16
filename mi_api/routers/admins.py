# routers/admins.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from services import usuario_admin_service
from schemas import (
    UsuarioAdminCreate,
    UsuarioAdminLogin,
    UsuarioAdminResponse
)
import traceback

router = APIRouter(
    prefix="/admins",
    tags=["Administradores"]
)

@router.post("/registro", response_model=dict, status_code=status.HTTP_201_CREATED)
def registrar_admin(
    datos: UsuarioAdminCreate,
    db: Session = Depends(get_db)
):
    try:
        print(f"=== REGISTRO ADMIN ===")
        print(f"Nombre: {datos.nombre}")
        resultado = usuario_admin_service.registrar_admin(
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
            detail=f"Error al registrar admin: {str(e)}"
        )

@router.post("/login", response_model=dict)
def login_admin(
    datos: UsuarioAdminLogin,
    db: Session = Depends(get_db)
):
    try:
        username = datos.username
        if not username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debe proporcionar nombre o email"
            )
        resultado = usuario_admin_service.login_admin(
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
        print(f"Error en login admin: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al hacer login: {str(e)}"
        )

@router.get("/{id_admin}", response_model=UsuarioAdminResponse)
def obtener_admin(
    id_admin: int,
    db: Session = Depends(get_db)
):
    try:
        resultado = usuario_admin_service.obtener_admin(db, id_admin)
        return resultado
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error al obtener admin: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener admin"
        )
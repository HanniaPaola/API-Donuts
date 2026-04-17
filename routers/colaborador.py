from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.colaborador import ColaboradorCreate, ColaboradorUpdate, CollaboratorPublic
from services.colaborador_service import ColaboradorService

router = APIRouter(prefix="/colaboradores", tags=["Colaboradores"])


@router.get("/specialty/{specialty}", response_model=List[CollaboratorPublic])
def get_colaboradores_by_specialty(specialty: str, db: Session = Depends(get_db)):
    try:
        return ColaboradorService.get_colaboradores_by_specialty(db, specialty)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/online", response_model=List[CollaboratorPublic])
def get_online_colaboradores(db: Session = Depends(get_db)):
    return ColaboradorService.get_online_colaboradores(db)


@router.get("/", response_model=List[CollaboratorPublic])
def get_all_colaboradores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        data = ColaboradorService.get_all_colaboradores(db, skip, limit)
        return data["colaboradores"]
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/", response_model=CollaboratorPublic, status_code=status.HTTP_201_CREATED)
def create_colaborador(colaborador_data: ColaboradorCreate, db: Session = Depends(get_db)):
    try:
        return ColaboradorService.create_colaborador(db, colaborador_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{colaborador_id}", response_model=CollaboratorPublic)
def get_colaborador(colaborador_id: int, db: Session = Depends(get_db)):
    try:
        return ColaboradorService.get_colaborador_by_id(db, colaborador_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{colaborador_id}", response_model=CollaboratorPublic)
def update_colaborador(
    colaborador_id: int,
    update_data: ColaboradorUpdate,
    db: Session = Depends(get_db),
):
    try:
        return ColaboradorService.update_colaborador(db, colaborador_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{colaborador_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_colaborador(colaborador_id: int, db: Session = Depends(get_db)):
    try:
        ColaboradorService.delete_colaborador(db, colaborador_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

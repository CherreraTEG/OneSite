from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.trucks import Truck, TruckCreate, TruckUpdate
from app.crud.crud_trucks import crud_truck
from app.db.base import get_db
from datetime import date

router = APIRouter()

@router.get("/trucks", response_model=List[Truck])
def read_trucks(
    skip: int = 0,
    limit: int = 100,
    id_empresa: Optional[int] = Query(None, alias="id_empresa"),
    id_warehouse: Optional[int] = Query(None, alias="id_warehouse"),
    carrier: Optional[str] = Query(None, alias="carrier"),
    date_from: Optional[date] = Query(None, alias="date_from"),
    date_to: Optional[date] = Query(None, alias="date_to"),
    id_customer: Optional[int] = Query(None, alias="id_customer"),
    estatus: Optional[int] = Query(None, alias="estatus"),
    load_number: Optional[str] = Query(None, alias="load_number"),
    db: Session = Depends(get_db)
):
    return crud_truck.get_multi(
        db, 
        skip=skip, 
        limit=limit, 
        id_empresa=id_empresa,
        id_warehouse=id_warehouse, 
        carrier=carrier, 
        date_from=date_from, 
        date_to=date_to,
        id_customer=id_customer,
        estatus=estatus,
        load_number=load_number
    )

@router.get("/trucks/{truck_id}", response_model=Truck)
def read_truck(truck_id: int, db: Session = Depends(get_db)):
    db_truck = crud_truck.get(db, truck_id)
    if not db_truck:
        raise HTTPException(status_code=404, detail="Truck not found")
    return db_truck

@router.post("/trucks", response_model=Truck)
def create_truck(truck: TruckCreate, db: Session = Depends(get_db)):
    return crud_truck.create(db, truck)

@router.put("/trucks/{truck_id}", response_model=Truck)
def update_truck(truck_id: int, truck: TruckUpdate, db: Session = Depends(get_db)):
    db_truck = crud_truck.get(db, truck_id)
    if not db_truck:
        raise HTTPException(status_code=404, detail="Truck not found")
    return crud_truck.update(db, db_truck, truck)

@router.delete("/trucks/{truck_id}", response_model=Truck)
def delete_truck(truck_id: int, db: Session = Depends(get_db)):
    db_truck = crud_truck.get(db, truck_id)
    if not db_truck:
        raise HTTPException(status_code=404, detail="Truck not found")
    return crud_truck.remove(db, truck_id)

@router.get("/trucks/empresa/{id_empresa}/warehouse/{id_warehouse}", response_model=List[Truck])
def read_trucks_by_empresa_and_warehouse(
    id_empresa: int,
    id_warehouse: int,
    db: Session = Depends(get_db)
):
    return crud_truck.get_by_empresa_and_warehouse(db, id_empresa, id_warehouse)

@router.get("/trucks/empresa/{id_empresa}/warehouse/{id_warehouse}/dates", response_model=List[Truck])
def read_trucks_by_empresa_warehouse_and_dates(
    id_empresa: int,
    id_warehouse: int,
    date_from: date = Query(..., alias="date_from"),
    date_to: date = Query(..., alias="date_to"),
    db: Session = Depends(get_db)
):
    return crud_truck.get_by_empresa_warehouse_and_dates(db, id_empresa, id_warehouse, date_from, date_to)

@router.get("/trucks/warehouse/{id_warehouse}/dates", response_model=List[Truck])
def read_trucks_by_warehouse_and_dates(
    id_warehouse: int,
    date_from: date = Query(..., alias="date_from"),
    date_to: date = Query(..., alias="date_to"),
    db: Session = Depends(get_db)
):
    return crud_truck.get_by_warehouse_and_dates(db, id_warehouse, date_from, date_to)

@router.get("/trucks/carrier/{carrier}", response_model=List[Truck])
def read_trucks_by_carrier(carrier: str, db: Session = Depends(get_db)):
    return crud_truck.get_by_carrier(db, carrier)

@router.get("/trucks/load/{load_number}", response_model=Truck)
def read_truck_by_load_number(load_number: str, db: Session = Depends(get_db)):
    db_truck = crud_truck.get_by_load_number(db, load_number)
    if not db_truck:
        raise HTTPException(status_code=404, detail="Truck not found")
    return db_truck 
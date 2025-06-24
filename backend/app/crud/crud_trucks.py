from sqlalchemy.orm import Session
from app.models.trucks import Truck
from app.schemas.trucks import TruckCreate, TruckUpdate
from typing import List, Optional
from datetime import date

class CRUDTruck:
    def get(self, db: Session, truck_id: int) -> Optional[Truck]:
        return db.query(Truck).filter(Truck.id == truck_id).first()

    def get_multi(self, db: Session, *, skip=0, limit=100, id_empresa=None, id_warehouse=None, carrier=None, date_from=None, date_to=None, id_customer=None, estatus=None, load_number=None) -> List[Truck]:
        query = db.query(Truck)
        
        if id_empresa:
            query = query.filter(Truck.id_empresa == id_empresa)
        if id_warehouse:
            query = query.filter(Truck.id_warehouse == id_warehouse)
        if carrier:
            query = query.filter(Truck.carrier == carrier)
        if date_from:
            query = query.filter(Truck.ship_date >= date_from)
        if date_to:
            query = query.filter(Truck.ship_date <= date_to)
        if id_customer:
            query = query.filter(Truck.id_customer == id_customer)
        if estatus is not None:
            query = query.filter(Truck.estatus == estatus)
        if load_number:
            query = query.filter(Truck.load_number == load_number)
            
        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: TruckCreate) -> Truck:
        db_obj = Truck(**obj_in.dict(exclude_unset=True))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Truck, obj_in: TruckUpdate) -> Truck:
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, truck_id: int) -> Optional[Truck]:
        obj = db.query(Truck).get(truck_id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def get_by_empresa_and_warehouse(self, db: Session, id_empresa: int, id_warehouse: int) -> List[Truck]:
        return db.query(Truck).filter(
            Truck.id_empresa == id_empresa,
            Truck.id_warehouse == id_warehouse
        ).all()

    def get_by_empresa_warehouse_and_dates(self, db: Session, id_empresa: int, id_warehouse: int, date_from: date, date_to: date) -> List[Truck]:
        return db.query(Truck).filter(
            Truck.id_empresa == id_empresa,
            Truck.id_warehouse == id_warehouse,
            Truck.ship_date >= date_from,
            Truck.ship_date <= date_to
        ).all()

    def get_by_warehouse_and_dates(self, db: Session, id_warehouse: int, date_from: date, date_to: date) -> List[Truck]:
        return db.query(Truck).filter(
            Truck.id_warehouse == id_warehouse,
            Truck.ship_date >= date_from,
            Truck.ship_date <= date_to
        ).all()

    def get_by_carrier(self, db: Session, carrier: str) -> List[Truck]:
        return db.query(Truck).filter(Truck.carrier == carrier).all()

    def get_by_load_number(self, db: Session, load_number: str) -> Optional[Truck]:
        return db.query(Truck).filter(Truck.load_number == load_number).first()

crud_truck = CRUDTruck() 
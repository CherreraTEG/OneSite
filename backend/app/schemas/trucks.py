from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime

class TruckBase(BaseModel):
    id_empresa: Optional[int] = None
    id_warehouse: Optional[int] = None
    ship_date: Optional[date] = None
    deliv_date: Optional[date] = None
    carrier: Optional[str] = None
    customer_facility: Optional[str] = None
    po: Optional[str] = None
    qty: Optional[float] = None
    estatus: Optional[int] = None
    time_in: Optional[time] = None
    door: Optional[str] = None
    time_out: Optional[time] = None
    comments: Optional[str] = None
    pickup_location: Optional[str] = None
    load_number: Optional[str] = None
    id_customer: Optional[int] = None
    estado_cargue: Optional[int] = None
    update_date: Optional[datetime] = None
    update_user: Optional[str] = None
    file_name: Optional[str] = None

class TruckCreate(TruckBase):
    pass

class TruckUpdate(TruckBase):
    pass

class TruckInDBBase(TruckBase):
    id: int
    
    class Config:
        from_attributes = True

class Truck(TruckInDBBase):
    pass 
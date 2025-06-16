from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PermisoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    activo: bool = True

class PermisoCreate(PermisoBase):
    pass

class PermisoUpdate(PermisoBase):
    pass

class PermisoInDB(PermisoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True 
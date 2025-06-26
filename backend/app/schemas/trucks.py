from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time, datetime

class TruckBase(BaseModel):
    """
    Modelo base para los datos de camiones.
    
    Este modelo contiene todos los campos disponibles para un camión,
    todos ellos opcionales para permitir flexibilidad en las operaciones.
    """
    
    id_empresa: Optional[int] = Field(None, description="ID de la empresa propietaria del camión", ge=1)
    id_warehouse: Optional[int] = Field(None, description="ID del almacén donde se encuentra el camión", ge=1)
    ship_date: Optional[date] = Field(None, description="Fecha de envío del camión (YYYY-MM-DD)")
    deliv_date: Optional[date] = Field(None, description="Fecha de entrega programada (YYYY-MM-DD)")
    carrier: Optional[str] = Field(None, description="Nombre de la empresa transportista", max_length=200)
    customer_facility: Optional[str] = Field(None, description="Instalación o centro del cliente", max_length=200)
    po: Optional[str] = Field(None, description="Número de orden de compra (Purchase Order)", max_length=200)
    qty: Optional[float] = Field(None, description="Cantidad de carga en el camión", ge=0)
    estatus: Optional[int] = Field(None, description="Estado actual del camión (0=Inactivo, 1=Activo, etc.)")
    time_in: Optional[time] = Field(None, description="Hora de entrada del camión al almacén (HH:MM:SS)")
    door: Optional[str] = Field(None, description="Número o identificador de la puerta asignada", max_length=25)
    time_out: Optional[time] = Field(None, description="Hora de salida del camión del almacén (HH:MM:SS)")
    comments: Optional[str] = Field(None, description="Comentarios adicionales sobre el camión", max_length=1000)
    pickup_location: Optional[str] = Field(None, description="Ubicación donde se recogerá la carga", max_length=150)
    load_number: Optional[str] = Field(None, description="Número único de identificación de la carga", max_length=50)
    id_customer: Optional[int] = Field(None, description="ID del cliente para quien se transporta la carga", ge=1)
    estado_cargue: Optional[int] = Field(None, description="Estado de la carga (0=Pendiente, 1=Cargando, 2=Completado)")
    update_date: Optional[datetime] = Field(None, description="Fecha y hora de la última actualización del registro")
    update_user: Optional[str] = Field(None, description="Usuario que realizó la última actualización", max_length=50)
    file_name: Optional[str] = Field(None, description="Nombre del archivo asociado al camión", max_length=100)

    class Config:
        """Configuración del modelo Pydantic"""
        json_schema_extra = {
            "example": {
                "id_empresa": 1,
                "id_warehouse": 1,
                "ship_date": "2025-06-26",
                "deliv_date": "2025-06-27",
                "carrier": "Transporte ABC S.A.",
                "customer_facility": "Centro de Distribución Norte",
                "po": "PO-2025-001",
                "qty": 100.5,
                "estatus": 1,
                "time_in": "08:30:00",
                "door": "A1",
                "time_out": "16:45:00",
                "comments": "Carga urgente para cliente VIP",
                "pickup_location": "Zona de carga norte",
                "load_number": "LOAD-2025-001",
                "id_customer": 1,
                "estado_cargue": 1,
                "update_date": "2025-06-26T12:00:00",
                "update_user": "admin",
                "file_name": "truck_data_001.csv"
            }
        }

class TruckCreate(TruckBase):
    """
    Modelo para crear un nuevo camión.
    
    Hereda todos los campos de TruckBase. Todos los campos son opcionales,
    pero se recomienda proporcionar al menos los campos básicos para
    un registro completo.
    """
    
    class Config:
        """Configuración del modelo para creación"""
        json_schema_extra = {
            "example": {
                "id_empresa": 1,
                "id_warehouse": 1,
                "ship_date": "2025-06-26",
                "carrier": "Transporte ABC S.A.",
                "load_number": "LOAD-2025-001",
                "estatus": 1,
                "update_user": "admin"
            }
        }

class TruckUpdate(TruckBase):
    """
    Modelo para actualizar un camión existente.
    
    Hereda todos los campos de TruckBase. Solo se actualizarán
    los campos que se proporcionen en la petición.
    """
    
    class Config:
        """Configuración del modelo para actualización"""
        json_schema_extra = {
            "example": {
                "carrier": "Nuevo Transportista XYZ",
                "estatus": 2,
                "comments": "Camión actualizado con nueva información",
                "update_user": "admin"
            }
        }

class TruckInDBBase(TruckBase):
    """
    Modelo base para camiones en la base de datos.
    
    Incluye el ID único del camión que se genera automáticamente
    en la base de datos.
    """
    
    id: int = Field(..., description="ID único del camión generado automáticamente", ge=1)
    
    class Config:
        """Configuración del modelo para respuestas de BD"""
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "id_empresa": 1,
                "id_warehouse": 1,
                "ship_date": "2025-06-26",
                "deliv_date": "2025-06-27",
                "carrier": "Transporte ABC S.A.",
                "customer_facility": "Centro de Distribución Norte",
                "po": "PO-2025-001",
                "qty": 100.5,
                "estatus": 1,
                "time_in": "08:30:00.000000",
                "door": "A1",
                "time_out": "16:45:00.000000",
                "comments": "Carga urgente para cliente VIP",
                "pickup_location": "Zona de carga norte",
                "load_number": "LOAD-2025-001",
                "id_customer": 1,
                "estado_cargue": 1,
                "update_date": "2025-06-26T12:00:00.000000",
                "update_user": "admin",
                "file_name": "truck_data_001.csv"
            }
        }

class Truck(TruckInDBBase):
    """
    Modelo completo de camión para respuestas de la API.
    
    Este es el modelo que se utiliza para todas las respuestas
    de la API que devuelven datos de camiones.
    """
    pass 
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.trucks import Truck, TruckCreate, TruckUpdate
from app.crud.crud_trucks import crud_truck
from app.db.base import get_db
from datetime import date
import logging

# Configurar logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get(
    "/trucks", 
    response_model=List[Truck],
    summary="Obtener lista de camiones",
    description="Retorna una lista paginada de camiones con filtros opcionales por empresa, almacén, transportista, fechas, cliente, estado y número de carga.",
    response_description="Lista de camiones encontrados",
    tags=["trucks"]
)
def read_trucks(
    skip: int = Query(0, description="Número de registros a omitir para paginación", ge=0),
    limit: int = Query(100, description="Número máximo de registros a retornar", ge=1, le=1000),
    id_empresa: Optional[int] = Query(None, description="ID de la empresa para filtrar"),
    id_warehouse: Optional[int] = Query(None, description="ID del almacén para filtrar"),
    carrier: Optional[str] = Query(None, description="Nombre del transportista para filtrar"),
    date_from: Optional[date] = Query(None, description="Fecha de inicio para filtrar por fecha de envío (YYYY-MM-DD)"),
    date_to: Optional[date] = Query(None, description="Fecha de fin para filtrar por fecha de envío (YYYY-MM-DD)"),
    id_customer: Optional[int] = Query(None, description="ID del cliente para filtrar"),
    estatus: Optional[int] = Query(None, description="Estado del camión para filtrar"),
    load_number: Optional[str] = Query(None, description="Número de carga para filtrar"),
    db: Session = Depends(get_db)
):
    """
    Obtiene una lista paginada de camiones con filtros opcionales.
    
    **Parámetros de paginación:**
    - `skip`: Número de registros a omitir (para paginación)
    - `limit`: Número máximo de registros a retornar (máximo 1000)
    
    **Filtros disponibles:**
    - `id_empresa`: Filtrar por empresa específica
    - `id_warehouse`: Filtrar por almacén específico
    - `carrier`: Filtrar por transportista
    - `date_from` y `date_to`: Filtrar por rango de fechas de envío
    - `id_customer`: Filtrar por cliente específico
    - `estatus`: Filtrar por estado del camión
    - `load_number`: Filtrar por número de carga
    
    **Ejemplo de uso:**
    ```
    GET /api/v1/trucks?skip=0&limit=10&id_empresa=1&carrier=ABC
    ```
    """
    try:
        logger.info(f"Obteniendo trucks con parámetros: skip={skip}, limit={limit}")
        result = crud_truck.get_multi(
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
        logger.info(f"Se encontraron {len(result)} trucks")
        return result
    except Exception as e:
        logger.error(f"Error al obtener trucks: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get(
    "/trucks/{truck_id}", 
    response_model=Truck,
    summary="Obtener camión por ID",
    description="Retorna los detalles completos de un camión específico por su ID.",
    response_description="Detalles del camión encontrado",
    tags=["trucks"]
)
def read_truck(
    truck_id: int = Path(..., description="ID único del camión", ge=1),
    db: Session = Depends(get_db)
):
    """
    Obtiene los detalles completos de un camión específico por su ID.
    
    **Parámetros:**
    - `truck_id`: ID único del camión (debe ser mayor a 0)
    
    **Respuestas:**
    - `200`: Camión encontrado exitosamente
    - `404`: Camión no encontrado
    
    **Ejemplo de uso:**
    ```
    GET /api/v1/trucks/1
    ```
    """
    try:
        logger.info(f"Obteniendo truck con ID: {truck_id}")
        db_truck = crud_truck.get(db, truck_id)
        if not db_truck:
            logger.warning(f"Truck con ID {truck_id} no encontrado")
            raise HTTPException(status_code=404, detail="Truck not found")
        logger.info(f"Truck encontrado: {db_truck}")
        return db_truck
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener truck {truck_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.post(
    "/trucks", 
    response_model=Truck,
    summary="Crear nuevo camión",
    description="Crea un nuevo registro de camión con los datos proporcionados.",
    response_description="Camión creado exitosamente",
    status_code=201,
    tags=["trucks"]
)
def create_truck(
    truck: TruckCreate,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo registro de camión.
    
    **Campos requeridos:**
    - Todos los campos son opcionales, pero se recomienda proporcionar al menos los campos básicos
    
    **Campos disponibles:**
    - `id_empresa`: ID de la empresa
    - `id_warehouse`: ID del almacén
    - `ship_date`: Fecha de envío (YYYY-MM-DD)
    - `deliv_date`: Fecha de entrega (YYYY-MM-DD)
    - `carrier`: Nombre del transportista
    - `customer_facility`: Instalación del cliente
    - `po`: Número de orden de compra
    - `qty`: Cantidad
    - `estatus`: Estado del camión
    - `time_in`: Hora de entrada (HH:MM:SS)
    - `door`: Puerta
    - `time_out`: Hora de salida (HH:MM:SS)
    - `comments`: Comentarios
    - `pickup_location`: Ubicación de recogida
    - `load_number`: Número de carga
    - `id_customer`: ID del cliente
    - `estado_cargue`: Estado de carga
    - `update_date`: Fecha de actualización (ISO format)
    - `update_user`: Usuario que actualizó
    - `file_name`: Nombre del archivo
    
    **Ejemplo de uso:**
    ```json
    {
      "id_empresa": 1,
      "id_warehouse": 1,
      "ship_date": "2025-06-26",
      "carrier": "Transporte ABC",
      "load_number": "LOAD-001"
    }
    ```
    """
    try:
        logger.info(f"Recibida petición para crear truck: {truck}")
        result = crud_truck.create(db, truck)
        logger.info(f"Truck creado exitosamente: {result}")
        return result
    except Exception as e:
        logger.error(f"Error al crear truck: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.put(
    "/trucks/{truck_id}", 
    response_model=Truck,
    summary="Actualizar camión",
    description="Actualiza los datos de un camión existente por su ID.",
    response_description="Camión actualizado exitosamente",
    tags=["trucks"]
)
def update_truck(
    truck_id: int = Path(..., description="ID único del camión a actualizar", ge=1),
    truck: TruckUpdate = None,
    db: Session = Depends(get_db)
):
    """
    Actualiza los datos de un camión existente.
    
    **Parámetros:**
    - `truck_id`: ID único del camión a actualizar
    
    **Campos actualizables:**
    - Todos los campos del modelo Truck son actualizables
    
    **Respuestas:**
    - `200`: Camión actualizado exitosamente
    - `404`: Camión no encontrado
    
    **Ejemplo de uso:**
    ```json
    {
      "carrier": "Nuevo Transportista",
      "estatus": 1,
      "comments": "Actualizado"
    }
    ```
    """
    try:
        logger.info(f"Actualizando truck con ID: {truck_id}")
        db_truck = crud_truck.get(db, truck_id)
        if not db_truck:
            logger.warning(f"Truck con ID {truck_id} no encontrado para actualizar")
            raise HTTPException(status_code=404, detail="Truck not found")
        result = crud_truck.update(db, db_truck, truck)
        logger.info(f"Truck actualizado exitosamente: {result}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al actualizar truck {truck_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.delete(
    "/trucks/{truck_id}", 
    response_model=Truck,
    summary="Eliminar camión",
    description="Elimina un camión existente por su ID.",
    response_description="Camión eliminado exitosamente",
    tags=["trucks"]
)
def delete_truck(
    truck_id: int = Path(..., description="ID único del camión a eliminar", ge=1),
    db: Session = Depends(get_db)
):
    """
    Elimina un camión existente.
    
    **Parámetros:**
    - `truck_id`: ID único del camión a eliminar
    
    **Respuestas:**
    - `200`: Camión eliminado exitosamente
    - `404`: Camión no encontrado
    
    **Ejemplo de uso:**
    ```
    DELETE /api/v1/trucks/1
    ```
    """
    try:
        logger.info(f"Eliminando truck con ID: {truck_id}")
        result = crud_truck.remove(db, truck_id)
        if not result:
            logger.warning(f"Truck con ID {truck_id} no encontrado para eliminar")
            raise HTTPException(status_code=404, detail="Truck not found")
        logger.info(f"Truck eliminado exitosamente: {result}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al eliminar truck {truck_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get(
    "/trucks/empresa/{id_empresa}/warehouse/{id_warehouse}", 
    response_model=List[Truck],
    summary="Obtener camiones por empresa y almacén",
    description="Retorna todos los camiones de una empresa y almacén específicos.",
    response_description="Lista de camiones encontrados",
    tags=["trucks"]
)
def read_trucks_by_empresa_and_warehouse(
    id_empresa: int = Path(..., description="ID de la empresa", ge=1),
    id_warehouse: int = Path(..., description="ID del almacén", ge=1),
    db: Session = Depends(get_db)
):
    """
    Obtiene todos los camiones de una empresa y almacén específicos.
    
    **Parámetros:**
    - `id_empresa`: ID de la empresa
    - `id_warehouse`: ID del almacén
    
    **Ejemplo de uso:**
    ```
    GET /api/v1/trucks/empresa/1/warehouse/1
    ```
    """
    try:
        logger.info(f"Obteniendo trucks por empresa {id_empresa} y warehouse {id_warehouse}")
        result = crud_truck.get_by_empresa_and_warehouse(db, id_empresa, id_warehouse)
        logger.info(f"Se encontraron {len(result)} trucks")
        return result
    except Exception as e:
        logger.error(f"Error al obtener trucks por empresa y warehouse: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get(
    "/trucks/empresa/{id_empresa}/warehouse/{id_warehouse}/dates", 
    response_model=List[Truck],
    summary="Obtener camiones por empresa, almacén y fechas",
    description="Retorna camiones de una empresa y almacén específicos dentro de un rango de fechas.",
    response_description="Lista de camiones encontrados",
    tags=["trucks"]
)
def read_trucks_by_empresa_warehouse_and_dates(
    id_empresa: int = Path(..., description="ID de la empresa", ge=1),
    id_warehouse: int = Path(..., description="ID del almacén", ge=1),
    date_from: date = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    date_to: date = Query(..., description="Fecha de fin (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Obtiene camiones de una empresa y almacén específicos dentro de un rango de fechas.
    
    **Parámetros:**
    - `id_empresa`: ID de la empresa
    - `id_warehouse`: ID del almacén
    - `date_from`: Fecha de inicio del rango
    - `date_to`: Fecha de fin del rango
    
    **Ejemplo de uso:**
    ```
    GET /api/v1/trucks/empresa/1/warehouse/1/dates?date_from=2025-06-01&date_to=2025-06-30
    ```
    """
    try:
        logger.info(f"Obteniendo trucks por empresa {id_empresa}, warehouse {id_warehouse}, fechas {date_from} a {date_to}")
        result = crud_truck.get_by_empresa_warehouse_and_dates(db, id_empresa, id_warehouse, date_from, date_to)
        logger.info(f"Se encontraron {len(result)} trucks")
        return result
    except Exception as e:
        logger.error(f"Error al obtener trucks por empresa, warehouse y fechas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get(
    "/trucks/warehouse/{id_warehouse}/dates", 
    response_model=List[Truck],
    summary="Obtener camiones por almacén y fechas",
    description="Retorna camiones de un almacén específico dentro de un rango de fechas.",
    response_description="Lista de camiones encontrados",
    tags=["trucks"]
)
def read_trucks_by_warehouse_and_dates(
    id_warehouse: int = Path(..., description="ID del almacén", ge=1),
    date_from: date = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    date_to: date = Query(..., description="Fecha de fin (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Obtiene camiones de un almacén específico dentro de un rango de fechas.
    
    **Parámetros:**
    - `id_warehouse`: ID del almacén
    - `date_from`: Fecha de inicio del rango
    - `date_to`: Fecha de fin del rango
    
    **Ejemplo de uso:**
    ```
    GET /api/v1/trucks/warehouse/1/dates?date_from=2025-06-01&date_to=2025-06-30
    ```
    """
    try:
        logger.info(f"Obteniendo trucks por warehouse {id_warehouse}, fechas {date_from} a {date_to}")
        result = crud_truck.get_by_warehouse_and_dates(db, id_warehouse, date_from, date_to)
        logger.info(f"Se encontraron {len(result)} trucks")
        return result
    except Exception as e:
        logger.error(f"Error al obtener trucks por warehouse y fechas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get(
    "/trucks/carrier/{carrier}", 
    response_model=List[Truck],
    summary="Obtener camiones por transportista",
    description="Retorna todos los camiones de un transportista específico.",
    response_description="Lista de camiones encontrados",
    tags=["trucks"]
)
def read_trucks_by_carrier(
    carrier: str = Path(..., description="Nombre del transportista"),
    db: Session = Depends(get_db)
):
    """
    Obtiene todos los camiones de un transportista específico.
    
    **Parámetros:**
    - `carrier`: Nombre del transportista
    
    **Ejemplo de uso:**
    ```
    GET /api/v1/trucks/carrier/Transporte%20ABC
    ```
    """
    try:
        logger.info(f"Obteniendo trucks por carrier: {carrier}")
        result = crud_truck.get_by_carrier(db, carrier)
        logger.info(f"Se encontraron {len(result)} trucks")
        return result
    except Exception as e:
        logger.error(f"Error al obtener trucks por carrier: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get(
    "/trucks/load/{load_number}", 
    response_model=Truck,
    summary="Obtener camión por número de carga",
    description="Retorna los detalles de un camión específico por su número de carga.",
    response_description="Detalles del camión encontrado",
    tags=["trucks"]
)
def read_truck_by_load_number(
    load_number: str = Path(..., description="Número de carga del camión"),
    db: Session = Depends(get_db)
):
    """
    Obtiene los detalles de un camión específico por su número de carga.
    
    **Parámetros:**
    - `load_number`: Número de carga del camión
    
    **Respuestas:**
    - `200`: Camión encontrado exitosamente
    - `404`: Camión no encontrado
    
    **Ejemplo de uso:**
    ```
    GET /api/v1/trucks/load/LOAD-001
    ```
    """
    try:
        logger.info(f"Obteniendo truck por load_number: {load_number}")
        db_truck = crud_truck.get_by_load_number(db, load_number)
        if not db_truck:
            logger.warning(f"Truck con load_number {load_number} no encontrado")
            raise HTTPException(status_code=404, detail="Truck not found")
        logger.info(f"Truck encontrado: {db_truck}")
        return db_truck
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener truck por load_number: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}") 
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from app.db.databases import get_companies_db
from app.crud.crud_company import company
from app.schemas.company import Company, CompanyCreate, CompanyUpdate, CompanyList
from app.core.deps import get_current_user

router = APIRouter()

@router.get("/test")
def test_companies():
    """Endpoint de prueba simple"""
    return {"message": "Companies endpoint funcionando", "count": 0}

@router.get("/debug")
def debug_companies(
    db: Session = Depends(get_companies_db),
    current_user: dict = Depends(get_current_user)
):
    """Endpoint de debug para verificar el estado"""
    try:
        # Información del usuario actual
        user_info = {
            "username": current_user.get("username"),
            "user_data": current_user
        }
        
        # Contar empresas totales
        total_companies = db.query(Company).count()
        active_companies = db.query(Company).filter(Company.Estado_Cargue == 1).count()
        
        # Información de la base de datos
        db_info = {
            "total_companies": total_companies,
            "active_companies": active_companies
        }
        
        return {
            "status": "ok",
            "user": user_info,
            "database": db_info,
            "message": "Debug endpoint funcionando correctamente"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Error en debug endpoint"
        }

@router.get(
    "/",
    response_model=CompanyList,
    summary="Obtener lista de empresas",
    description="Retorna una lista paginada de empresas activas",
    tags=["Empresas"]
)
def get_companies(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    active_only: bool = Query(True, description="Solo empresas activas"),
    db: Session = Depends(get_companies_db)
):
    """
    Obtiene una lista paginada de empresas.
    
    - **skip**: Número de registros a omitir (para paginación)
    - **limit**: Número máximo de registros a retornar
    - **active_only**: Si es True, solo retorna empresas activas
    """
    try:
        companies = company.get_multi(db, skip=skip, limit=limit, active_only=active_only)
        total = company.count(db, active_only=active_only)
        return CompanyList(companies=companies, total=total)
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get(
    "/active",
    response_model=List[Company],
    summary="Obtener empresas activas permitidas para el usuario",
    description="Retorna todas las empresas activas a las que el usuario tiene permiso",
    tags=["Empresas"]
)
def get_active_companies(
    db: Session = Depends(get_companies_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene las empresas activas asignadas al usuario actual.
    Si el usuario no tiene empresas asignadas, retorna una lista vacía.
    """
    try:
        username = current_user["sub"]
        
        # SIMPLIFICADO: Verificar usuario directamente con SQL
        from app.db.databases import get_main_db
        
        main_db_gen = get_main_db()
        main_db = next(main_db_gen)
        
        try:
            # Consulta SQL directa para evitar problemas de mappers
            result = main_db.execute(
                text("SELECT id, username, is_superuser FROM OneSite.[user] WHERE username = :username AND is_active = 1"),
                {"username": username}
            ).fetchone()
            
            if not result:
                # Usuario no existe en OneSite - rechazar acceso
                print(f"⚠️  Usuario {username} no existe en OneSite - acceso denegado")
                raise HTTPException(
                    status_code=403,
                    detail="Usuario no registrado en OneSite. Contacte al administrador para obtener acceso."
                )
            
            user_id, db_username, is_superuser = result
            
            # Si es superuser, retornar todas las empresas
            if is_superuser:
                all_companies = company.get_multi(db, skip=0, limit=100, active_only=True)
                print(f"Usuario {username} (superuser) - {len(all_companies)} empresas disponibles")
                return all_companies
            
            # Para usuarios regulares, verificar permisos específicos
            permissions_result = main_db.execute(
                text("SELECT company_code FROM OneSite.user_company_permission WHERE user_id = :user_id AND is_active = 1"),
                {"user_id": user_id}
            ).fetchall()
            
            if not permissions_result:
                print(f"Usuario {username} sin permisos específicos de empresa")
                return []
            
            # Obtener códigos de empresa permitidos
            allowed_company_codes = [row[0] for row in permissions_result]
            
            # Filtrar empresas por códigos permitidos
            user_companies = company.get_companies_by_codes(db, allowed_company_codes)
            
            print(f"Usuario {username} (ID: {user_id}) tiene acceso a {len(user_companies)} empresas")
            if user_companies:
                company_names = [comp.Company or comp.BU for comp in user_companies]
                print(f"Empresas permitidas: {company_names[:5]}{'...' if len(company_names) > 5 else ''}")
            
            return user_companies
            
        finally:
            main_db.close()
        
    except HTTPException:
        # Re-lanzar HTTPExceptions sin modificar
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo empresas del usuario: {str(e)}")

@router.get(
    "/{company_id}",
    response_model=Company,
    summary="Obtener empresa por ID",
    description="Retorna una empresa específica por su ID",
    tags=["Empresas"]
)
def get_company(company_id: int, db: Session = Depends(get_companies_db)):
    """
    Obtiene una empresa específica por su ID.
    
    - **company_id**: ID único de la empresa
    """
    db_company = company.get(db, company_id=company_id)
    if not db_company:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return db_company

@router.post(
    "/",
    response_model=Company,
    summary="Crear nueva empresa",
    description="Crea una nueva empresa en el sistema",
    tags=["Empresas"]
)
def create_company(company_in: CompanyCreate, db: Session = Depends(get_companies_db)):
    """
    Crea una nueva empresa.
    
    - **name**: Nombre de la empresa (requerido)
    - **code**: Código único de la empresa (requerido)
    - **description**: Descripción opcional de la empresa
    - **is_active**: Estado activo de la empresa (por defecto True)
    """
    # Verificar si ya existe una empresa con el mismo código
    existing_company = company.get_by_code(db, code=company_in.code)
    if existing_company:
        raise HTTPException(
            status_code=400, 
            detail=f"Ya existe una empresa con el código '{company_in.code}'"
        )
    
    # Verificar si ya existe una empresa con el mismo ID de Oracle
    if company_in.code:
        existing_company_by_oracle = company.get_by_oracle_id(db, oracle_id=company_in.code)
        if existing_company_by_oracle:
            raise HTTPException(
                status_code=400, 
                detail=f"Ya existe una empresa con el ID de Oracle '{company_in.code}'"
            )
    
    return company.create(db, obj_in=company_in)

@router.put(
    "/{company_id}",
    response_model=Company,
    summary="Actualizar empresa",
    description="Actualiza una empresa existente",
    tags=["Empresas"]
)
def update_company(
    company_id: int, 
    company_in: CompanyUpdate, 
    db: Session = Depends(get_companies_db)
):
    """
    Actualiza una empresa existente.
    
    - **company_id**: ID de la empresa a actualizar
    - **company_in**: Datos de la empresa a actualizar
    """
    db_company = company.get(db, company_id=company_id)
    if not db_company:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    
    # Si se está actualizando el código, verificar que no exista otro
    if company_in.code and company_in.code != db_company.code:
        existing_company = company.get_by_code(db, code=company_in.code)
        if existing_company:
            raise HTTPException(
                status_code=400, 
                detail=f"Ya existe una empresa con el código '{company_in.code}'"
            )
    
    # Si se está actualizando el ID de Oracle, verificar que no exista otro
    if company_in.code and company_in.code != db_company.code:
        existing_company_by_oracle = company.get_by_oracle_id(db, oracle_id=company_in.code)
        if existing_company_by_oracle:
            raise HTTPException(
                status_code=400, 
                detail=f"Ya existe una empresa con el ID de Oracle '{company_in.code}'"
            )
    
    return company.update(db, db_obj=db_company, obj_in=company_in)

@router.delete(
    "/{company_id}",
    response_model=Company,
    summary="Eliminar empresa",
    description="Elimina una empresa (soft delete)",
    tags=["Empresas"]
)
def delete_company(company_id: int, db: Session = Depends(get_companies_db)):
    """
    Elimina una empresa (soft delete - la marca como inactiva).
    
    - **company_id**: ID de la empresa a eliminar
    """
    db_company = company.get(db, company_id=company_id)
    if not db_company:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    
    return company.delete(db, company_id=company_id) 
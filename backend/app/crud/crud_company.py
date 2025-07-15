from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate

class CRUDCompany:
    def get(self, db: Session, company_id: int) -> Optional[Company]:
        """Obtiene una empresa por su ID"""
        return db.query(Company).filter(Company.id_Company == company_id).first()
    
    def get_by_code(self, db: Session, code: str) -> Optional[Company]:
        """Obtiene una empresa por su código"""
        return db.query(Company).filter(Company.code == code).first()
    
    def get_by_name(self, db: Session, name: str) -> Optional[Company]:
        """Obtiene una empresa por su nombre (BU)"""
        return db.query(Company).filter(Company.BU == name).first()
    
    def get_by_oracle_id(self, db: Session, oracle_id: str) -> Optional[Company]:
        """Obtiene una empresa por su ID de Oracle"""
        return db.query(Company).filter(Company.id_Oracle == oracle_id).first()
    
    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        active_only: bool = True
    ) -> List[Company]:
        """Obtiene múltiples empresas con paginación"""
        query = db.query(Company)
        
        if active_only:
            query = query.filter(Company.Estado_Cargue == 1)
        
        query = query.order_by(Company.Company)
        return query.offset(skip).limit(limit).all()
    
    def create(self, db: Session, obj_in: CompanyCreate) -> Company:
        """Crea una nueva empresa"""
        from datetime import datetime
        
        db_obj = Company(
            name=obj_in.name,
            code=obj_in.code,
            description=obj_in.description,
            is_active=obj_in.is_active,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, 
        db: Session, 
        db_obj: Company, 
        obj_in: CompanyUpdate
    ) -> Company:
        """Actualiza una empresa existente"""
        from datetime import datetime
        
        update_data = obj_in.dict(exclude_unset=True)
        
        # Agregar timestamp de actualización
        update_data['updated_at'] = datetime.now()
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, company_id: int) -> Company:
        """Elimina una empresa (soft delete marcándola como inactiva)"""
        db_obj = db.query(Company).filter(Company.id_Company == company_id).first()
        if db_obj:
            db_obj.is_active = False
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        return db_obj
    
    def count(self, db: Session, active_only: bool = True) -> int:
        """Cuenta el total de empresas"""
        query = db.query(Company)
        
        if active_only:
            query = query.filter(Company.Estado_Cargue == 1)
        
        return query.count()

    def get_multi_by_ids(self, db: Session, ids: list, active_only: bool = True):
        query = db.query(Company).filter(Company.id_Company.in_(ids))
        if active_only:
            query = query.filter(Company.Estado_Cargue == 1)
        query = query.order_by(Company.Company)
        return query.all()
    
    def get_active_companies(self, db: Session) -> List[Company]:
        """Obtiene todas las empresas activas"""
        return db.query(Company).filter(Company.Estado_Cargue == 1).order_by(Company.Company).all()
    
    def get_companies_for_user(self, db: Session, user_id: int) -> List[Company]:
        """Obtiene las empresas asignadas a un usuario específico"""
        from app.models.user_company_permission import UserCompanyPermission
        
        # Hacer join entre Company y UserCompanyPermission para obtener solo las empresas del usuario
        return db.query(Company).join(
            UserCompanyPermission, 
            Company.id_Company == UserCompanyPermission.company_id
        ).filter(
            UserCompanyPermission.user_id == user_id,
            Company.Estado_Cargue == 1  # Solo empresas activas
        ).order_by(Company.Company).all()
    
    def get_companies_by_codes(self, db: Session, company_codes: List[str]) -> List[Company]:
        """Obtiene empresas por una lista de códigos (id_Oracle o id_Company)"""
        if not company_codes:
            return []
        
        # Separar códigos numéricos y alfanuméricos
        numeric_codes = [int(code) for code in company_codes if code.isdigit()]
        oracle_codes = [code for code in company_codes if not code.isdigit()]
        
        # Crear filtros
        filters = []
        if oracle_codes:
            filters.append(Company.id_Oracle.in_(oracle_codes))
        if numeric_codes:
            filters.append(Company.id_Company.in_(numeric_codes))
        
        if not filters:
            return []
        
        # Aplicar filtros con OR
        query = db.query(Company).filter(
            and_(
                or_(*filters),
                Company.Estado_Cargue == 1  # Solo empresas activas
            )
        )
        
        return query.order_by(Company.Company).all()

company = CRUDCompany() 
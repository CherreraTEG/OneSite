from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate

class CRUDCompany:
    def get(self, db: Session, company_id: int) -> Optional[Company]:
        """Obtiene una empresa por su ID"""
        return db.query(Company).filter(Company.id == company_id).first()
    
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
        db_obj = db.query(Company).filter(Company.id == company_id).first()
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

company = CRUDCompany() 
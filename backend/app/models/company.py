from sqlalchemy import Column, Integer, String, Float, DateTime
from app.db.base import Base

class Company(Base):
    __tablename__ = "Companies"
    __table_args__ = {"schema": "TheEliteGroup_Parameters"}
    
    # Mapeo a los campos reales de la tabla Companies
    id_Company = Column(Integer, primary_key=True, index=True)
    BU = Column(String(255), nullable=True, index=True)
    Country_Company = Column(String(255), nullable=True)
    Country_BU = Column(String(255), nullable=True)
    Currency = Column(String(10), nullable=True)
    Company_Type = Column(String(255), nullable=True)
    id_Oracle = Column(String(50), nullable=True, index=True)
    id_Elite = Column(Float, nullable=True)
    id_Traze = Column(String(50), nullable=True)
    Own_User = Column(String(255), nullable=True)
    Estado_Cargue = Column(Integer, nullable=True)
    Fecha_crea = Column(DateTime, nullable=True)
    
    # Propiedades para compatibilidad con el frontend
    @property
    def id(self):
        return self.id_Company
    
    @property
    def name(self):
        return self.BU or "Sin nombre"
    
    @property
    def code(self):
        return self.id_Oracle or str(self.id_Company)
    
    @property
    def is_active(self):
        return self.Estado_Cargue == 1 if self.Estado_Cargue is not None else True
    
    @property
    def created_at(self):
        return self.Fecha_crea
    
    @property
    def updated_at(self):
        return self.Fecha_crea 
from pydantic import BaseModel, Field, computed_field
from typing import Optional
from datetime import datetime

class CompanyBase(BaseModel):
    BU: Optional[str] = Field(None, description="Nombre de la unidad de negocio")
    Company: Optional[str] = Field(None, description="Nombre de la empresa")  
    Country_Company: Optional[str] = Field(None, description="País de la empresa")
    Currency: Optional[str] = Field(None, description="Moneda")
    id_Oracle: Optional[str] = Field(None, description="ID en Oracle")

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    BU: Optional[str] = Field(None, description="Nombre de la unidad de negocio")
    Company: Optional[str] = Field(None, description="Nombre de la empresa")
    Country_Company: Optional[str] = Field(None, description="País de la empresa")
    Currency: Optional[str] = Field(None, description="Moneda")

class Company(BaseModel):
    id_Company: int = Field(..., description="ID único de la empresa")
    BU: Optional[str] = Field(None, description="Nombre de la unidad de negocio")
    Company: Optional[str] = Field(None, description="Nombre de la empresa")
    Country_Company: Optional[str] = Field(None, description="País de la empresa")
    Currency: Optional[str] = Field(None, description="Moneda")
    id_Oracle: Optional[str] = Field(None, description="ID en Oracle")
    Estado_Cargue: Optional[int] = Field(None, description="Estado de carga")
    Fecha_crea: Optional[datetime] = Field(None, description="Fecha de creación")
    
    # Campos computados para compatibilidad con el frontend
    @computed_field
    @property
    def id(self) -> int:
        return self.id_Company
    
    @computed_field
    @property 
    def name(self) -> str:
        return self.BU or self.Company or "Sin nombre"
    
    @computed_field
    @property
    def code(self) -> str:
        return self.id_Oracle or str(self.id_Company)
    
    @computed_field
    @property
    def is_active(self) -> bool:
        return self.Estado_Cargue == 1 if self.Estado_Cargue is not None else True
    
    class Config:
        from_attributes = True

class CompanyList(BaseModel):
    companies: list[Company]
    total: int 
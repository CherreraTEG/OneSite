from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CompanyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Nombre de la empresa")
    code: str = Field(..., min_length=1, max_length=50, description="Código único de la empresa")
    description: Optional[str] = Field(None, max_length=500, description="Descripción de la empresa")
    is_active: bool = Field(True, description="Indica si la empresa está activa")

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Nombre de la empresa")
    code: Optional[str] = Field(None, min_length=1, max_length=50, description="Código único de la empresa")
    description: Optional[str] = Field(None, max_length=500, description="Descripción de la empresa")
    is_active: Optional[bool] = Field(None, description="Indica si la empresa está activa")

class CompanyInDB(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class Company(CompanyInDB):
    pass

class CompanyList(BaseModel):
    companies: list[Company]
    total: int 
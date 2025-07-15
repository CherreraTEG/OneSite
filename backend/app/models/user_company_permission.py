from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class UserCompanyPermission(Base):
    __tablename__ = "user_company_permission"
    __table_args__ = {"schema": "OneSite"}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("OneSite.user.id"), nullable=False)
    company_code = Column(String(50), nullable=False)  # Referencia a Companies.id_Oracle o id_Company
    permission_type = Column(String(50), default='read', nullable=False)  # read, write, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.getutcdate())
    updated_at = Column(DateTime, server_default=func.getutcdate(), onupdate=func.getutcdate())
    created_by = Column(String(50), nullable=True) 
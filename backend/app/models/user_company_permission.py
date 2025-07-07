from sqlalchemy import Column, Integer, ForeignKey
from app.db.base import Base

class UserCompanyPermission(Base):
    __tablename__ = "user_company_permission"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("Companies.id_Company"), nullable=False) 
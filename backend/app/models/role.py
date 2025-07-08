from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(200))
    
    # Relationships (usando lazy import para evitar dependencias circulares)
    users = relationship("app.models.user.User", secondary="user_role", back_populates="roles", lazy="dynamic") 
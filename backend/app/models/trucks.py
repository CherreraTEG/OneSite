from sqlalchemy import Column, Integer, String, Date, Time, Text, Float, DateTime, BigInteger
from app.db.base import Base

class Truck(Base):
    __tablename__ = 'trucks_control'
    __table_args__ = {'schema': 'trucks'}

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    id_empresa = Column(Integer, index=True)
    id_warehouse = Column(Integer, index=True)
    ship_date = Column(Date, index=True)
    deliv_date = Column(Date, index=True)
    carrier = Column(String(200), index=True)
    customer_facility = Column(String(200))
    po = Column(String(200), index=True)
    qty = Column(Float)
    estatus = Column(Integer, index=True)
    time_in = Column(Time(7))
    door = Column(String(25))
    time_out = Column(Time(7))
    comments = Column(String(1000))
    pickup_location = Column(String(150))
    load_number = Column(String(50), index=True)
    id_customer = Column(Integer, index=True)
    estado_cargue = Column(Integer)
    update_date = Column(DateTime, index=True)
    update_user = Column(String(50))
    file_name = Column(String(100)) 
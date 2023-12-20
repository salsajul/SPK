from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Laptop(Base):
    __tablename__ = 'laptop'
    id = Column(Integer, primary_key=True)
    Nama_Produk  = Column(String(50))
    Harga_C1  = Column(String(50)) 
    Prosesor_C2  = Column(String(50))
    RAM_C3  = Column(String(50))
    Storage_C4  = Column(String(50))
    Baterai_C5  = Column(String(50))

    def __repr__(self):
        return f"laptop(id={self.id!r}, nama={self.nama!r}"

from sqlalchemy import Column, Integer, String, Text, Enum, Numeric
from config.database import Base
import enum

class CategoriaEnum(str, enum.Enum):
    Platos = "Platos"
    Bebidas = "Bebidas"
    Extras = "Extras"
    
class Producto(Base):
    __tablename__ = "productos"

    id_producto = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50))
    descripcion = Column(Text)
    precio_venta = Column(Numeric(10, 2))
    categoria = Column(Enum(CategoriaEnum))
    imagen = Column(String(255))


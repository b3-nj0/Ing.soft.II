from pydantic import BaseModel
from enum import Enum

class CategoriaEnum(str, Enum):
    Platos = "Platos"
    Bebidas = "Bebidas"
    Extras = "Extras"

class ProductoBase(BaseModel):
    nombre: str
    descripcion: str
    precio_venta: float
    categoria: CategoriaEnum
    imagen: str



class ProductoOut(ProductoBase):
    id_producto: int

    class Config:
        from_attributes = True

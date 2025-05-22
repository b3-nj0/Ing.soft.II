from pydantic import BaseModel

class productoInput(BaseModel):

    nombre: str
    descripcion: str
    precio_venta: float
    categoria: str
    imagen: str


class productoupdate(BaseModel):

    id_producto: int
    nombre: str
    descripcion: str
    precio_venta: float
    categoria: str
    imagen: str



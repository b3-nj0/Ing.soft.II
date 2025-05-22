from pydantic import BaseModel

class usuariosInput(BaseModel):

    nombre: str
    telefono: str
    direccion: str
    fecha_registro: str
    usuario: float
    contrasena: float


class usuariosupdate(BaseModel):

    id_usuario: int
    nombre: str
    telefono: str
    direccion: str
    fecha_registro: str
    usuario: float
    contrasena: float




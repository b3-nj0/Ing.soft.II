from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class VentaDiaResponse(BaseModel):
    id_producto: int
    nombre: str
    cantidad: int
    total: float
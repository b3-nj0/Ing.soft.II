from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, Form
from sqlalchemy.orm import Session
from config.settings_env import settings_objeto
from service.service_producto import guardar_imagen, obtener_productos, crear_producto, obtener_producto_por_id,actualizar_producto ,eliminar_producto
from config.database import get_db
from schemas.schema_producto import ProductoOut, ProductoBase


producto_route = APIRouter()




@producto_route.get("/productos")
def obtener_producto(db: Session = Depends(get_db)):
    return obtener_productos(db)

@producto_route.post("/crear_producto", response_model=ProductoOut)
def crear_productos(data_producto: ProductoBase, db: Session = Depends(get_db)):
    return crear_producto(data_producto, db)


@producto_route.get("/obtener_producto_por_id/{producto_id}")
def obtener_productos_id(producto_id: int ,db: Session = Depends(get_db)):
    return obtener_producto_por_id(producto_id,db)


@producto_route.put("/actualizar_producto/{producto_id}")
def actualizar_productos(producto_id: int ,data_producto :ProductoBase,db: Session = Depends(get_db)):
    return actualizar_producto(producto_id,data_producto, db)

@producto_route.delete("/eliminar_producto/{producto_id}")
def eliminar_productos(producto_id: int ,db: Session = Depends(get_db)):
    return eliminar_producto(producto_id ,db)

@producto_route.post("/crear_producto_form", response_model=ProductoOut)
def crear_producto_form(
    nombre: str = Form(...),
    descripcion: str = Form(...),
    precio_venta: float = Form(...),
    categoria: str = Form(...),
    imagen: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    ruta_base = settings_objeto.ASSET_URL
    ruta_imagen = guardar_imagen(imagen, ruta_base)
    data_producto = ProductoBase(
        nombre=nombre,
        descripcion=descripcion,
        precio_venta=precio_venta,
        categoria=categoria,
        imagen=ruta_imagen
    )
    return crear_producto(data_producto, db)



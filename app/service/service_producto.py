from fastapi import Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
import os
import shutil
from config.database import get_db
from config.settings_env import settings_objeto
from models.model_producto import Producto
from schemas.schema_producto import ProductoBase  # supuestos schemas para crear y actualizar

# Crear un producto
def crear_producto(producto: ProductoBase, db: Session):
    ruta_base = settings_objeto.ASSET_URL
    nombre_imagen = producto.imagen
    if not nombre_imagen.startswith(ruta_base):
        nombre_imagen = ruta_base + nombre_imagen
    nuevo_producto = Producto(
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio_venta=producto.precio_venta,
        categoria=producto.categoria,
        imagen=producto.imagen
    )
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto
def guardar_imagen(imagen: UploadFile, ruta_base: str) -> str:
    # Validar extensión
    ext_permitidas = {".jpg", ".jpeg", ".png", ".gif"}
    nombre = os.path.basename(imagen.filename)
    _, ext = os.path.splitext(nombre)
    if ext.lower() not in ext_permitidas:
        raise HTTPException(status_code=400, detail="Formato de imagen no permitido")

    # Sanitizar nombre (evita path traversal)
    nombre = nombre.replace("..", "").replace("/", "").replace("\\", "")

    ruta_destino = os.path.join(ruta_base, nombre)
    with open(ruta_destino, "wb") as buffer:
        shutil.copyfileobj(imagen.file, buffer)
    return ruta_destino

# Obtener todos los productos
def obtener_productos(db: Session = Depends(get_db)):
    return db.query(Producto).all()

# Obtener un producto por id
def obtener_producto_por_id(producto_id: int ,db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id_producto == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

# Actualizar un producto
def actualizar_producto( producto_id: int, producto_actualizado: ProductoBase ,db: Session):
    producto = obtener_producto_por_id(producto_id, db)
    producto.nombre = producto_actualizado.nombre
    producto.descripcion = producto_actualizado.descripcion
    producto.precio_venta = producto_actualizado.precio_venta
    producto.categoria = producto_actualizado.categoria
    db.commit()
    db.refresh(producto)
    return producto

# Eliminar un producto
def eliminar_producto(producto_id: int,db: Session = Depends(get_db)):
    producto = obtener_producto_por_id(producto_id,db)
    db.delete(producto)
    db.commit()
    return {"detail": "Producto eliminado correctamente"}

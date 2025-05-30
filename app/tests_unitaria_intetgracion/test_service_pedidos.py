import pytest
from unittest.mock import MagicMock, patch
from datetime import date, datetime, timedelta
from back.app.config.database import Base
from back.app.config.database import get_db
# Imports de la app (asegúrate de que solo hay una copia de los modelos en tu proyecto)
from back.app.service.service_pedidos import ventas_semana
from back.app.models.model_pedidos import Pedido, EstadoPedido
from back.app.models.model_detalles_pedidos import DetallePedido
from back.app.config.settings_env import settings_objeto



# ---------- PRUEBA UNITARIA COMPLEJA ----------
def test_ventas_semana_unitaria():
    hoy = date(2024, 5, 29) 
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    dias_ventas = [
        inicio_semana,                  
        inicio_semana + timedelta(days=2), 
        inicio_semana + timedelta(days=4) 
    ]
    resultados_mock = [
        MagicMock(dia=dias_ventas[0], cantidad_ventas=3),
        MagicMock(dia=dias_ventas[1], cantidad_ventas=5),
        MagicMock(dia=dias_ventas[2], cantidad_ventas=2),
    ]
    db_mock = MagicMock()
    db_mock.query.return_value.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = resultados_mock

    with patch("locale.setlocale"):
        with patch("back.app.service.service_pedidos.date") as date_patch:
            date_patch.today.return_value = hoy
            salida = ventas_semana(db_mock)

    # Compara en minúsculas para evitar problemas de locale
    labels = [l.lower() for l in salida["labels"]]
    assert labels in (
        ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"],
        ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"],
    )
    assert salida["data"] == [3, 0, 5, 0, 2, 0, 0]

# ---------- PRUEBA INTEGRACIÓN ----------
@pytest.mark.integration_test
def test_ventas_semana_integracion():


    db = next(get_db())

    # Limpiar tablas
    db.query(DetallePedido).delete()
    db.query(Pedido).delete()
    db.commit()

    hoy = date(2024, 5, 29)
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    dias = [inicio_semana + timedelta(days=i) for i in range(7)]
    
    # Crear datos de prueba
    db.add_all([
        Pedido(fecha_hora=datetime.combine(dias[0], datetime.min.time()), estado=EstadoPedido.Terminado, total=10),
        Pedido(fecha_hora=datetime.combine(dias[0], datetime.min.time()), estado=EstadoPedido.Terminado, total=20),
        Pedido(fecha_hora=datetime.combine(dias[0], datetime.min.time()), estado=EstadoPedido.Pendiente, total=30),
    ])
    db.add(Pedido(fecha_hora=datetime.combine(dias[2], datetime.min.time()), estado=EstadoPedido.Terminado, total=40))
    db.add_all([
        Pedido(fecha_hora=datetime.combine(dias[4], datetime.min.time()), estado=EstadoPedido.Terminado, total=50),
        Pedido(fecha_hora=datetime.combine(dias[4], datetime.min.time()), estado=EstadoPedido.Terminado, total=60),
        Pedido(fecha_hora=datetime.combine(dias[4], datetime.min.time()), estado=EstadoPedido.Terminado, total=70),
    ])
    db.commit()

    with patch("locale.setlocale"):
        with patch("back.app.service.service_pedidos.date") as date_patch:
            date_patch.today.return_value = hoy
            salida = ventas_semana(db)

    labels = [l.lower() for l in salida["labels"]]
    assert labels in (
        ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"],
        ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"],
    )
    assert salida["data"] == [2, 0, 1, 0, 3, 0, 0]
    
    db.close()




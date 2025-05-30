from fastapi import FastAPI

from config.conn_front import setup_cors
from config.settings_env import settings_objeto
from starlette.middleware.sessions import SessionMiddleware

from routes.detalle_pedidos_routes import detalle_pedido_route
from routes.pedidos_routes import pedidos_route
from routes.producto_routes import producto_route   
# from routes.ticket_diario_routes import ticket_diario_route
from routes.ticket_route import ticket_routes
from routes.usuario_routes import usuario


main = FastAPI()

main.add_middleware(SessionMiddleware, secret_key=settings_objeto.SECRET_KEY)

setup_cors(main)


main.include_router(usuario)
main.include_router(detalle_pedido_route)
main.include_router(pedidos_route)
main.include_router(producto_route)
# main.include_router(ticket_diario_route)
main.include_router(ticket_routes)

# Dependency para obtener la DB session



# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session


# from schemas.schema_ticket import TicketOut
# from config.database import get_db

# # from service.service_ticket import generar_ticket_impresion





# ticket_diario_route = APIRouter()



# @ticket_diario_route.get('/imprimir_ticket', response_model = TicketOut ,tags=['Ticket_Diario'])
# def mostrar_tickets( db: Session = Depends(get_db)):
#     return generar_ticket_impresion(TicketOut,db)
    


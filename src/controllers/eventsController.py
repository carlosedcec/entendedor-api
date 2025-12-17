from flask_openapi3 import Tag
from model import Event
from functions import CRUDFunctions, ValidationHelper
from schema import *
from controllers.authController import *

def register_events_routes(app):

    event_tag = Tag(name="Eventos", description="Adição, visualização, edição e remoção de eventos")

    @app.get("/get-events", tags=[event_tag],
            responses={ "200": Event_ListReturnSchema, "400": ErrorSchema })
    @auth_required
    def get_events(user_id: int):
        """Pesquisa por todos os eventos cadastrados
        Retorna uma listagem dos eventos
        """

        def get_function(session, params):

            events = session.query(Event).filter(Event.user_id == params["user_id"]).order_by(Event.date.desc(), Event.time.desc()).all()

            data = []
            for event in events:
                data.append({
                    "id": event.id,
                    "description": event.description,
                    "date": event.date,
                    "time": event.time
                })
        
            return data
        
        params = { "user_id": user_id }

        crud = CRUDFunctions()
        return crud.get_data(get_function, params, "eventos")

    @app.post("/add-event", tags=[event_tag],
            responses={ "200": Event_AddReturnSchema, "400": ErrorSchema })
    @auth_required
    def add_event(body: Event_AddFormSchema, user_id: int):
        """Adiciona um novo evento ao banco de dados
        Retorna o objeto inserído e uma mensagem de confirmação ou uma menasgem de erro
        """

        def insert_function(body, session, params):

            if not ValidationHelper.is_valid_date(body.date):
                return { "error": "O campo \"Data\" está inválido" }, 422

            if not ValidationHelper.is_valid_time(body.time):
                return { "error": "O campo \"Hora\" está inválido" }, 422

            return Event(
                description=body.description,
                date=body.date,
                time=body.time,
                user_id=params["user_id"]
            )

        params = { "user_id": user_id }

        crud = CRUDFunctions()
        return crud.add_data(body, insert_function, params, "evento")

    @app.put("/update-event/<int:event_id>", tags=[event_tag],
            responses={ "200": Event_UpdateReturnSchema, "400": ErrorSchema })
    @auth_required
    def update_event(path: Event_IdSchema, body: Event_UpdateFormSchema, user_id: int):
        """Atualiza o evento informado
        Retorna o objeto atualizado e uma mensagem de confirmação ou uma menasgem de erro
        """

        def update_function(body, session, params):

            if not ValidationHelper.is_valid_date(body.date):
                return { "error": "O campo \"Data\" está inválido" }, 422

            if not ValidationHelper.is_valid_time(body.time):
                return { "error": "O campo \"Hora\" está inválido" }, 422

            event = session.query(Event).filter(
                Event.id == params["item_id"],
                Event.user_id == params["user_id"]
                ).first()
            if not event:
                return { "error": "Evento não encontrado no banco de dados" }, 404

            event.description = str(body.description)
            event.date = str(body.date)
            event.time = str(body.time)

            return event

        params = {
            "user_id": user_id,
            "item_id": path.event_id
        }

        crud = CRUDFunctions()
        return crud.update_data(body, update_function, params, "evento")

    @app.delete("/delete-event/<int:event_id>", tags=[event_tag],
            responses={ "200": Event_DeleteReturnSchema, "400": ErrorSchema })
    @auth_required
    def delete_event(path: Event_IdSchema, user_id: int):
        """Deleta o evento informado do banco de dados
        Retorna uma mensagem de confirmação ou erro
        """
        crud = CRUDFunctions()
        params = { "user_id": user_id, "item_id": path.event_id }
        return crud.delete_data(Event, Event.id, params, "evento")
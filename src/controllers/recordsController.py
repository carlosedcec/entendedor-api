from sqlalchemy import func
from flask_openapi3 import Tag
from model import Record, Symptom
from functions import CRUDFunctions, ValidationHelper
from schema import *
from controllers.authController import *

def register_records_routes(app):

    record_tag = Tag(name="Registros", description="Adição, visualização, edição e remoção de registros")

    @app.get("/get-records", tags=[record_tag],
            responses={ "200": Record_ListCompleteReturnSchema, "400": ErrorSchema })
    @auth_required
    def get_records(user_id: int):
        """Pesquisa por todos os registros cadastrados
        Retorna uma listagem dos registros
        """

        def get_function(session, params):
            # Seleciona os dados agrupando registros que são iguais na mesma data e calculando a média destes
            daily_records = session.query(
                Record.id,
                Record.date,
                Record.time,
                Record.symptom_id,
                Symptom.name.label('symptom_name'),
                func.sum(Record.value).label('total_value'),
                func.avg(Record.value).label('average_value')
            ).join(
                Symptom,
                Record.symptom_id == Symptom.id
            ).filter(
                Record.user_id == params["user_id"]
            ).group_by(
                Record.date,
                Record.symptom_id
            ).all()
            
            data = []
            for record in daily_records:
                data.append({
                    "id": record.id,
                    "date": record.date,
                    "time": record.time,
                    "symptom_id": record.symptom_id,
                    "symptom_name": record.symptom_name,
                    "total_value": record.total_value,
                    "average_value": round(record.average_value, 2) if record.average_value else 0
                })

            return data

        params = { "user_id": user_id }

        crud = CRUDFunctions()
        return crud.get_data(get_function, params, "registros")

    @app.get("/get-records-by-symptom/<int:symptom_id>", tags=[record_tag],
            responses={ "200": Record_ListBasicReturnSchema, "400": ErrorSchema })
    @auth_required
    def get_records_by_symptom(path: Symptom_IdSchema, user_id: int):
        """Pesquisa pelos registros referentes ao sintoma informado como parâmetro
        Retorna uma listagem dos registros encontrados
        """

        def get_function(session, params):
            # Busca os registros filtrando por sintoma
            records = session.query(
                Record,
                Symptom.name.label('symptom_name')
            ).join(
                Symptom, 
                Record.symptom_id == Symptom.id
            ).filter(
                Record.user_id == params["user_id"],
                Record.symptom_id == params["symptom_id"]
            ).order_by(Record.date.desc(), Record.time.desc()).all()
            
            data = []
            for record, symptom_name in records:
                data.append({
                    "id": record.id,
                    "date": record.date,
                    "time": record.time,
                    "symptom_id": record.symptom_id,
                    "symptom_name": symptom_name,
                    "value": record.value
                })
            
            return data

        params = {
            "user_id": user_id,
            "symptom_id": path.symptom_id
        }

        crud = CRUDFunctions()
        return crud.get_data(get_function, params, "registros")    

    @app.post("/add-record", tags=[record_tag],
            responses={ "200": Record_AddReturnSchema, "400": ErrorSchema })
    @auth_required
    def add_record(body: Record_AddFormSchema, user_id: int):
        """Adiciona um novo registro ao banco de dados
        Retorna o objeto inserído e uma mensagem de confirmação ou uma menasgem de erro
        """

        def insert_function(body, session, params):

            if not ValidationHelper.is_valid_date(body.date):
                return { "error": "O campo \"Data\" está inválido" }, 422

            if not ValidationHelper.is_valid_time(body.time):
                return { "error": "O campo \"Hora\" está inválido" }, 422

            symptom = session.query(Symptom).filter(
                Symptom.id == int(body.symptom_id),
                Symptom.user_id == params["user_id"]
            ).first()

            if not symptom:
                return { "error": "Sintoma não encontrado no banco de dados" }, 404

            return Record(
                symptom_id=symptom.id,
                date=body.date,
                time=body.time,
                value=body.value,
                user_id=params["user_id"]
            )

        params = { "user_id": user_id }

        crud = CRUDFunctions()
        return crud.add_data(body, insert_function, params, "registro")

    @app.post("/add-batch-records", tags=[record_tag],
            responses={ "200": Record_AddBatchReturnSchema, "400": ErrorSchema })
    @auth_required
    def add_batch_records(body: Record_AddBatchFormSchema, user_id: int):
        """Adiciona registros em lote no banco de dados
        Retorna a lista de objetos inserídos e uma mensagem de confirmação ou uma mensagem de erro
        """

        def insert_function(body, session, params):

            if not ValidationHelper.is_valid_date(body.date):
                return { "error": "O campo \"Data\" está inválido" }, 422

            if not ValidationHelper.is_valid_time(body.time):
                return { "error": "O campo \"Hora\" está inválido" }, 422

            if not body.batch_records or len(body.batch_records) == 0:
                return { "error": "Formato de dados inválido" }, 422

            records = []

            for record in body.batch_records:
                records.append(Record(
                    symptom_id=record.symptom_id,
                    date=body.date,
                    time=body.time,
                    value=record.value,
                    user_id=params["user_id"]
                ))
            
            return records

        params = { "user_id": user_id }

        crud = CRUDFunctions()
        return crud.add_data(body, insert_function, params, "registro")

    @app.put("/update-record/<int:record_id>", tags=[record_tag],
            responses={ "200": Record_UpdateReturnSchema, "400": ErrorSchema })
    @auth_required
    def update_record(path: Record_IdSchema, body: Record_UpdateFormSchema, user_id: int):
        """Atualiza o registro informado
        Retorna o objeto atualizado e uma mensagem de confirmação ou uma menasgem de erro
        """

        def update_function(body, session, url_parameter):

            if not ValidationHelper.is_valid_date(body.date):
                return { "error": "O campo \"Data\" está inválido" }, 422

            if not ValidationHelper.is_valid_time(body.time):
                return { "error": "O campo \"Hora\" está inválido" }, 422

            record = session.query(Record).filter(
                Record.id == params["item_id"],
                Record.user_id == params["user_id"]
            ).first()

            if not record:
                return { "error": "Registro não encontrado no banco de dados" }, 404

            record.date = str(body.date)
            record.time = str(body.time)
            record.value = str(body.value)

            return record

        params = {
            "user_id": user_id,
            "item_id": path.record_id
        }

        crud = CRUDFunctions()
        return crud.update_data(body, update_function, params, "registro")

    @app.delete("/delete-record/<int:record_id>", tags=[record_tag],
            responses={ "200": Record_DeleteReturnSchema, "400": ErrorSchema })
    @auth_required
    def delete_record(path: Record_IdSchema, user_id: int):
        """Deleta o registro informado do banco de dados
        Retorna uma mensagem de confirmação ou um erro
        """
        crud = CRUDFunctions()
        params = { "user_id": user_id, "item_id": path.record_id }
        return crud.delete_data(Record, Record.id, params, "registro")

    @app.delete("/delete-records-date/<string:records_date>", tags=[record_tag],
            responses={ "200": Record_DeleteReturnSchema, "400": ErrorSchema })
    @auth_required
    def delete_records_date(path: Record_DateIdSchema, user_id: int):
        """Deleta todos os registro referentes a data passada como parâmetro
        Retorna uma mensagem de confirmação ou um erro
        """
        crud = CRUDFunctions()
        params = { "user_id": user_id, "item_id": path.records_date }
        return crud.delete_data(Record, Record.date, params, "dia")

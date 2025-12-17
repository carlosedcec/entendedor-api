from flask_openapi3 import Tag
from model import Symptom, Record, Session
from functions import CRUDFunctions
from schema import *
from controllers.authController import *

def register_symptoms_routes(app):

    symptom_tag = Tag(name="Sintomas", description="Adição, visualização, edição e remoção de sintoma")

    @app.get("/get-symptoms", tags=[symptom_tag],
            responses={ "200": Symptom_ListReturnSchema, "400": ErrorSchema })
    @auth_required
    def get_symptoms(user_id: int):
        """Pesquisa por todos os sintoma cadastrados
        Retorna uma listagem dos sintoma
        """

        def get_function(session, params):

            symptoms = session.query(Symptom).filter(Symptom.user_id == params["user_id"]).order_by(Symptom.order.asc()).all()

            data = []
            for symptom in symptoms:
                data.append({
                    "id": symptom.id,
                    "name": symptom.name,
                    "order": symptom.order
                })

            return data
        
        params = { "user_id": user_id }

        crud = CRUDFunctions()
        return crud.get_data(get_function, params, "sintomas")

    @app.post("/add-symptom", tags=[symptom_tag],
            responses={ "200": Symptom_AddReturnSchema, "400": ErrorSchema })
    @auth_required
    def add_symptom(body: Symptom_AddFormSchema, user_id: int):
        """Adiciona um novo sintoma ao banco de dados
        Retorna o objeto inserído e uma mensagem de confirmação ou uma menasgem de erro
        """

        def insert_function(body, session, params):

            symptoms = session.query(Symptom).filter(Symptom.user_id == params["user_id"]).order_by(Symptom.order.asc()).all()

            for symptom in symptoms:
                if (symptom.name == str(body.name).lower()):
                    return { "error": "Sintoma já existente no banco de dados" }, 404

            new_maximum_order = 1
            symptom_with_maximum_order = session.query(Symptom).order_by(Symptom.order.desc()).first()
            if symptom_with_maximum_order and symptom_with_maximum_order.order > 0:
                new_maximum_order = (symptom_with_maximum_order.order + 1)

            return Symptom(
                name=str(body.name).lower(),
                order=new_maximum_order,
                user_id=params["user_id"]
            )

        params = { "user_id": user_id }

        crud = CRUDFunctions()
        return crud.add_data(body, insert_function, params, "sintoma")

    @app.put("/update-symptom/<int:symptom_id>", tags=[symptom_tag],
            responses={ "200": Symptom_UpdateReturnSchema, "400": ErrorSchema })
    @auth_required
    def update_symptom(path: Symptom_IdSchema, body: Symptom_UpdateFormSchema, user_id: int):
        """Atualiza o sintoma informado
        Retorna o objeto atualizado e uma mensagem de confirmação ou uma menasgem de erro
        """

        def update_function(body, session, params):

            symptom = session.query(Symptom).filter(
                Symptom.id == params["item_id"],
                Symptom.user_id == params["user_id"]
            ).first()

            if not symptom:
                return { "error": "Sintoma não encontrado no banco de dados" }, 404

            symptom.name = str(body.name).lower()

            return symptom

        params = {
            "user_id": user_id,
            "item_id": path.symptom_id
        }

        crud = CRUDFunctions()
        return crud.update_data(body, update_function, params, "sintoma")

    @app.put("/update-symptom-order", tags=[symptom_tag],
            responses={ "200": Symptom_UpdateOrderReturnSchema, "400": ErrorSchema })
    @auth_required
    def update_symptom_order(body: Symptom_UpdateOrderFormSchema, user_id: int):
        """Atualiza a ordenação dos sintoma no banco de dados
        Retorna uma mensagem de confirmação ou erro
        """

        def update_function(body, session, params):

            if not body.symptoms_order or len(body.symptoms_order) == 0:
                return { "error": "Formato de dados inválido" }, 422

            symptoms_return = []

            for item in body.symptoms_order:
                symptom = session.query(Symptom).filter(
                    Symptom.id == item.id,
                    Symptom.user_id == params["user_id"]
                ).first()
                if not symptom:
                    return { "error": "Sintoma não encontrado no banco de dados" }, 404
                symptom.order = int(item.order)
                symptoms_return.append(symptom)

            return symptoms_return

        params = { "user_id": user_id }

        crud = CRUDFunctions()
        return crud.update_data(body, update_function, params, "sintomas")

    @app.delete("/delete-symptom/<int:symptom_id>", tags=[symptom_tag],
            responses={ "200": Symptom_DeleteReturnSchema, "400": ErrorSchema })
    @auth_required
    def delete_symptom(path: Symptom_IdSchema, user_id: int):
        """Deleta o sintoma informado do banco de dados
        Retorna uma mensagem de confirmação ou erro
        """

        session = Session()

        record = session.query(Record).filter(
            Record.symptom_id == path.symptom_id,
            Record.user_id == user_id
        ).first()

        if record and record.id > 0:
            return { "error": "Não é possível excluir este sintoma pois ele está sendo utilizado por registros" }, 409


        params = { "user_id": user_id, "item_id": path.symptom_id }

        crud = CRUDFunctions()
        return crud.delete_data(Symptom, Symptom.id, params, "sintoma")
import os
from flask_openapi3 import Tag
from model import Session, User
from functions import AuthHelper, CRUDFunctions, ValidationHelper
from datetime import datetime
from schema import *
from controllers.authController import auth_required

def register_users_routes(app):

    user_tag = Tag(name="Usuário", description="Adição, visualização e edição de usuário")

    @app.get("/get-user", tags=[user_tag],
            responses={ "200": User_ViewSchema, "400": ErrorSchema })
    @auth_required
    def get_user(user_id: int):
        """Retorna os dados do usuário logado
        """

        def get_function(session, params):

            user = session.query(User).filter(User.id == params["user_id"]).first()

            if not user or not user.id:
                return { "error": "Usuário não encontrado no banco de dados" }, 400

            return {
                "username": user.username,
                "email": user.email,
                "cep": user.cep,
                "city": user.city,
                "state": user.state
            }
        
        params = { "user_id": user_id }

        crud = CRUDFunctions()
        return crud.get_data(get_function, params, "usuário")

    @app.post("/add-user", tags=[user_tag],
            responses={ "200": User_AddReturnSchema, "400": ErrorSchema })
    def add_user(body: User_AddFormSchema):
        """Adiciona um novo usuário no banco de dados
        Retorna o objeto inserído e uma mensagem de confirmação ou uma menasgem de erro
        """

        def insert_function(body, session, params):

            if not ValidationHelper.is_valid_email(body.email):
                return { "error": "O campo \"E-mail\" está inválido" }, 422

            user = session.query(User).filter(User.email == body.email).first()

            if user and user.id > 0:
                return { "error": "E-mail já cadastrado em nosso banco de dados" }, 409

            password = body.password

            if len(password) < 8:
                return { "error": "A senha deve conter no mínimo 8 caracteres" }, 400

            password_salt = os.urandom(4).hex()
            password_hash = AuthHelper.hash_password(password + password_salt)

            current_time = datetime.now().strftime("%d/%m/%Y %H:%M")

            return User(
                username=body.username,
                email=body.email,
                cep=body.cep,
                city=body.city,
                state=body.state,
                salt=password_salt,
                password=password_hash,
                created_at=current_time
            )

        crud = CRUDFunctions()
        return crud.add_data(body, insert_function, {}, "usuário")

    @app.put("/update-user", tags=[user_tag],
            responses={ "200": User_UpdateReturnSchema, "400": ErrorSchema })
    @auth_required
    def update_user(body: User_UpdateFormSchema, user_id: int):
        """Atualiza o usuário informado
        Retorna o objeto atualizado e uma mensagem de confirmação ou uma menasgem de erro
        """

        def update_function(body, session, params):

            user = session.query(User).filter(User.id == params["user_id"]).first()

            if not user:
                return { "error": "Usuário não encontrado no banco de dados" }, 404

            if not ValidationHelper.is_valid_email(body.email):
                return { "error": "O campo \"E-mail\" está inválido" }, 422

            password = body.password
            password_hash = user.password

            if password:
                if len(password) < 8:
                    return { "error": "A senha deve conter no mínimo 8 caracteres" }, 400
                password_hash = AuthHelper.hash_password(password + user.salt)

            user.username = str(body.username)
            user.email = str(body.email)
            user.cep = str(body.cep)
            user.city = str(body.city)
            user.state = str(body.state)
            user.password = str(password_hash)

            return user

        params = {
            "user_id": user_id
        }

        crud = CRUDFunctions()
        return crud.update_data(body, update_function, params, "usuário")
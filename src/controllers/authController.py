import os
from flask_openapi3 import Tag
from model import Session, User
from functools import wraps
from flask import request, make_response
from functions import AuthHelper
from schema import *

AUTH_COOKIE_NAME = "access_token"

def register_auth_routes(app):

    auth_tag = Tag(name="Autenticação", description="Rotas de login e autenticação")

    @app.post("/login", tags=[auth_tag],
            responses={ "200": Auth_LoginSchema, "401": ErrorSchema })
    def login(body: User_LoginSchema):
        
        try:

            session = Session()

            user = session.query(User).filter((User.username == body.username) | (User.email == body.username)).first()
            if not user:
                return { "error": "Credenciais de login inválidas" }, 401

            password_with_salt = body.password + user.salt

            if not AuthHelper.verify_password(password_with_salt, user.password):
                return { "error": "Credenciais de login inválidas" }, 401

            token = AuthHelper.generate_token(user.id)

            response = make_response({ "message": "Login realizado com sucesso" }, 200)

            response.set_cookie(
                AUTH_COOKIE_NAME,
                token,
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=7200,
                path="/",
            )

            return response

        except Exception as e:
            print(str(e))
            return { "message": "Não foi possível fazer login" }, 400
        finally:
            session.close()

    @app.post("/logout", tags=[auth_tag],
            responses={ "200": Auth_LogoutSchema, "401": ErrorSchema })
    def logout():
        response = make_response({ "message": "Logout realizado com sucesso" }, 200)
        response.delete_cookie(AUTH_COOKIE_NAME)
        return response

    @app.get("/auth/status", tags=[auth_tag],
            responses={ "200": Auth_CheckStatusSchema, "401": ErrorSchema })
    def check_auth_status():

        auth_check = check_token()

        if auth_check["invalid"]:
            return { "error": auth_check["message"] }, 401

        if not auth_check["user_id"]:
            return { "error": "Autenticação inválida" }, 401

        return { "message": "Autenticado" }, 200

def check_token():
    token = request.cookies.get(AUTH_COOKIE_NAME)
    if not token:
        return { "invalid": True, "message": "Não autenticado" }
    user_id = AuthHelper.verify_token(token)
    if not user_id:
        return { "invalid": True, "message": "Sua sessão expirou" }
    return { "invalid": False, "user_id": user_id }

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        auth_check = check_token()

        if auth_check["invalid"]:
            return { "error": auth_check["message"] }, 401

        if not auth_check["user_id"]:
            return { "error": "Autenticação inválida" }, 401

        kwargs["user_id"] = auth_check["user_id"]
        return f( *args, **kwargs )
    
    return decorated_function
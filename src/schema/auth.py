from pydantic import BaseModel, Field

class Auth_LoginSchema(BaseModel):
    """ Define como será a estrutura do retorno após o login
    """
    message: str

class Auth_LogoutSchema(BaseModel):
    """ Define como será a estrutura do retorno após o logout
    """
    message: str

class Auth_CheckStatusSchema(BaseModel):
    """ Define como será a estrutura do retorno após o logout
    """
    message: str
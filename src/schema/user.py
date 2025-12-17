from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

# --------------
# Views Schema

class User_ViewSchema(BaseModel):
    """ Define a estrutura de retorno de um usuário
    """
    id: int = 1
    username: str = "usuario"
    email: str = "usuario@email.com"
    cep: str = "01001-000"
    city: str = "São Paulo"
    state: str = "SP"

# --------------
# Add Schema

class User_AddFormSchema(BaseModel):
    """ Define como um novo usuário a ser inserido deve ser estruturado
    """
    model_config = ConfigDict(extra='forbid')
    username: str = Field(..., example="usuario")
    email: str = Field(..., example="usuario@email.com")
    cep: str = Field(..., example="01001-000")
    city: str = Field(..., example="São Paulo")
    state: str = Field(..., example="SP")
    password: str = Field(..., example="12345678")

class User_AddReturnSchema(BaseModel):
    """ Define a estrutura de retorno após a inserção de um usuário
    """
    data: User_ViewSchema
    message: str

# --------------
# Update Schema

class User_UpdateFormSchema(BaseModel):
    """ Define como um usuário a ser atulizado deve ser estruturado
    """
    model_config = ConfigDict(extra='forbid')
    username: str = Field(..., example="usuario")
    email: str = Field(..., example="usuario@email.com")
    cep: str = Field(..., example="01001-000")
    city: str = Field(..., example="São Paulo")
    state: str = Field(..., example="SP")
    password: Optional[str] = Field(default=None, example="novasenha1234")

class User_UpdateReturnSchema(BaseModel):
    """ Define a estrutura de retorno após a atualização de um usuário
    """
    data: User_ViewSchema
    message: str


# --------------
# Login

class User_LoginSchema(BaseModel):
    """ Define como os dados de login devem ser passados
    """
    model_config = ConfigDict(extra='forbid')
    username: str = Field(..., example="usuario")
    password: str = Field(..., example="minhasenha1234")
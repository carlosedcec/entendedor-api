from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List

# --------------
# Views Schema

class Symptom_ViewSchema(BaseModel):
    """ Define a estrutura de retorno de um sintoma
    """
    id: int = 1
    name: str = "Dor"
    order: int = 1

class Symptom_ListReturnSchema(BaseModel):
    """ Define como a listagem de sintomas será retornada
    """
    data: List[Symptom_ViewSchema]

# --------------
# Add Schema

class Symptom_AddFormSchema(BaseModel):
    """ Define como um novo sintoma a ser inserido deve ser estruturado
    """
    model_config = ConfigDict(extra='forbid')
    name: str = Field(..., example="Dor")

class Symptom_AddReturnSchema(BaseModel):
    """ Define a estrutura de retorno após a inserção de um sintoma
    """
    data: Symptom_ViewSchema
    message: str

# --------------
# Update Schema

class Symptom_IdSchema(BaseModel):
    """ Define o parâmetro a ser passado na URL para update ou delete
    """
    symptom_id: int

class Symptom_UpdateFormSchema(BaseModel):
    """ Define como um sintoma a ser atulizado deve ser estruturado
    """
    model_config = ConfigDict(extra='forbid')
    name: str = Field(..., example="Novo nome")

class Symptom_UpdateReturnSchema(BaseModel):
    """ Define a estrutura de retorno após a atualização de um sintoma
    """
    data: Symptom_ViewSchema
    message: str

class Symptom_UpdateOrderInnerFormSchema(BaseModel):
    """ Define como um sintoma deve ser estruturado para a atualização da ordenação dos sintomas
    """
    id: int = Field(..., example=1)
    order: int = Field(..., example=1)

class Symptom_UpdateOrderFormSchema(BaseModel):
    """ Define como deve ser a estrutura para a atualização da ordenação dos sintomas
    """
    model_config = ConfigDict(extra='forbid')
    symptoms_order: List[Symptom_UpdateOrderInnerFormSchema]

class Symptom_UpdateOrderReturnSchema(BaseModel):
    """ Define a estrutura de retorno após a atualização da ordenação dos sintomas
    """
    data: Symptom_ViewSchema
    message: str

# --------------
# Delete Schema

class Symptom_DeleteReturnSchema(BaseModel):
    """ Define a estrutura de retorno após a exclusão de um sintoma
    """
    message: str
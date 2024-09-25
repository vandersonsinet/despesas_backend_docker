from pydantic import BaseModel
from typing import Optional, List
from model.tipo_despesa import TipoDespesa


class TipoDespesaSchema(BaseModel):
    id_tipo_despesa: str = "id do tipo da despesa"
    descricao: str

class ListagemTipoDespesasSchema(BaseModel):
    tipoDespesas:List[TipoDespesaSchema]

def apresenta_tipos_despesas(tiposDespesas: List[TipoDespesa]):
    result = []
    for tipoDespesa in tiposDespesas:
        result.append({
            "id": tipoDespesa.id,
            "descricao": tipoDespesa.descricao,
            "data_insercao": tipoDespesa.data_insercao,
        })

    return {"tipoDespesas": result}

class TipoDespesaViewSchema(BaseModel):
    id: int = 1
    descricao: str = "Despesa de Aluguel"

def apresenta_tipo_despesa(tipoDespesa: TipoDespesa):
    return {
        "id": tipoDespesa.id,
        "descricao": tipoDespesa.descricao,
        "dataInsercao": tipoDespesa.data_insercao
    }

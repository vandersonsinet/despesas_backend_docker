from pydantic import BaseModel
from typing import Optional, List
from model.despesa import Despesa
from schemas.tipo_despesa import TipoDespesaSchema
import requests

class DespesaEditarSchema(BaseModel):
    """ Define como uma nova despesa a ser inserida deve ser representada
    """
    id: int
    descricao: str 
    quantidade: Optional[int]
    valor: float
    tipo_despesa_id: int

class DespesaSchema(BaseModel):
    """ Define como uma nova despesa a ser inserida deve ser representada
    """
    descricao: str
    quantidade: Optional[int]
    valor: float
    tipo_despesa_id: int

class ApresentaDespesaSchema(BaseModel):

    descricao: str
    quantidade: Optional[int]
    valor: float
    tipo_despesa_id: int
    tipo_despesa: TipoDespesaSchema 

class DespesaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca que será
        feita apenas com base no nome da despesa.
    """
    nome: str = "Teste"

class ListagemDespesasSchema(BaseModel):
    """ Define como uma listagem de despesas será retornada.
    """
    despesas:List[ApresentaDespesaSchema]


def apresenta_despesas(despesas: List[Despesa]):
    """ Retorna uma representação da despesa seguindo o schema definido em
        DespesaViewSchema.
    """
    result = []

    for despesa in despesas:

        if despesa.tipo_despesa.id == 7:
            taxa_cambio = obter_taxa_cambio()
            #taxa_cambio = 6.072109
            taxa_cambio_f = "{:.2f}".format(taxa_cambio)
            despesa_float = float(despesa.valor)
            valor_final = despesa_float * float(taxa_cambio_f)
            despesa.valor = valor_final
        result.append({
            "descricao": despesa.descricao,
            "quantidade": despesa.quantidade,
            "valor": despesa.valor,
            "id_despesa": despesa.id,
            "tipo_despesa": {"id": despesa.tipo_despesa.id, "descricao": despesa.tipo_despesa.descricao}
        })

    return {"despesas": result}

def obter_taxa_cambio() -> float:

    # api_key = '5c80df676dc2d8e96d1c5f70705ef6bb'
     api_key = '6925460ff87c7fa6929e6b75d6a40ca5'

     symbols = 'BRL'

    # Endpoint da API para obter as taxas de câmbio mais recentes
     url = f"http://data.fixer.io/api/latest?access_key={api_key}&symbols={symbols}"

    # Faz a requisição GET à API do Fixer
     response = requests.get(url)

    # Verifica se a resposta foi bem-sucedida
     if response.status_code == 200:
         data = response.json()
         if data.get("success"):
             # Exibe as taxas de câmbio
             print("Taxas de câmbio:", data["rates"])
             taxa_cambio = data['rates'].get(symbols)
             if taxa_cambio:
                return taxa_cambio
             else:
                raise ValueError(f"A moeda {symbols} não foi encontrada na resposta.")
         else:
             print("Erro ao obter as taxas de câmbio:", data.get("error"))
     else:
         print(f"Falha na requisição. Status Code: {response.status_code}")
    
    # return 6.22


class DespesaViewSchema(BaseModel):
    """ Define como uma despesa será retornada: despesa.
    """
    id: int = 1
    descricao: str = "Despesa de Deslocamento"
    quantidade: Optional[int] = 1
    valor: float = 50.00


class DespesaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    id: str

def apresenta_despesa(despesa: Despesa):
    """ Retorna uma representação da despesa seguindo o schema definido em
        DespesaViewSchema.
    """
    return {
        "id": despesa.id,
        "descricao": despesa.descricao,
        "quantidade": despesa.quantidade,
        "valor": despesa.valor
    }

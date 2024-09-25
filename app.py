from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Despesa
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="API - Cadastro de despesas", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)
despesa_tag = Tag(name="Despesa", description="Adição, visualização e remoção de despesas à base")
tipo_despesa_tag = Tag(name="TipoDespesa", description="visualização dos tipos de depesa")
home_tag = Tag(name="Documentação", description="Documentação da api em Swagger")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para documentação da api em Swagger
    """
    return redirect('/openapi/swagger')

@app.post('/adicionaDespesa', tags=[despesa_tag],
          responses={"200": DespesaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_despesa(form: DespesaSchema):
    """Adiciona uma nova despesa à base de dados

    Retorna uma representação das despesas.
    """
    despesa = Despesa(
        descricao=form.descricao,
        quantidade=form.quantidade,
        valor=form.valor,
        tipo_despesa_id=form.tipo_despesa_id)
    logger.debug(f"Adicionando a despesa com a descriçao: '{despesa.descricao}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(despesa)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado a despesa com a descricao: '{despesa.descricao}'")
        return apresenta_despesa(despesa), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Uma despesa com a mesma descricao já foi salva na base :/"
        logger.warning(f"Erro ao adicionar despesa '{despesa.descricao}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar despesa '{despesa.descricao}', {error_msg}")
        return {"mesage": error_msg}, 400
    
@app.get('/listarDespesas', tags=[despesa_tag],
         responses={"200": ListagemDespesasSchema, "404": ErrorSchema})
def get_despesas():

    # criando conexão com a base
    session = Session()
    # fazendo a busca
    despesas = session.query(Despesa).all()

    if not despesas:

        return {"despesas": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(despesas))

        return apresenta_despesas(despesas), 200
    
@app.delete('/removerDespesa', tags=[despesa_tag],
            responses={"200": DespesaDelSchema, "404": ErrorSchema})
def del_despesa(query: DespesaDelSchema):
    """Deleta a despesa a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    despesa_id = query.id
    print(despesa_id)
    logger.debug(f"Deletando dados sobre despesa #{despesa_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Despesa).filter(Despesa.id == despesa_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado despesa #{despesa_id}")
        return {"mesage": "Despesa removida", "id": despesa_id}
    else:
        error_msg = "Despesa não encontrado na base :/"
        logger.warning(f"Erro ao deletar despesa #'{despesa_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    


@app.put('/editarDespesa', tags=[despesa_tag],
            responses={"200": DespesaEditarSchema, "404": ErrorSchema})
def alterar_despesa(form: DespesaEditarSchema):
    """Atualizar a despesa

    """
    despesa_id = form.id
    tipo_despesa_id = form.tipo_despesa_id
    session = Session()
    # recuperar a despesa informada da base
    despesa = session.query(Despesa).filter(Despesa.id == despesa_id).first()

    try:

        if not despesa:
            erro = "Nenhuma despesa encontrada para o id informado!"
            return {"message": erro}, 200
        
        despesa.id = form.id
        despesa.descricao = form.descricao
        despesa.quantidade = form.quantidade
        despesa.valor = form.valor
        despesa.tipo_despesa_id = tipo_despesa_id

        session.add(despesa)
        session.commit()

        return apresenta_despesa(despesa), 200

    except IntegrityError as e:
        error_msg = "Uma despesa com a mesma descricao já foi salva na base :/"
        logger.warning(f"Erro ao adicionar despesa '{despesa.descricao}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        error_msg = "Não foi possível salvar a despesa alterada :/"
        logger.warning(f"Erro ao adicionar despesa '{despesa.descricao}', {error_msg}")
        return {"mesage": error_msg}, 400

@app.get('/listarTipoDespesas', tags=[tipo_despesa_tag],
         responses={"200": ListagemTipoDespesasSchema, "404": ErrorSchema})
def get_tipo_despesas():
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    tipoDespesas = session.query(TipoDespesa).all()

    if not tipoDespesas:
        return {"tipos de despesas": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(tipoDespesas))
        print(tipoDespesas[0].id)
        return apresenta_tipos_despesas(tipoDespesas), 200
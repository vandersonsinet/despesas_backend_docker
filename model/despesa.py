from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from datetime import datetime
from typing import Union
from sqlalchemy.orm import relationship

from  model import Base

class Despesa(Base):
    __tablename__ = 'despesa'

    id = Column("id", Integer, primary_key=True)
    descricao = Column(String(140), unique=True)
    quantidade = Column(Integer)
    valor = Column(Float)
    data_insercao = Column(DateTime, default=datetime.now())
    tipo_despesa_id = Column(Integer, ForeignKey("tipo_despesa.id"), nullable=False)
    tipo_despesa = relationship("TipoDespesa", back_populates="despesa")

    def __init__(self, descricao:str, quantidade:int, valor:float, tipo_despesa_id:int,
                 data_insercao:Union[DateTime, None] = None):
        
        self.descricao = descricao
        self.quantidade = quantidade
        self.valor = valor
        self.tipo_despesa_id = tipo_despesa_id

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao



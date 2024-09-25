from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from typing import Union
from sqlalchemy.orm import relationship

from  model import Base

class TipoDespesa(Base):
    __tablename__ = 'tipo_despesa'

    id = Column("id", Integer, primary_key=True)
    descricao = Column(String(50), unique=True)
    data_insercao = Column(DateTime, default=datetime.now())
    despesa = relationship("Despesa", back_populates="tipo_despesa")

    def __init__(self, descricao:str, 
                 data_insercao:Union[DateTime, None] = None):
        
        self.data_insercao = data_insercao
        self.descricao = descricao

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao



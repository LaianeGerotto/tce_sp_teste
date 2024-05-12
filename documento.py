from sqlalchemy import Column, Integer, String, Date, Text
from base import Base


class Documento(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True)
    doc = Column(String(250))
    n_processo = Column(String(250))
    data_autuacao = Column(Date)
    materia = Column(String(250))
    ementa = Column(Text(5000))
    tribunal = Column(String(250))
    link = Column(String(250))

    def __repr__(self):
        return f"Documento {self.n_processo}"

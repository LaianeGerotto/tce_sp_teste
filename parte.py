from sqlalchemy import Column, Integer, String, ForeignKey
from base import Base


class Parte(Base):
    __tablename__ = "partes"

    id = Column(Integer, primary_key=True)
    parte = Column(String(250))
    doc_id = Column(ForeignKey("documentos.id"), nullable=False)

    def __repr__(self):
        return f"Parte {self.parte}"

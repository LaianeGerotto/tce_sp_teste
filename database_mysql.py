import os
from dotenv import load_dotenv
from sqlalchemy import (
    create_engine,
)

from sqlalchemy_utils import database_exists, create_database
from documento import Documento
from parte import Parte
from base import Base

from sqlalchemy.orm import sessionmaker


load_dotenv()
host_name = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
user_name = os.getenv("DB_USER")
password = os.getenv("DB_PASSWD")


# Criar Database
class SgbdMysql:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.engine = self.criar_db()

    def criar_db(self):
        engine = create_engine(
            f"mysql+pymysql://{user_name}:{password}@{host_name}/{self.db_name}",
            echo=False,
        )
        if not database_exists(engine.url):
            print(f"Database {self.db_name} nāo existe")
            create_database(engine.url)
            print(f"Database {self.db_name} criado com sucesso.")

        print("Banco Conectado!")

        return engine

    # Criar Tabela
    def criar_tabela(self):
        Base.metadata.create_all(self.engine)

    # Inserir dados nas Tabelas documentos e partes
    def inserir_dados(self, lista):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        lista_doc_mysql = []
        for i in lista:
            id = self.select_dados(i)
            documento = Documento(
                id=id,
                doc=i["processo"]["doc"],
                n_processo=i["processo"]["n_processo"],
                data_autuacao=i["processo"]["data_autuacao"],
                materia=i["processo"]["materia"],
                ementa=i["processo"]["ementa"],
                tribunal=i["processo"]["tribunal"],
                link=i["processo"]["link"],
            )

            if not id:
                session.add(documento)
                session.commit()
                print(documento.id)

                for j in i["partes"]:
                    if len(j["parte"]) > 0:
                        teste_parte = Parte(parte=j["parte"], doc_id=documento.id)
                        session.add(teste_parte)
                        session.commit()
            i["processo"]["id"] = documento.id
            lista_doc_mysql.append(i)
        return lista_doc_mysql

    def select_dados(self, i):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        query = session.query(Documento).where(
            Documento.n_processo == i["processo"]["n_processo"]
        )
        resultado = session.execute(query)
        documentos = resultado.all()
        if documentos:
            return documentos[0][0].id
        return None

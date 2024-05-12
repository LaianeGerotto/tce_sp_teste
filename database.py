import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Date, insert
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
def create_db(db_name):
    engine = create_engine(
        f"mysql+pymysql://{user_name}:{password}@{host_name}/{db_name}", echo=False
    )
    if not database_exists(engine.url):
        print(f"Database {db_name} not exists")
        create_database(engine.url)
        print(f"Database {db_name} created successfully.")
    print("Connected Database")

    return engine


# Criar Tabela
def create_table(engine):
    Base.metadata.create_all(engine)


# Inserir dados nas Tabelas documentos e partes
def insert_tables(engine, lista):
    Session = sessionmaker(bind=engine)
    session = Session()

    for i in lista:
        documento = Documento(
            doc=i["processo"]["doc"],
            n_processo=i["processo"]["n_processo"],
            data_autuacao=i["processo"]["data_autuacao"],
            materia=i["processo"]["materia"],
            ementa=i["processo"]["ementa"],
            tribunal=i["processo"]["tribunal"],
            link=i["processo"]["link"],
        )
        session.add(documento)
        session.commit()
        print(documento.id)

        for j in i["partes"]:
            if len(j["parte"]) > 0:
                teste_parte = Parte(parte=j["parte"], doc_id=documento.id)
                session.add(teste_parte)
                session.commit()

    # teste = Documento(
    #     doc="Teste",
    #     n_processo="Teste",
    #     data_autuacao="2024-01-01",
    #     materia="aaaaaaaaa",
    #     ementa="fsfsfsfsfsffsfsf",
    #     tribunal="tce",
    #     link="wwwwww",
    # )
    # session.add(teste)
    # session.commit()
    # print(teste.id)

    # teste_parte = Parte(parte="Meg", doc_id=teste.id)
    # session.add(teste_parte)
    # session.commit()

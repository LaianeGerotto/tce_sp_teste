# -*- coding: utf-8 -*-
import datetime
from elasticsearch import Elasticsearch
import os

from dotenv import load_dotenv

load_dotenv()
host = os.getenv("ES_HOST")
port = os.getenv("ES_PORT")
user = os.getenv("ES_USER")
passwd = os.getenv("ES_PASSWD")


class SgbdEs:
    def __init__(self, es_name: str):
        self.es_name = es_name
        self.es = self.conectar_es()
        self.acessar_index()

    # CONECTAR COM ELASTICSEARCH
    def conectar_es(self):
        es = Elasticsearch(
            [{"host": str(host), "port": int(port), "scheme": "http"}],
            basic_auth=(user, passwd),
        )
        print(es.info())
        print("Conectado ao Elasticsearch")
        return es

    # CRIAR/ACESSAR INDEX
    def acessar_index(self):
        try:
            self.es.search(index=self.es_name)

        except:
            print(f"{self.es_name} Nāo encontrado!")
            self.es.indices.create(index=self.es_name)
            print(f"{self.es_name} criado com sucesso!")

    # ENVIAR DADOS PARA O ELASTICSEARCH
    def inserir_dados(self, dados):
        for i in dados:
            lista = []
            processo = i["processo"]
            for j in i["partes"]:
                lista.append(j["parte"])
            processo["partes"] = lista
            teste = self.es.index(
                index=self.es_name, id=i["processo"]["id"], body=processo
            )
            print(f"Status Inserçāo: {teste['result']}")


############
# Deletar index por completo
# print(self.es.indices.delete(index="teste-elastic"))

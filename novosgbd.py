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
# Variavel de Conexāo
# teste = Elasticsearch(
#     host=os.getenv("ES_HOST"),
#     port=os.getenv("ES_PORT"),
# )

# es = Elasticsearch(
#     hosts="http://localhost:9200", basic_auth=[user, passwd], verify_certs=False
# )


es = Elasticsearch(
    [{"host": str(host), "port": int(port), "scheme": "http"}],
    basic_auth=(user, passwd),
)

print(es.info())

resultado = {
    "processo": {
        "doc": "Processo",
        "link": "https://jurisprudencia.tce.sp.gov.br",
        "n_processo": "12345",
        "data_autuacao": datetime.date(2023, 1, 1),
        "materia": "Lorem",
        "ementa": "Praesent rhoncus dictum ipsum eget accumsan. Phasellus facilisis leo turpis",
        "tribunal": "tce_sp",
        "partes": [{"parte": "Proin urna magna"}, {"parte": "Suspendisse rutrum urna"}],
    }
}

teste = es.index(index="turivius", id=2, body=resultado)
print(f"Status Inserçāo: {teste['result']}")

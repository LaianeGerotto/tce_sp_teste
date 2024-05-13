# -*- coding: utf-8 -*-
from novosgbd import Elasticsearch

# Variavel de Conexāo
teste = Elasticsearch(
    ["192.168.1.228"],
    port=8000,
)

print(teste.info())

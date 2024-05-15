from database_mysql import SgbdMysql
from tribunais.tce_sp import TceSp

from database_es import SgbdEs

db_name = "teste_mysql"  # Nome do Banco de Dados no Mysql
es_name = "teste_elastic"  # Nome do index no Elasticsearch

pesquisa = "Fraudes em Escolas"  # Palavras chaves para a busca no site do TCE SP
periodo = [2023]  # Periodo da Busca no site do TCE SP


# INICIAR A EXTRAÇĀO DOS DADOS
tce = TceSp(pesquisa, periodo)
dados, dados_brutos = tce.requests_tce()

# PARA CRIAR/CONECTAR AO BANCO DE DADOS
sgbd_mysql = SgbdMysql(db_name)

# # Para Criar as Tabelas
# PARA CRIAR AS TABELAS NO BANCO DE DADOS
table = sgbd_mysql.criar_tabela()


# PARA INSERIR OS DADOS EXTRAÍDOS/TRATADOS NO BANCO DE DADOS - MYSQL
lista_doc_mysql = sgbd_mysql.inserir_dados(dados)


# Para gerar o arquivo JSON com os dados Brutos
# utils.convert_json(dados_brutos)


# PARA CONECTAR AO ELASTICSEARCH
sgbd_es = SgbdEs(es_name)

# PARA ACESSAR/CRIAR INDEX
sgbd_es.acessar_index()

# INSERIR DADOS ELASTICSEARH
sgbd_es.inserir_dados(lista_doc_mysql)

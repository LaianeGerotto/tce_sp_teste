import database, utils
from tribunais.tce_sp import TceSp


db_name = "Turivius"
periodo = [2023]
pesquisa = "Fraudes em Escolas"
# pesquisa = "SERRAAESTRELLLA"

# Para iniciar a Raspagem
# lista, dados_brutos = utils.requests_tce(pesquisa, periodo)
# print(lista)

tce = TceSp(pesquisa, periodo)
# dados, dados_brutos = tce.requests_tce()
# print(dados)

dados = tce.requests_tce()
print(dados)

# Para criar/Conectar o Banco de Dados
# engine = database.create_db(db_name)

# # Para Criar as Tabelas
# table = database.create_table(engine)

# # Para inserir os dados extraídos/tratados no Banco
# database.insert_tables(engine, lista)


# Para gerar o arquivo JSON com os dados Brutos
# utils.convert_json(dados_brutos)


#### VERIFICAR a necessidade do arquivo tce_sp

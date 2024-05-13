import database, utils


db_name = "Turivius"
periodo = [2023]
pesquisa = "Fraudes"
# pesquisa = "SERRAAESTRELLLA"

# Para iniciar a Raspagem
lista, dados_brutos = utils.requests_tce(pesquisa, periodo)
# print(lista)

# Para criar/Conectar o Banco de Dados
# engine = database.create_db(db_name)

# # Para Criar as Tabelas
# table = database.create_table(engine)

# # Para inserir os dados extraídos/tratados no Banco
# database.insert_tables(engine, lista)


# Para gerar o arquivo JSON com os dados Brutos
utils.convert_json(dados_brutos)


#### VERIFICAR a necessidade do arquivo tce_sp

# TCE SP - EXTRAÇĀO DE DADOS
## Finalidade do Projeto
### O projeto consiste em extrair os dados públicos do [TRIBUNAL DE CONTAS DO ESTADO DE SĀO PAULO - TCE SP](https://www.tce.sp.gov.br/jurisprudencia/), realizar o tratamento dos dados brutos e inserir no Banco de Dados.
#
## Tecnologias/Bibliotecas
- Python
- Requests
- BeautifulSoup
- SQLAlchemy
- Elasticsearch

## Tela de Busca - TCE SP
#### Inserir imagem
#
## Instruções de uso

- Criar `.env` com as seguintes variáveis:
```
    DB_HOST=mysql    
    DB_PORT=3306
    DB_USER=***
    DB_PASSWD=***    
    ES_HOST=elasticsearch
    ES_PORT=9200
    ES_USER=***
    ES_PASSWD=***
    MYSQL_ROOT_PASSWORD=***
```
## Docker
- Instalar o Docker e executar os seguintes comandos:

    ```
    docker compose build scraping
    docker compose run scraping
    ```


## Testes
- Para executar os testes no Docker é necessário rodar o comando abaixo:
    ```
    docker compose run -it scraping python -m pytest tests/
    ```

import requests
from bs4 import BeautifulSoup
import re
import math

URL = "https://www.tce.sp.gov.br/jurisprudencia/"

session = requests.Session()

session.headers.update(
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    }
)

response = session.get(URL)
print(response)  # Remover e inserir tratamento de erro

parametros = {
    "txtTdPalvs": "Fraudes",  # Ajustar
    "txtExp": "",
    "txtQqUma": "",
    "txtNenhPalvs": "",
    "txtNumIni": "",
    "txtNumFim": "",
    "tipoBuscaTxt": "Documento",
    "_tipoBuscaTxt": "on",
    "quantTrechos": 1,
    "processo": "",
    "exercicio": [2023],  # Ajustar
    "dataAutuacaoInicio": "",
    "dataAutuacaoFim": "",
    "dataPubInicio": "",
    "dataPubFim": "",
    "_relator": 1,
    "_auditor": 1,
    "_materia": 1,
    "_tipoDocumento": 1,
    "acao": "Executa",
}

response_doc = session.get(URL + "pesquisar", params=parametros)

print(response_doc)  # Remover e inserir tratamento de erro
home_page = BeautifulSoup(response_doc.content, "html.parser")

qtde_registros = home_page.find("h3", class_="nopadding").text
print(qtde_registros)

# DO Preparar o Script para ausencia de dados


def listaChaves(home_page):
    chaves = home_page.find_all("th", class_="alinhamento")
    lista_chaves = []
    for i in chaves:
        chave = i.get_text("", strip=True)
        lista_chaves.append(chave)
    return lista_chaves


# paginacao = home_page.find("a", class_="page-link pn prev")
# if not paginacao:
# #     paginacao = home_page.find_all("li", class_="page-item")[-2]
# #     paginacao = paginacao.find("a").get("href")
paginas = re.search("Foram encontrados (\d+) registros", qtde_registros)

# paginas = re.search("offset=(\d+)", paginacao)
if paginas:
    paginas = int(paginas.group(1))
    total_paginas = math.ceil(paginas / 10)  # Melhorar

lista_chaves = listaChaves(home_page)
print(lista_chaves)

# Raspagem dos documentos/processos

lista_documentos = []


def get_documentos(home_page):
    documentos = home_page.find_all("tr", class_="borda-superior")

    for i in documentos:
        dict_documentos = {}
        lista_valores = []
        itens = i.find_all(True)
        for j in itens:
            if len(j.contents) == 0:
                continue
            valor = j.get_text(" ", strip=True)
            if len(j) > 3:  # Necessario para limitar a td ref. ao numero do processo
                valor = j.contents[0].get_text()
            if j.find("a") and j.a.has_attr("href"):
                link = j.a["href"]
                if not link.startswith("https://www.tce.sp.gov.br"):
                    link = "https://www.tce.sp.gov.br/jurisprudencia/" + link
                valor = {"nome": valor, "link": link}
            lista_valores.append(valor)
            dict_documentos = dict(list(zip(lista_chaves, lista_valores)))
        if len(dict_documentos) > 1:
            conteudo = (
                i.find_next("tr")
                .find("ul")
                .get_text("", strip=True)
                .replace("\n", "")
                .replace("  ", " ")
            )
            dict_documentos["Conteudo"] = conteudo
            lista_documentos.append(dict_documentos)

    return lista_documentos


lista_documentos = get_documentos(home_page)
if total_paginas > 1:
    i = 1
    while i <= (total_paginas - 1):
        print(f"Total da lista no WHILE {len(lista_documentos)}")
        print(f"Pagina atual {i}")
        response_doc = session.get(
            URL + "pesquisar", params={"acao": "Executa", "offset": i * 10}
        )
        # tratamento para status code
        if response_doc.status_code != 200:
            print(f"Erro: {response_doc.status_code}")
            break
        home_page = BeautifulSoup(response_doc.content, "html.parser")

        get_documentos(home_page)
        i = i + 1


print(lista_documentos)


# Inserir informativo se todos dos registros foram inseridos = Total de registro encontrados x len(lista_documentos)

# VER SOBRE POSSIVEL IMPLEMENTACAO: Um dos links direciona para outra pagina que contem outros documentos para download

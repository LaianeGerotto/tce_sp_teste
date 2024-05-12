import requests
from bs4 import BeautifulSoup
import re
import math
import json
from datetime import datetime

URL = "https://www.tce.sp.gov.br/jurisprudencia/"


def listaChaves(home_page):
    chaves = home_page.find_all("th", class_="alinhamento")
    lista_chaves = []
    for i in chaves:
        chave = i.get_text("", strip=True)
        lista_chaves.append(chave)
    return lista_chaves


def get_documentos(home_page, lista_documentos, lista_chaves):
    documentos = home_page.find_all("tr", class_="borda-superior")

    for i in documentos:
        dict_documentos = {}
        lista_valores = []
        itens = i.find_all("td")
        for j in itens:
            if len(j.contents) == 0:
                continue
            valor = j.get_text(" ", strip=True)
            if len(j) > 3:  # Necessario para limitar a td ref. ao numero do processo
                valor = j.contents[0].get_text()
            if j.find("a") and j.a.has_attr("href"):
                link = j.a["href"]
                if not link.startswith("https://jurisprudencia.tce.sp.gov.br"):
                    link = "https://www.tce.sp.gov.br/jurisprudencia/" + link
                valor = {"nome": valor, "link": link}
            lista_valores.append(valor)

            dict_documentos = dict(list(zip(lista_chaves, lista_valores)))
        if len(dict_documentos) > 1:
            conteudo = (
                i.find_next("tr")
                .find("ul")
                .get_text(" ", strip=True)
                .replace("\n", "")
                .replace("  ", " ")
                .upper()
            )
            dict_documentos["Conteudo"] = conteudo
            dict_documentos["Tribunal"] = "tce_sp"
            lista_documentos.append(dict_documentos)

    return lista_documentos


def requests_tce(pesquisa, periodo):

    # Validar o Periodo para evitar dados extras
    for i in periodo:
        if len(str(i)) != 4:
            raise Exception(f"Periodo Inválido: {periodo}")

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        }
    )

    response = session.get(URL)
    if response.status_code != 200:
        response.raise_for_status()

    parametros = {
        "txtTdPalvs": pesquisa,
        "txtExp": "",
        "txtQqUma": "",
        "txtNenhPalvs": "",
        "txtNumIni": "",
        "txtNumFim": "",
        "tipoBuscaTxt": "Documento",
        "_tipoBuscaTxt": "on",
        "quantTrechos": 1,
        "processo": "",
        "exercicio": periodo,
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
    if response.status_code != 200:  # Tratamento de erro
        response.raise_for_status()

    home_page = BeautifulSoup(response_doc.content, "html.parser")

    # Verifica se a pagina possui alguma mensagem erro/alerta
    mensagem = home_page.find("div", class_="alert alert-info")
    if mensagem:
        raise Exception(mensagem.get_text(" ", strip=True))

    qtde_registros = home_page.find("h3", class_="nopadding").text
    print(qtde_registros)

    paginas = re.search("Foram encontrados (\d+) registros", qtde_registros)

    # Cálculo para o Total de páginas
    if paginas:
        paginas = int(paginas.group(1))
        total_paginas = math.ceil(paginas / 10)  # Melhorar

    lista_chaves = listaChaves(home_page)

    lista_documentos = []
    lista_documentos = get_documentos(home_page, lista_documentos, lista_chaves)

    # Trecho para percorrer as outras páginas
    if total_paginas > 1:
        i = 1
        while i <= (total_paginas - 1):
            response_doc = session.get(
                URL + "pesquisar/", params={"acao": "Executa", "offset": i * 10}
            )

            if response_doc.status_code != 200:
                response_doc.raise_for_status()

            home_page = BeautifulSoup(response_doc.content, "html.parser")
            get_documentos(home_page, lista_documentos, lista_chaves)
            i = i + 1

    # Verificar se a quantidade de documentos extraidos é igual a quantidade encontrada na Busca.
    if len(lista_documentos) != paginas:
        raise Exception(
            f"Foram extraídos {len(lista_documentos)}/{paginas} documentos."
        )
    print(lista_documentos)

    # conteudo_json = json.dumps({"processos": lista_documentos}, ensure_ascii=False)
    # # conteudo_json = json.dumps(lista_documentos, ensure_ascii=False)
    conteudo_json = lista_documentos

    processos = tratamento_dados_brutos(lista_documentos)
    return processos, conteudo_json


def tratamento_dados_brutos(lista_documentos):
    # Tratamento os Dados para enviar ao Banco
    processos = []
    for i in lista_documentos:
        info = {
            "doc": i.get("Doc.")["nome"],
            "link": i.get("Doc.")["link"],
            "n_processo": i.get("N° Proc.")["nome"],
            "data_autuacao": datetime.strptime(i.get("Autuação"), "%d/%m/%Y").date(),
            "materia": i.get("Matéria"),
            "ementa": i.get("Conteudo"),
            "tribunal": i.get("Tribunal"),
        }

        partes = [{"parte": i["Parte 1"]}, {"parte": i["Parte 2"]}]
        processo = {"processo": info, "partes": partes}
        processos.append(processo)

    return processos


def convert_json(conteudo_json):
    with open("dados.json", "w") as arquivo:
        json.dump({"Documentos": conteudo_json}, arquivo, indent=2, ensure_ascii=False)


# Verificar se dos dados foram tratados (espaco, caracteres especiais)

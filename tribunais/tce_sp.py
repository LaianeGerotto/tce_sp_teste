from requests import Session
from bs4 import BeautifulSoup
import re
import math
import json
from datetime import datetime


class TceSp:
    def __init__(self, pesquisa: any, periodo: list[int]):
        self.pesquisa = pesquisa
        self.periodo = periodo
        self.url = "https://www.tce.sp.gov.br/jurisprudencia/"
        self.session = Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                + "Chrome/124.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;"
                + "q=0.8,application/signed-exchange;v=b3;q=0.7",
            }
        )

    # FUNÇĀO PARA VERIFICAR O PERIODO/INTERVALO DA BUSCA
    def validacao_periodo(self):
        if not self.periodo:
            return False
        try:
            for i in self.periodo:
                i = int(i)
                if len(str(i)) != 4 or type(i) is not int:
                    print(f"Periodo Inválido {self.periodo}")
                    return False
        except Exception as err:
            print(err)
            return False
        return True

    # FUNÇĀO PARA EXTRAIR AS CHAVES DOS DOCUMENTOS
    def listaChaves(self, home_page):
        chaves = home_page.find_all("th", class_="alinhamento")
        lista_chaves = []
        for i in chaves:
            chave = i.get_text("", strip=True)
            lista_chaves.append(chave)
        return lista_chaves

    # FUNCAO PARA EXTRAIR OS DOCUMENTOS
    def get_documentos(self, home_page, lista_chaves, lista_documentos):
        documentos = home_page.find_all("tr", class_="borda-superior")
        for i in documentos:
            dict_documentos = {}
            lista_valores = []
            itens = i.find_all("td")
            for j in itens:
                if len(j.contents) == 0:
                    continue
                valor = j.get_text(" ", strip=True)
                if (
                    len(j) > 3
                ):  # Necessario p/ limitar a tag 'td' ref. ao numero do processo
                    valor = j.contents[0].get_text()
                if j.find("a") and j.a.has_attr("href"):
                    link = j.a["href"]
                    if not link.startswith("https://jurisprudencia.tce.sp.gov.br"):
                        link = "https://www.tce.sp.gov.br/jurisprudencia/" + link
                    valor = {"nome": valor, "link": link}
                lista_valores.append(valor)

                dict_documentos = dict(list(zip(lista_chaves, lista_valores)))
            if len(dict_documentos) > 1:
                conteudo = i.find_next("tr").find("ul")
                if conteudo:
                    conteudo = (
                        conteudo.get_text(" ", strip=True)
                        .replace("\n", " ")
                        .replace("  ", " ")
                        .upper()
                    )

                dict_documentos["Conteudo"] = re.sub("[\ ]{2,}", "", conteudo).replace(
                    "\xa0", " "
                )
                dict_documentos["Tribunal"] = "tce_sp"
                lista_documentos.append(dict_documentos)

        return lista_documentos

    # FUNÇÃO PARA PERCORRER AS PAGINAS
    def percorrer_paginas(self, total_paginas, lista_documentos, lista_chaves):
        i = 1
        while i <= (total_paginas - 1):
            print(f"Pagina Atual {i}")
            response_doc = self.session.get(
                self.url + "pesquisar/", params={"acao": "Executa", "offset": i * 10}
            )

            if response_doc.status_code != 200:
                response_doc.raise_for_status()

            home_page = BeautifulSoup(response_doc.content, "html.parser")
            self.get_documentos(home_page, lista_chaves, lista_documentos)
            i = i + 1

        return lista_documentos

    # FUNÇĀO PARA INICIAR A EXTRAÇĀO DOS DADOS
    def requests_tce(self) -> list:
        """
        Função usa atributos da class TceSP para realizar a requisição
        no site e para obter os documentos públicos disponíveis, retornando os dados extraídos.

        Atributos:
            pesquisa (str): Palavras chaves para a busca no site do TCE SP.
            periodo (list[int]):  Periodo da Busca no site do TCE SP.

        Returns:
            List[dict]: Lista de Processos/Documentos com dados tratados.
            List[dict]: Lista de Processos/Documentos com dados brutos.
        """

        # VALIDAR O PERIODO/ANO
        if self.validacao_periodo() == False:
            raise Exception("Periodo inválido")

        response = self.session.get(self.url)
        if response.status_code != 200:
            response.raise_for_status()

        parametros = {
            "txtTdPalvs": self.pesquisa,
            "txtExp": "",
            "txtQqUma": "",
            "txtNenhPalvs": "",
            "txtNumIni": "",
            "txtNumFim": "",
            "tipoBuscaTxt": "Documento",
            "_tipoBuscaTxt": "on",
            "quantTrechos": 1,
            "processo": "",
            "exercicio": self.periodo,
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

        response_doc = self.session.get(self.url + "pesquisar", params=parametros)
        if response_doc.status_code != 200:
            response_doc.raise_for_status()

        home_page = BeautifulSoup(response_doc.content, "html.parser")

        # Verifica se a pagina possui alguma mensagem erro/alerta
        mensagem = home_page.find("div", class_="alert alert-info")
        if mensagem:
            raise Exception(mensagem.get_text(" ", strip=True))

        qtde_registros = home_page.find("h3", class_="nopadding").text
        print(qtde_registros)  # Quantidade de registros encontrados

        paginas = re.search("Foram encontrados (\d+) registros", qtde_registros)

        # Cálculo para o Total de páginas
        if paginas:
            paginas = int(paginas.group(1))
            total_paginas = math.ceil(paginas / 10)  # Melhorar

        lista_chaves = self.listaChaves(home_page)
        lista_documentos = []
        self.get_documentos(home_page, lista_chaves, lista_documentos)

        # Trecho para percorrer as outras páginas
        if total_paginas > 1:
            self.percorrer_paginas(total_paginas, lista_documentos, lista_chaves)

        # Verificar se a quantidade de documentos extraidos é igual a quantidade encontrada na Busca.
        if len(lista_documentos) != paginas:
            raise Exception(
                f"Foram extraídos {len(lista_documentos)}/{paginas} documentos."
            )

        # Salva os dados Brutos em outra variavel para uma possível conversão arquivo JSON.
        conteudo_json = lista_documentos

        # Limpeza/Tratamento dos Dados Brutos que nāo serāo utilizados no Banco de Dados
        processos = self.tratamento_dados_brutos(lista_documentos)
        print(f"Total de Processos/Documentos Capturados foram {len(processos)}.")
        return processos, conteudo_json

    # TRATAMENTO DOS DADOS BRUTOS
    def tratamento_dados_brutos(self, lista_documentos: list[dict]) -> list:
        processos = []
        for i in lista_documentos:
            info = {
                "doc": i.get("Doc.")["nome"],
                "link": i.get("Doc.")["link"],
                "n_processo": i.get("N° Proc.")["nome"],
                "data_autuacao": datetime.strptime(
                    i.get("Autuação"), "%d/%m/%Y"
                ).date(),
                "materia": i.get("Matéria"),
                "ementa": i.get("Conteudo"),
                "tribunal": i.get("Tribunal"),
            }

            partes = [{"parte": i["Parte 1"]}, {"parte": i["Parte 2"]}]
            processo = {"processo": info, "partes": partes}
            processos.append(processo)

        return processos

    # FUNÇĀO PARA CONVERTER A LISTA PARA JSON E ARMAZENAR NA MEMÓRIA
    def convert_json(self, conteudo_json: list):
        with open("dados.json", "w") as arquivo:
            json.dump(
                {"Documentos": conteudo_json}, arquivo, indent=2, ensure_ascii=False
            )

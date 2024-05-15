import pytest
import datetime
import requests_mock

from tribunais.tce_sp import TceSp


def test_valida_retorno():

    # Esse retorno contém os dados tratados e os dados Brutos
    retorno = [
        {
            "processo": {
                "doc": "Despacho",
                "link": "https://jurisprudencia.tce.sp.gov.br/arqs_juri/pdf/20008081.pdf",
                "n_processo": "7279/989/24",
                "data_autuacao": datetime.date(2024, 2, 26),
                "materia": "ENCAMINHA DOCUMENTO",
                "ementa": "...GABINETE DO CONSELHEIRO ROBSON MARINHO (11) 3292-3521 - GCRRM@TCE.SP.GOV.BR D E S P A C H O   PROCESSO: 00007279.989.24-8 REQUERENTE /SOLICITANTE: FRANCISCO ALVES DA SILVA (CPF ***. 326.188-**) ADVOGADO: ANDRESSA FRANCIELI GONCALVES DE SOUZA (OAB/SP 412.667) MENCIONADO(A): PREFEITURA MUNICIPAL DE AGUAS DA PRATA (CNPJ 44.831.733/0001-43) ASSUNTO: DENÚNCIA REFERENTE À FRAUDE DE DISPENSA DE LICITAÇÃO, PARA CONTRATAÇÃO DE EMPRESA PARA EXECUÇÃO DE SERVIÇOS DE REGULARIZAÇÃO DE PISO NA ESCOLA FELIPE URTADO NO DISTRITO DE SÃO ROQUE DA FARTURA, NA PREFEITURA DE ÁGUAS DA PRATA. INCLUI CONTRATADO PRÉ-DEFINIDO, INÍCIO DA OBRA ANTES DO CONTRATO, EMPENHO...",
                "tribunal": "tce_sp",
            },
            "partes": [
                {"parte": "FRANCISCO ALVES DA SILVA"},
                {"parte": "PREFEITURA MUNICIPAL DE AGU..."},
            ],
        },
        {
            "processo": {
                "doc": "Despacho",
                "link": "https://jurisprudencia.tce.sp.gov.br/arqs_juri/pdf/932748.pdf",
                "n_processo": "15595/989/23",
                "data_autuacao": datetime.date(2023, 8, 1),
                "materia": "ENCAMINHA DOCUMENTO",
                "ementa": "...21/09/2023, 11:31 E-PROCESSO.TCE.SP.GOV.BR/E-TCESP/LISTAGENS/DOWNLOADARQUIVO?VIS&ARQUIVO=8133236 HTTPS://E-PROCESSO.TCE.SP.GOV.BR/E-TCESP/LISTAGENS/DOWNLOADARQUIVO?VIS&ARQUIVO=8133236 1/2 D E S P A C H OPROCESSO: 00015595.989.23-7 REQUERENTE/SOLICITANTE: FRANCISCO ALVES DA SILVA (CPF ***.326.188-**) ADVOGADO: ANDRESSA FRANCIELI GONCALVES DE SOUZA (OAB/SP 412.667) MENCIONADO(A): PREFEITURA MUNICIPAL DE AGUAS DA PRATA (CNPJ 44.831.733/0001-43) ASSUNTO: ASSUNTO: DENÚNCIA REFERENTE À INDÍCIOS DE FRAUDE À LICITAÇÃO NA CARTA CONVITE Nº. 003/2023, BEM COMO DE DISPENSAS E PAGAMENTOS RELACIONADOS, DA PREFEITURA DE ÁGUAS DA PRATA. EXERCÍCIO: 2023...",
                "tribunal": "tce_sp",
            },
            "partes": [
                {"parte": "FRANCISCO ALVES DA SILVA"},
                {"parte": "PREFEITURA MUNICIPAL DE AGU..."},
            ],
        },
    ]

    with open("./tests/pagina_inicial.html", "r") as file:
        page = file.read()

    with open("./tests/pagina_teste_func.html", "r") as file:
        page2 = file.read()

    with requests_mock.Mocker() as m:

        m.get(
            "https://www.tce.sp.gov.br/jurisprudencia/",
            text=page,
        )

        m.get(
            "https://www.tce.sp.gov.br/jurisprudencia/pesquisar?txtTdPalvs=Fraudes+em+Escolas&txtExp=&txtQqUma=&txtNenhPalvs=&txtNumIni=&txtNumFim=&tipoBuscaTxt=Documento&_tipoBuscaTxt=on&quantTrechos=1&processo=&exercicio=2023&dataAutuacaoInicio=&dataAutuacaoFim=&dataPubInicio=&dataPubFim=&_relator=1&_auditor=1&_materia=1&_tipoDocumento=1&acao=Executa",
            text=page2,
        )

        tce = TceSp("Fraudes em Escolas", [2023])
        resp = tce.requests_tce()
        assert retorno == resp[0]

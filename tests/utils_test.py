from utils import validacao_periodo, tratamento_dados_brutos, get_documentos
import pytest
import datetime
from bs4 import BeautifulSoup


# TESTE UNITARIO/UNIDADE

# TESTE PARA VERIFICAR O PERIODO - ANO


# PERIODO INVÁLIDO - LISTA COM INTEIRO
def test_len_validacao_periodo_invalido():
    assert validacao_periodo([200]) == False


# PERIODO VÁLIDO - LISTA COM INTEIRO
def test_len_validacao_periodo_valido():
    assert validacao_periodo([2000]) == True


# PERIODO INVÁLIDO - LISTA COM STRING
def test_validacao_periodo_lista_string():
    assert validacao_periodo(["test"]) == False


# PERIODO INVALIDO EM CASO DE STRING
def test_validacao_periodo_string_invalido():
    assert validacao_periodo("2000") == False


# PERIODO INVALIDO EM CASO DE INTEIRO SEM LISTA
def test_validacao_periodo_inteiro():
    assert validacao_periodo(1000) == False


# PERIODO INVALIDO EM CASO DE LISTA VAZIA
def test_validacao_periodo_lista_vazia():
    assert validacao_periodo([]) == False


def test_tratamento_dados_brutos_validos():
    lista = [
        {
            "Doc.": {
                "nome": "Processo",
                "link": "https://jurisprudencia.tce.sp.gov.br",
            },
            "N° Proc.": {"nome": "12345", "link": "https://www.tce.sp.gov.br"},
            "Autuação": "01/01/2023",
            "Parte 1": "Proin urna magna",
            "Parte 2": "Suspendisse rutrum urna",
            "Matéria": "Lorem",
            "Objeto": "Lorem ipsum",
            "Exercício": "2023",
            "Conteudo": "Praesent rhoncus dictum ipsum eget accumsan. Phasellus facilisis leo turpis",
            "Tribunal": "tce_sp",
        }
    ]

    resultado_esperado = [
        {
            "processo": {
                "doc": "Processo",
                "link": "https://jurisprudencia.tce.sp.gov.br",
                "n_processo": "12345",
                "data_autuacao": datetime.date(2023, 1, 1),
                "materia": "Lorem",
                "ementa": "Praesent rhoncus dictum ipsum eget accumsan. Phasellus facilisis leo turpis",
                "tribunal": "tce_sp",
            },
            "partes": [
                {"parte": "Proin urna magna"},
                {"parte": "Suspendisse rutrum urna"},
            ],
        }
    ]

    resultado = tratamento_dados_brutos(lista)
    assert resultado_esperado == resultado


def test_tratamento_dados_brutos_chave_invalida():
    lista = [
        {
            "teste": {
                "nome": "Processo",
                "link": "https://jurisprudencia.tce.sp.gov.br",
            },
            "N° Proc.": {"nome": "12345", "link": "https://www.tce.sp.gov.br"},
            "Autuação": "01/01/2023",
            "Parte 1": "Proin urna magna",
            "Parte 2": "Suspendisse rutrum urna",
            "Matéria": "Lorem",
            "Objeto": "Lorem ipsum",
            "Exercício": "2023",
            "Conteudo": "Praesent rhoncus dictum ipsum eget accumsan. Phasellus facilisis leo turpis",
            "Tribunal": "tce_sp",
        }
    ]
    with pytest.raises(TypeError, match="'NoneType' object is not subscriptable"):
        tratamento_dados_brutos(lista)


def test_tratamento_dados_brutos_chave_sem_valor_ementa():
    lista = [
        {
            "Doc.": {
                "nome": "Processo",
                "link": "https://jurisprudencia.tce.sp.gov.br",
            },
            "N° Proc.": {"nome": "12345", "link": "https://www.tce.sp.gov.br"},
            "Autuação": "01/01/2023",
            "Parte 1": "Proin urna magna",
            "Parte 2": "Suspendisse rutrum urna",
            "Matéria": "Lorem",
            "Objeto": "Lorem ipsum",
            "Exercício": "2023",
            "Conteudo": "",
            "Tribunal": "tce_sp",
        }
    ]
    resultado_esperado = [
        {
            "processo": {
                "doc": "Processo",
                "link": "https://jurisprudencia.tce.sp.gov.br",
                "n_processo": "12345",
                "data_autuacao": datetime.date(2023, 1, 1),
                "materia": "Lorem",
                "ementa": "",
                "tribunal": "tce_sp",
            },
            "partes": [
                {"parte": "Proin urna magna"},
                {"parte": "Suspendisse rutrum urna"},
            ],
        }
    ]

    resultado = tratamento_dados_brutos(lista)
    assert resultado_esperado == resultado


def test_tratamento_dados_brutos_lista_vazia():
    lista = []
    resultado_esperado = []
    resultado = tratamento_dados_brutos(lista)
    assert resultado_esperado == resultado


def test_get_documentos_e_uma_lista():
    with open("./tests/pagina_tce_sp.html", "r") as file:
        page = file.read()
    home_page = BeautifulSoup(page, "html.parser")
    lista_chaves = [
        "Doc.",
        "N° Proc.",
        "Autuação",
        "Parte 1",
        "Parte 2",
        "Matéria",
        "Objeto",
        "Exercício",
    ]

    resultado = get_documentos(home_page, lista_chaves)

    assert type(resultado) == list


def test_get_documentos_e_uma_lista():
    with open("./tests/pagina_tce_sp.html", "r") as file:
        page = file.read()
    home_page = BeautifulSoup(page, "html.parser")
    lista_chaves = [
        "Doc.",
        "N° Proc.",
        "Autuação",
        "Parte 1",
        "Parte 2",
        "Matéria",
        "Objeto",
        "Exercício",
    ]

    resultado = get_documentos(home_page, lista_chaves)

    assert type(resultado) == list

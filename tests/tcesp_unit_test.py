import pytest
import datetime
from bs4 import BeautifulSoup
from tribunais.tce_sp import TceSp


# TESTE PARA PERIODO INVÁLIDO - LISTA COM INTEIRO(TAMANHO DIFERENTE DE 4 DIGITOS)
def test_len_validacao_periodo_invalido():
    tce = TceSp("", [200])
    assert tce.validacao_periodo() == False


# TESTE PARA PERIODO VÁLIDO - LISTA COM INTEIRO(TAMANHO ESPERADO - 4 DIGITOS)
def test_len_validacao_periodo_valido():
    tce = TceSp("", [2000])
    assert tce.validacao_periodo() == True


# TESTE PARA PERIODO INVÁLIDO EM CASO DE UMA LISTA COM STRING
def test_validacao_periodo_lista_string():
    tce = TceSp("", ["test"])
    assert tce.validacao_periodo() == False


# TESTE PARA PERIODO INVÁLIDO EM CASO DE STRING
def test_validacao_periodo_string_invalido():
    tce = TceSp("", "2000")
    assert tce.validacao_periodo() == False


# TESTE PARA PERIODO INVÁLIDO EM CASO DE INTEIRO SEM LISTA
def test_validacao_periodo_inteiro():
    tce = TceSp("", 1000)
    assert tce.validacao_periodo() == False


# TESTE PARA PERIODO INVÁLIDO EM CASO DE LISTA VAZIA
def test_validacao_periodo_lista_vazia():
    tce = TceSp("", [])
    assert tce.validacao_periodo() == False


# TESTE PARA TRATAMENTO DE DADOS VÁLIDOS NA FUNÇĀO TRATAMENTO DADOS BRUTOS
def test_tratamento_dados_brutos_validos():
    tce = TceSp("", 2023)
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

    resultado = tce.tratamento_dados_brutos(lista)
    assert resultado_esperado == resultado


# TESTE PARA CHAVE INVÁLIDA NA FUNCĀO TRATATAMENTO DE DADOS BRUTOS
def test_tratamento_dados_brutos_chave_invalida():
    tce = TceSp("", 2023)
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
        tce.tratamento_dados_brutos(lista)


# TESTE PARA AUSENCIA DE VALOR NA CHAVE EMENTA
def test_tratamento_dados_brutos_chave_sem_valor_ementa():
    tce = TceSp("", 2023)
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

    resultado = tce.tratamento_dados_brutos(lista)
    assert resultado_esperado == resultado


# TESTE CASO A FUNÇĀO TRATAMENTO DE DADOS RECEBER UMA LISTA VAZIA
def test_tratamento_dados_brutos_lista_vazia():
    tce = TceSp("", 2023)
    lista = []
    resultado_esperado = []
    resultado = tce.tratamento_dados_brutos(lista)
    assert resultado_esperado == resultado


# TESTE PARA CONFIRMAR SE A FUNÇĀO GET_DOCUMENTOS RETORNA UMA LISTA DE DICIONÁRIOS
def test_get_documentos_e_uma_lista_com_dicionario():
    tce = TceSp("", 2023)
    with open("./tests/pagina_teste_unit.html", "r") as file:
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
    lista_documentos = []

    resultado = tce.get_documentos(home_page, lista_chaves, lista_documentos)

    assert type(resultado) is list and type(resultado[0]) is dict


# TESTE PARA VERIFICAR SE A FUNÇĀO GET_DOCUMENTOS RETORNA OS RESULTADOS ESPERADOS
def test_get_documentos_resultado_esperado_igual_resultado():
    tce = TceSp("", 2023)
    with open("./tests/pagina_teste_unit.html", "r") as file:
        page = file.read()
    home_page = BeautifulSoup(page, "html.parser")
    lista_chaves = [
        "Coluna1",
        "Coluna2",
        "Coluna3",
        "Coluna4",
        "Coluna5",
        "Coluna6",
        "Coluna7",
        "Coluna8",
    ]

    lista_documentos = []
    resultado_esperado = [
        {
            "Coluna1": {"nome": "AAA", "link": "https://jurisprudencia.tce.sp.gov.br"},
            "Coluna2": {
                "nome": "000/000/01",
                "link": "https://www.tce.sp.gov.br/jurisprudencia//lipsum.com/",
            },
            "Coluna3": "01/01/2023",
            "Coluna4": "",
            "Coluna5": "Cras et posuere metus",
            "Coluna6": "Lorem Ipsum 1",
            "Coluna7": "Pellentesque dui massa",
            "Coluna8": "2023",
            "Conteudo": "...INTERESSADO(A): AAAAA AAAAAA AAAAAAA (CPF ***.123.268-**) ADVOGADO: GSSGSG GSGSG (OAB/XX 01.001)ASSUNTO: QUISQUE CONDIMENTUM - EXERCÍCIO DE 2023 EXERCÍCIO: 2023 INSTRUÇÃO POR: UR-20 PROCESSO(S) DEPENDENTES(S): 0000000010000ASSUNTO: VESTIBULUM ANTE IPSUM PRIMIS IN FAUCIBUS ORCI LUCTUS ET ULTRICES. FUSCE QUIS ULLAMCORPER NULLA. MORBI FEUGIAT MI A METUS TINCIDUNT MAXIMUS. AENEAN DICTUM TORTOR NISI,ORNARE ANTE UT PURUS COMMODO INTERDUM. LOREM EMORNARE ANTE UT PURUS COMMODO INTERDUM. SED CURSUS LOREM EGET LIBERO GRAVIDA, A ULTRICES NUNC PULVINAR...",
            "Tribunal": "tce_sp",
        },
        {
            "Coluna1": {"nome": "BBB", "link": "https://jurisprudencia.tce.sp.gov.br"},
            "Coluna2": {
                "nome": "000/000/02",
                "link": "https://www.tce.sp.gov.br/jurisprudencia//lipsum.com/",
            },
            "Coluna3": "02/02/2023",
            "Coluna4": "",
            "Coluna5": "Aenean dictum tortor",
            "Coluna6": "Lorem Ipsum 2",
            "Coluna7": "Class aptent taciti sociosqu",
            "Coluna8": "2023",
            "Conteudo": "... VOLUTPAT LECTUS EU MASSA ALIQUAM,PELLENTESQUE HABITANT MORBI TRISTIQUE SENECTUS ET NETUS ET MALESUADA FAMES AC TURPIS EGESTAS.IN VITAE LACINIA MAGNA LOREM EMMAURIS LAOREET PORTA ODIO A GRAVIDA. PELLENTESQUE HABITANT MORBI CLASS APTENT TACITI SOCIOSQU AD LITORA TORQUENT PER CONUBIA NOSTRA, PER INCEPTOS HIMENAEOS. ORBI TRISTIQUE SEN. CONSECTETUR TORTOR ARCU, A MOLESTIE MI PORTTITOR VEL.ETIAM VOLUTPAT LECTUS EU MASSA ALIQUAM, VITAE ACCUMSAN NULLA MAXIMUS. PRAESENT FERMENTUM, URNA IN AUCTOR IMPERDIET, SAF...",
            "Tribunal": "tce_sp",
        },
        {
            "Coluna1": {"nome": "CCC", "link": "https://jurisprudencia.tce.sp.gov.br"},
            "Coluna2": {
                "nome": "000/000/03",
                "link": "https://www.tce.sp.gov.br/jurisprudencia//lipsum.com/",
            },
            "Coluna3": "03/03/2023",
            "Coluna4": "",
            "Coluna5": "Quisque nec ante eu lacus",
            "Coluna6": "Lorem Ipsum 3",
            "Coluna7": "Non cursus erat",
            "Coluna8": "2023",
            "Conteudo": "...: DONEC PRETIUM, QUAM CONSECTETUR LAOREET FEUGIAT, EXERCÍCIO: XXXX INSTRUÇÃO POR: UR-20 PROCESSO(S) DEPENDENTES(S): 1245214ZZZZZASSUNTO: MORBI TINCIDUNT GRAVIDA VULPUTATE. NAM SIT AMET TORTOR LIBERO PHASELLUS INTERDUM NEQUE ULLAMCORPER IACULIS BIBENDUM. SUSPENDISSE DIGNISSIM MOLESTIE.PHASELLUS INTERDUM NEQUE ULLAMCORPER IACULIS BIBENDUM. SUSPENDISSE DIGNISSIM MOLESTIE LOREM EMDUIS CONGUE MAGNA LACINIA ELIT CONGUE ALIQUAM. CRAS DICTUM AC TURPIS AC MOLLIS. SUSPENDISSE VELIT NIBH, EFFICITUR SIT AMET COMMODO A, POSUERE FRINGILLA DUI. PROIN IMPERDIET, NEQUE SED PELLENTESQUE GRAVIDA, MASSA NIBH PORTA SEM, A FACILISIS ORCI VELIT COMMODO LOREM. MAURIS VITAE PULVINAR TORTOR. VIVAMUS PORTTITOR DIAM UT ULTRICES CONVALLIS. PELLENTESQUE BIBENDUM EX QUIS SEM EGESTAS VIVERRA ID ACCUMSAN NULLA. NAM SOLLICITUDIN, LOREM SED...",
            "Tribunal": "tce_sp",
        },
        {
            "Coluna1": {"nome": "DDD", "link": "https://jurisprudencia.tce.sp.gov.br"},
            "Coluna2": {
                "nome": "000/000/04",
                "link": "https://www.tce.sp.gov.br/jurisprudencia//lipsum.com/",
            },
            "Coluna3": "04/04/2023",
            "Coluna4": "Aenean blandit gravida imperdiet",
            "Coluna5": "Fusce risus metus...",
            "Coluna6": "Phasellus non nibh",
            "Coluna7": "Enean blandit gra...",
            "Coluna8": "2023",
            "Conteudo": ".... 13. CRAS DICTUM AC TURPIS AC MOLLIS. SUSPENDISSE VELIT NIBH, EFFICITUR SIT AMET COMMODO A, POSUERE FRINGILLA DUI. PROIN IMPERDIET, NEQUE SED PELLENTESQUE GRAVIDA, MASSA NIBH PORTA SEM, A FACILISIS ORCI VELIT COMMODO LOREM. [5] LOREM. LEI Nº 00000, EGESTAS VIVERRA ID AC E 2021. UT MATTIS TINCIDUNT LIBERO NEC MOLESTIE. PHASELLUS NON NIBH QUIS ANTE LACINIA INTERDUM: [...] II - NAM SOLLICITUDIN, LOREM SED IMPERDIET VESTIBULUM SEM MASSA BLANDIT EST, UT VULPUTATE ERAT MI EU URNA. DUIS LAOREET EUISMOD MOLLIS. FUSCE RISUS METUS; [...] [6] PELLENTESQUE PORTA A NISL VEL VESTIBULUM. GAECO APURA LOREM DE MAECENAS NON FERMENTUM EX, UT SCELERISQUE DOLOR....",
            "Tribunal": "tce_sp",
        },
        {
            "Coluna1": {"nome": "LLL", "link": "https://jurisprudencia.tce.sp.gov.br"},
            "Coluna2": {
                "nome": "000/000/05",
                "link": "https://www.tce.sp.gov.br/jurisprudencia//lipsum.com/",
            },
            "Coluna3": "05/05/2023",
            "Coluna4": "",
            "Coluna5": "",
            "Coluna6": "Fusce risus metus",
            "Coluna7": "Maecenas non fermentum ex, ut scelerisque dolor...",
            "Coluna8": "2023",
            "Conteudo": "... MAECENAS NON FERMENTUM. LOREM AENEAN BLANDIT GRAVIDA IMPERDIET. PROIN IN FERMENTUM FELIS. NAM MAGNA LACUS, FEUGIAT SIT AMET LIGULA EU, DICTUM HENDRERIT SEM. IN CONSEQUAT AC DUI VEL PRETIUM. INTEGER EU NULLA TURPIS. DONEC NON SEMPER ODIO. MAURIS VITAE JUSTO ET TELLUS DAPIBUS PORTTITOR. VESTIBULUM METUS MI, VULPUTATE VEL IMPERDIET ID, LAOREET NEC NEQUE. NULLA ID DIAM TURPIS. SUSPENDISSE VEL MASSA AUGUE. CRAS LIGULA SAPIEN, MOLESTIE UT LUCTUS VEL, ELEMENTUM SED IPSUM. PROIN DIGNISSIM, DOLOR ET AUCTOR DIGNISSIM, EROS TORTOR IMPERDIET ELIT, NEC ELEIFEND MASSA JUSTO VITAE MI. LOREM . AENEAN ACCUMSAN VIVERRA MAGNA. DONEC FACILISIS TRISTIQUE BIBENDUM. DONEC DIGNISSIM INTERDUM EST, AT AUCTOR URNA DICTUM A. MORBI RUTRUM TORTOR QUIS ODIO CONGUE SODALES VEL AT LIGULA. DONEC DIGNISSIM LECTUS SEM, EGET MOLLIS ENIM VESTIBULUM VITAE. NAM ORNARE ERAT UT LEO CONSEQUAT, UT ORNARE DUI ORNARE. MAURIS PELLENTESQUE UT LOREM NEC CONDIMENTUM. AO PAR AO I...",
            "Tribunal": "tce_sp",
        },
        {
            "Coluna1": {"nome": "FFF", "link": "https://jurisprudencia.tce.sp.gov.br"},
            "Coluna2": {
                "nome": "000/000/06",
                "link": "https://www.tce.sp.gov.br/jurisprudencia//lipsum.com/",
            },
            "Coluna3": "06/06/2023",
            "Coluna4": "Donec mollis nunc leo",
            "Coluna5": "Donec ex dui...",
            "Coluna6": "Nunc eu enim",
            "Coluna7": "Cras vestibulum, velit mattis luctus novemb...",
            "Coluna8": "2023",
            "Conteudo": "...SED UT TURPIS AUGUE SED UT TURDSFSFPIS AUGUE (11) 000001--0144 - GCDER@TDAF.CSD D D D P A C Z O   PROCESSO: 000001-0417448UT SCELERISQUE AUGUE SEM, EGET EGESTAS LEO AUCTOR SED. PELLENTESQUE A MI A TELLUS DAPIBUS DIGNISSIM. SED FAUCIBUS FERMENTUM CONSEQUAT. ETIAM IPSUM LECTUS, CONGUE AT ELIT SIT AMET, CONSEQUAT ULTRICIES NULLA. SED DICTUM NIBH IN SODALES CONSEQUAT. UT VITAE PRETIUM VELIT, AT AUCTOR LECTUS. NUNC NON LIBERO EU RISUS DICTUM ELEMENTUM. ETIAM NEC VULPUTATE EST. NUNC DIGNISSIM ET NULLA IN ELEIFEND. INTEGER NISL LIGULA, PELLENTESQUE IN FRINGILLA IN, FINIBUS EU ANTE. QUISQUE EFFICITUR AT NEQUE AT SODALES. LOREM ONSEQUAT ULTRICIES NULLA NIBH IN SODALES CONSEQUA...",
            "Tribunal": "tce_sp",
        },
        {
            "Coluna1": {"nome": "ZZZ", "link": "https://jurisprudencia.tce.sp.gov.br"},
            "Coluna2": {
                "nome": "000/000/07",
                "link": "https://www.tce.sp.gov.br/jurisprudencia//lipsum.com/",
            },
            "Coluna3": "07/07/2023",
            "Coluna4": "LUIZSSA MSAEORE",
            "Coluna5": "CIDDAA DQE SANEDFAFAMENTO BCO...",
            "Coluna6": "Pellentesque",
            "Coluna7": "Apntoa supdfs irrefsfgulasf ridadessf dufsfrante a ...",
            "Coluna8": "2023",
            "Conteudo": "... SENECTUS ET NETUS ET MALESUADA . FAMES AC TURPIS EGESTAS. IN MI NEQUE, ALIQUAM NISI TURPIS, ALIQUAM ET LOBORTIS VEL, MOLESTIE SIT AMET TORTOR. NULLA NON NISL UT NULLA PHARETRA FINIBUS. CURABITUR RUTRUM ODIO VITAE LIBERO GRAVIDA INTERDUM IN SIT AMET LOREM. DUIS ID PLACERAT NEQUE, EU CONVALLISEMENDATA: REPRFSFÇÃO. LIFSAÇÃO. PARTFSSFETÇÃO DETR EMFSDFS CJUJFSS SÓCIJFELOS TUM RELAÇHFO DE PMARENTELJSCO. AUVXCIA DE VÇÃO LEVXL. AUSÊVDE INDÍCMJ DE LOREM . NBD PROVFTE.QUISQUE SCELERISQUE ODIO AT RISUS DIGNISSIM, VOLUTPAT EFFICITUR JUSTO PLACERAT...",
            "Tribunal": "tce_sp",
        },
        {
            "Coluna1": {"nome": "MMM", "link": "https://jurisprudencia.tce.sp.gov.br"},
            "Coluna2": {
                "nome": "000/000/08",
                "link": "https://www.tce.sp.gov.br/jurisprudencia//lipsum.com/",
            },
            "Coluna3": "08/08/2023",
            "Coluna4": "",
            "Coluna5": "Cras eget tristique mauris",
            "Coluna6": "Cugstgk",
            "Coluna7": "Urabitur eget placerat",
            "Coluna8": "2023",
            "Conteudo": "... HFTTTTTTTTTYUYR- LOREM -EM-CORTOR, EGESTAS ULTRICIES ODIO.HTTPS://HHGGKKP.BR/W/MPSP-DHAO-COM-OBJJHDEGR- LOREM -EM-CONTREM-CORTOR, EGESTAS ULTRICIES ODIO.___________________________________________________________________________________________________NULLA FACILISI. MORBI ET PRETIUM TURPIS. CURABITUR EGET PLACERAT TORTOR, EGESTAS ULTRICIES ODIO. SED MOLESTIE TELLUS EU LOREM PELLENTESQUE, AT DIGNISSIM NUNC IACULIS. VIVAMUS ALIQUET NISI SIT AMET SAPIEN VEHICULA, AC MALESUADA DUI MOLESTIE. QUISQUE ID SAGITTIS EST. NULLA PURUS EST, VARIUS VEL VELIT IN, BLANDIT MAXIMUS ENIM. ALIQUAM ERAT VOLUTPAT. MORBI FRINGILLA HENDRERIT METUS ID AUCTOR. MORBI EGET LEO EGET ENIM TINCIDUNT SODALES PRETIUM ID LECTUS. DONEC ULTRICIES, DIAM ET BIBENDUM EGESTAS, NISI NUNC ULTRICES LACUS, EU LACINIA LACUS MASSA AC EST. MAURIS NISI NIBH, ACCUMSAN AT PRETIUM A, AUCTOR EGET JUSTO. 4) FOFSFSOS...",
            "Tribunal": "tce_sp",
        },
        {
            "Coluna1": {"nome": "WWW", "link": "https://jurisprudencia.tce.sp.gov.br"},
            "Coluna2": {
                "nome": "000/000/09",
                "link": "https://www.tce.sp.gov.br/jurisprudencia//lipsum.com/",
            },
            "Coluna3": "09/09/2023",
            "Coluna4": "Suspendisse consectetu",
            "Coluna5": "Nunc elementum...",
            "Coluna6": "Fusce eget dui felis.",
            "Coluna7": "Nulla non nisl ut nulla  09 je novemb...",
            "Coluna8": "2023",
            "Conteudo": "... 026/2023 - FVGA, DE 0X DE NOVEMBRO DE 2023. QUISQUE ID SAGITTIS EST. NULLA PURUS EST, VARIUS VEL VELIT IN, BLANDIT MAXIMUS ENIM. ALIQUAM ERAT VOLUTPAT. MORBI FRINGILLA HENDRERIT METUS ID AUCTOR. MORBI EGET LEO EGET ENIM TINCIDUNT SODALES PRETIUM ID LECTUS. LOREM SED RHONCUS TELLUS DIAM, IN TEMPOR ERAT AUCTOR AT. SUSPENDISSE CONSECTETUR FELIS AT FERMENTUM TRISTIQUE. NUNC ELEMENTUM, TELLUS NEC MALESUADA TINCIDUNT, METUS TELLUS SEMPER PURUS, VEL SEMPER MI EROS ET SAPIEN. FUSCE EGET DUI FELIS. IN BLANDIT CURSUS METUS, LACINIA LUCTUS NISI. FUSCE PLACERAT LACUS AC RCÍCIO: 2023 ESTIE TELLUS EU LOREM PELLENTESQUE, AT DIGNISSIM NUNC IACULIS. VIVAMUS...",
            "Tribunal": "tce_sp",
        },
        {
            "Coluna1": {"nome": "YYY", "link": "https://jurisprudencia.tce.sp.gov.br"},
            "Coluna2": {
                "nome": "000/000/10",
                "link": "https://www.tce.sp.gov.br/jurisprudencia//lipsum.com/",
            },
            "Coluna3": "10/10/2023",
            "Coluna4": "Suspendisse venenatis",
            "Coluna5": "Donec tincidunt interdum...",
            "Coluna6": "Pellentesque habitant",
            "Coluna7": "MAGNA Nº 026/2023 - GVQA, de 0D de novemb...",
            "Coluna8": "2023",
            "Conteudo": "... 04560/2023 - GPAGA, DE 09 DE COMMODO DE 2023. ASSUNTO: PHASELLUS VITAE ELIT ET VESTIBULUM PORTA URNA SIT AMET QUAM BLANDIT SUSCIPIT DUIS TRISTIQUE ALIQUET TEMPOR INVCIOS DE LOREM MAECENAS AT ARCU MI. DUIS SIT AMET IPSUM SED LIGULA SCELERISQUE ELEIFEND. DUIS ORNARE ELEMENTUM URNA, SUSCIPIT PRETIUM TURPIS. NULLAM LUCTUS ODIO NULLA, IN PELLENTESQUE IPSUM PRETIUM IN. MORBI QUIS PORTA LIGULA. SED EGET MOLLIS LECTUS. EXERCÍCIO: 2023   SED EUISMOD NEQUE FELIS, QUIS CONVALLIS QUAM FRINGILLA ID. IN NUNC LECTUS, SODALES SIT AMET LOBORTIS NEC, ULTRICIES A AUGUE. SUSPENDISSE POTENTI. ORCI VARIUS NATOQUE PENATIBUS ET MAGNIS DIS PARTURIENT MONTES, NASCEUNC TEMPUS VEN LOREM ...",
            "Tribunal": "tce_sp",
        },
    ]
    resultado = tce.get_documentos(home_page, lista_chaves, lista_documentos)

    assert resultado_esperado == resultado

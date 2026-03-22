from enum import Enum

class Secao(str, Enum):
    COMPACTO = "compacto"
    NAO_COMPACTO = "nao-compacto"
    ESBELTO = "esbelto"
    FORA_ESCOPO = "fora de escopo da norma"
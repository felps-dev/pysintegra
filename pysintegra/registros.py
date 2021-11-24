# from pysintegra.classes import Registro

from pysintegra.classes import FormatoN, FormatoX, Registro


class Registro10(Registro):
    tipo = FormatoN('Tipo do Registro', 2, None)
    descricao = FormatoX('Descrição do Registro', 10, None)

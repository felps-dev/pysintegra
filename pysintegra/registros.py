# from pysintegra.classes import Registro

from datetime import datetime
from pysintegra.classes import FormatoN, FormatoNData, FormatoX, Registro


class Registro10(Registro):
    tipo = FormatoN('Tipo 10', 2, '10', False)
    cnpj_mf = FormatoN('CNPJ do estabelecimento informante ', 14, None)
    ie = FormatoX('Inscrição estadual do estabelecimento informante', 14, None)
    nome_contribuinte = FormatoX('Nome do Contribuinte', 35, None)
    municipio = FormatoX('Município', 30, None)
    unidade_federacao = FormatoX('Unidade da Federação', 2, None)
    fax = FormatoN('Número do fax do estabelecimento informante', 10, None)
    data_inicial = FormatoNData(
        'A data do início do período referente às informações prestadas', 8, datetime.now())
    data_final = FormatoNData(
        'A data do início do período referente às informações prestadas', 8, datetime.now())
    cod_id_estrutura = FormatoX(
        'Código da identificação da estrutura do arquivo magnético entregue', 1, None)
    cod_id_natureza = FormatoX(
        'Código da identificação da natureza das operações informadas', 1, None)
    cod_id_finalidade = FormatoX(
        'Código da finalidade do arquivo magnético', 1, None)

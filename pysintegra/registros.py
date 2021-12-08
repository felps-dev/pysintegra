# from pysintegra.classes import Registro

from datetime import datetime
from pysintegra.classes import FormatoN, FormatoNData, FormatoNValor, FormatoX, Registro


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


class Registro11(Registro):
    tipo = FormatoN('Tipo 11', 2, '11', False)
    logradouro = FormatoX('Logradouro', 34, None)
    numero = FormatoN('Numero', 5, None)
    complemento = FormatoX('Complemento', 22, None)
    bairro = FormatoX('Bairro', 15, None)
    cep = FormatoN('Bairro', 8, None)
    nome_contato = FormatoX('Nome do Contato', 28, None)
    telefone = FormatoN('Telefone', 12, None)


class Registro50(Registro):
    tipo = FormatoN('Tipo 50', 2, '50', False)
    cnpj = FormatoN(
        'CNPJ do remetente nas entradas e do destinatário nas saídas', 14, None)
    ie = FormatoX(
        'Inscrição Estadual do remetente nas entradas e do destinatário nas saídas', 14, None)
    data = FormatoNData(
        'Data de emissão na saída ou de recebimento na entrada ', 8, datetime.now())
    unidade_federacao = FormatoX('Unidade da Federação', 2, None)
    modelo = FormatoN('Código do modelo da nota fiscal', 2, None)
    serie = FormatoX('Série da nota fiscal', 3, None)
    numero = FormatoN('Numero da nota fiscal', 6, None)
    cfop = FormatoN('Código Fiscal de Operação e Prestação', 4, None)
    emitente = FormatoX(
        'Emitente da Nota Fiscal (P-próprio/Tterceiros)', 1, None)
    valor_total = FormatoNValor(
        'Valor total da nota fiscal (com 2 decimais)', 13, None)
    bc_icms = FormatoNValor(
        'Base de Cálculo do ICMS (com 2 decimais)', 13, None)
    valor_icms = FormatoNValor(
        'Montante do imposto (com 2 decimais)', 13, None)
    isenta = FormatoNValor(
        'Valor amparado por isenção ou não incidência (com 2 decimais)', 13, None)
    outras = FormatoNValor(
        'Valor que não confira débito ou crédito do ICMS (com 2 decimais) ', 13, None)
    aliquota = FormatoNValor('Alíquota do ICMS (com 2 decimais)', 4, None)
    situacao = FormatoX('Situação da Nota Fiscal', 1, None)

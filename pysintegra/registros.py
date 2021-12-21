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


class Registro51(Registro):
    tipo = FormatoN('Tipo 51', 2, '51', False)
    cnpj = FormatoN(
        'CNPJ do remetente nas entradas e do destinatário nas saídas', 14, None)
    ie = FormatoX(
        'Inscrição Estadual do remetente nas entradas e do destinatário nas saídas', 14, None)
    data = FormatoNData(
        'Data de emissão na saída ou de recebimento na entrada ', 8, datetime.now())
    unidade_federacao = FormatoX('Unidade da Federação', 2, None)
    serie = FormatoX('Série da nota fiscal', 3, None)
    numero = FormatoN('Numero da nota fiscal', 6, None)
    cfop = FormatoN('Código Fiscal de Operação e Prestação', 4, None)
    valor_total = FormatoNValor(
        'Valor total da nota fiscal (com 2 decimais)', 13, None)
    valor_ipi = FormatoNValor(
        'Montante IPI da nota fiscal (com 2 decimais)', 13, None)
    isenta = FormatoNValor(
        'Valor amparado por isenção ou não incidência (com 2 decimais)', 13, None)
    outras = FormatoNValor(
        'Valor que não confira débito ou crédito do ICMS (com 2 decimais) ', 13, None)
    brancos = FormatoX('Brancos', 20, '', False)
    situacao = FormatoX('Situação da Nota Fiscal', 1, None)


class Registro53(Registro):
    tipo = FormatoN('Tipo 53', 2, '53', False)
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
    bc_icms = FormatoNValor(
        'Base de cálculo de retenção do ICMS (com 2 decimais)', 13, None)
    icms_retido = FormatoNValor(
        'ICMS retido pelo substituto (com 2 decimais) ', 13, None)
    desposa_acessorias = FormatoNValor(
        'Soma das despesas acessórias (frete, Seguro e outras - com 2 decimais) ', 13, None)
    situacao = FormatoX('Situação da Nota Fiscal', 1, None)
    brancos = FormatoX('Brancos', 30, '', False)


class Registro54(Registro):
    tipo = FormatoN('Tipo 54', 2, '54', False)
    cnpj = FormatoN(
        'CNPJ do remetente nas entradas e do destinatário nas saídas', 14, None)
    modelo = FormatoN('Código do modelo da nota fiscal', 2, None)
    serie = FormatoX('Série da nota fiscal', 3, None)
    numero = FormatoN('Numero da nota fiscal', 6, None)
    cfop = FormatoN('Código Fiscal de Operação e Prestação', 4, None)
    cst = FormatoN('Código da Situação Tributária', 3, None)
    item = FormatoN('Número de ordem do item na nota fiscal', 3, None)
    codigo = FormatoX(
        'Código do produto/mercadoria ou serviço do informante ', 14, None)
    quantidade = FormatoNValor(
        'Quantidade do produto/mercadoria(com 3 decimais)', 11, None, decimal_places=3)
    valor = FormatoNValor(
        'Valor bruto do produto/mercadoria (valor unitário multiplicado por quantidade) com 2 decimais ', 12, None)
    desconto = FormatoNValor(
        'Valor do desconto concedido no item (com 2 decimais).', 12, None)
    bc_icms = FormatoNValor(
        'Base de cálculo do ICMS (com 2 decimais)', 12, None)
    bc_icms_sbst = FormatoNValor(
        'Base de cálculo do ICMS de retenção na Substituição Tributária (com 2 decimais)', 12, None)
    valor_ipi = FormatoNValor(
        'Valor IPI (com 2 decimais)', 12, None)
    aliquota = FormatoNValor('Alíquota do ICMS (com 2 decimais)', 4, None)


class Registro55(Registro):
    tipo = FormatoN('Tipo 55', 2, '55', False)
    cnpj = FormatoN(
        'CNPJ do contribuinte substituto tributário', 14, None)
    ie = FormatoX(
        'Inscrição Estadual do contribuinte substituto tributário', 14, None)
    data = FormatoNData(
        'Data de GNRE', 8, datetime.now())
    unidade_federacao = FormatoX(
        'Unidade da Federação do contribuinte substituto tributário', 2, None)
    unidade_federacao_favorecida = FormatoX(
        'Unidade da Federação destino', 2, None)
    banco = FormatoN(
        'Código do banco onde foi efetuado o recolhimento', 3, None)
    agencia = FormatoN('Agência onde foi efetuado o recolhimento ', 4, None)
    numero = FormatoN(
        'Número de autenticação bancária do documento de arrecadação', 20, None)
    valor = FormatoNValor(
        'Valor GNRE (com 2 decimais)', 12, None)
    data_vencimento = FormatoNData(
        'Data do vencimento', 8, datetime.now())
    mes_ano_referencia = FormatoN(
        'Mês e ano referente à ocorrência do fato gerador, formato MMAAAA ', 6, None)
    convenio = FormatoX(
        'Número do Convênio ou Protocolo /Mercadoria', 30, None)


class Registro60M(Registro):
    tipo = FormatoN('Tipo 60', 2, '60', False)
    subtipo = FormatoN('Tipo M', 1, 'M', False)
    data = FormatoNData(
        'Data de emissão dos documentos', 8, datetime.now())
    serie = FormatoX('Série de fabricação do equipamento', 20, None)
    sequencia = FormatoN(
        'Número atribuído pelo estabelecimento ao equipamento', 3, None)
    modelo = FormatoX('Código do modelo do documento fiscal', 2, None)
    coo_inicio = FormatoN('COO do inicio do dia', 6, None)
    coo_fim = FormatoN('COO do fim do dia', 6, None)
    crz = FormatoN('Número do Contador de Redução Z(CRZ)', 6, None)
    cro = FormatoN(
        'Valor acumulado no Contador de Reinício de Operação (CRO)', 3, None)
    venda_bruta = FormatoN(
        'Valor venda Bruta', 16, None)
    totalizador = FormatoN(
        'Valor Totalizador geral', 16, None)
    brancos = FormatoX('Brancos', 37, '', False)


class Registro60A(Registro):
    tipo = FormatoN('Tipo 60', 2, '60', False)
    subtipo = FormatoN('Tipo A', 1, 'A', False)
    data = FormatoNData(
        'Data de emissão dos documentos', 8, datetime.now())
    serie = FormatoX('Série de fabricação do equipamento', 20, None)
    st_aliquota = FormatoX(
        'Identificador da Situação Tributária / Alíquota do ICMS', 4, None)
    bc_icms = FormatoNValor(
        'Valor acumulado no final do dia no totalizador parcial da situação tributária / alíquota indicada no campo 05 (com 2 decimais)', 12, None)
    brancos = FormatoX('Brancos', 79, '', False)


class Registro60I(Registro):
    tipo = FormatoN('Tipo 60', 2, '60', False)
    subtipo = FormatoN('Tipo I', 1, 'I', False)
    data = FormatoNData(
        'Data de emissão dos documentos', 8, datetime.now())
    modelo = FormatoX('Código do modelo do documento fiscal', 2, None)
    coo = FormatoN('COO', 6, None)
    item = FormatoN('Número de ordem do item na nota fiscal', 3, None)
    codigo = FormatoX(
        'Código do produto/mercadoria ou serviço do informante ', 14, None)
    quantidade = FormatoNValor(
        'Quantidade do produto/mercadoria(com 3 decimais)', 13, None, decimal_places=3)
    valor = FormatoNValor(
        'Valor bruto do produto/mercadoria (valor unitário multiplicado por quantidade) com 3 decimais ', 13, None)
    bc_icms = FormatoNValor(
        'Base de cálculo do ICMS (com 2 decimais)', 12, None)
    st_aliquota = FormatoX(
        'Identificador da Situação Tributária / Alíquota do ICMS', 4, None)
    valor_icms = FormatoNValor(
        'Montante do imposto (com 2 decimais)', 12, None)
    brancos = FormatoX('Brancos', 16, '', False)


class Registro61(Registro):
    tipo = FormatoN('Tipo 61', 2, '61', False)
    brancos = FormatoX('Brancos', 14, '', False)
    brancos = FormatoX('Brancos', 14, '', False)
    data = FormatoNData(
        'Data de emissão dos documentos', 8, datetime.now())
    modelo = FormatoX('Código do modelo do documento fiscal', 2, None)
    serie = FormatoX('Série do documento fiscal', 3, None)
    subserie = FormatoX('SubSérie do documento fiscal', 2, None)
    coo_inicio = FormatoN('COO do inicio do dia', 6, None)
    coo_fim = FormatoN('COO do fim do dia', 6, None)
    valor_total = FormatoNValor(
        'Valor Total', 13, None)
    bc_icms = FormatoNValor(
        'Base de cálculo do ICMS (com 2 decimais)', 13, None)
    valor_icms = FormatoNValor(
        'Montante do imposto (com 2 decimais)', 12, None)
    isenta = FormatoNValor(
        'Valor amparado por isenção ou não incidência (com 2 decimais)', 13, None)
    outras = FormatoNValor(
        'Valor que não confira débito ou crédito do ICMS (com 2 decimais) ', 13, None)
    aliquota = FormatoNValor('Alíquota do ICMS (com 2 decimais)', 4, None)
    brancos = FormatoX('Brancos', 1, '', False)


class Registro61R(Registro):
    tipo = FormatoN('Tipo 61', 2, '61', False)
    subtipo = FormatoN('Tipo R', 1, 'R', False)
    mes_ano = FormatoX('Mês e ano de emissão dos documentos fiscais', 6, None)
    codigo_produto = FormatoX('Código do produto do informante', 14, None)
    quantidade = FormatoNValor(
        'Quantidade do produto/mercadoria(com 3 decimais)', 13, None, decimal_places=3)
    valor_total = FormatoNValor(
        'Valor Total', 16, None)
    bc_icms = FormatoNValor(
        'Base de cálculo do ICMS (com 2 decimais)', 16, None)
    aliquota = FormatoNValor('Alíquota do ICMS (com 2 decimais)', 4, None)
    brancos = FormatoX('Brancos', 54, '', False)


class Registro70(Registro):
    tipo = FormatoN('Tipo 70', 2, '70', False)
    cnpj = FormatoN(
        'CNPJ do contribuinte substituto tributário', 14, None)
    ie = FormatoX(
        'Inscrição Estadual do contribuinte substituto tributário', 14, None)
    data = FormatoNData(
        'Data de GNRE', 8, datetime.now())
    unidade_federacao = FormatoX(
        'Unidade da Federação do contribuinte substituto tributário', 2, None)
    modelo = FormatoX('Código do modelo do documento fiscal', 2, None)
    serie = FormatoX('Série do documento fiscal', 3, None)
    subserie = FormatoX('SubSérie do documento fiscal', 2, None)
    numero = FormatoN('Numero da nota fiscal', 6, None)
    cfop = FormatoN('Código Fiscal de Operação e Prestação', 4, None)
    valor_total = FormatoNValor('Valor Total', 13, None)
    bc_icms = FormatoNValor(
        'Base de cálculo do ICMS (com 2 decimais)', 14, None)
    valor_icms = FormatoNValor(
        'Montante do imposto (com 2 decimais)', 14, None)
    isenta = FormatoNValor(
        'Valor amparado por isenção ou não incidência (com 2 decimais)', 14, None)
    outras = FormatoNValor(
        'Valor que não confira débito ou crédito do ICMS (com 2 decimais) ', 13, None)
    cif_fob = FormatoN('Modalidade do Frete', 2, None)
    situacao = FormatoX('Situação da Nota Fiscal', 1, None)


class Registro71(Registro):
    tipo = FormatoN('Tipo 71', 2, '71', False)
    cnpj = FormatoN(
        'CNPJ do tomador', 14, None)
    ie = FormatoX(
        'Inscrição Estadual do Tomador', 14, None)
    data = FormatoNData(
        'Data de Emissão', 8, datetime.now())
    unidade_federacao = FormatoX(
        'Unidade da Federação do contribuinte', 2, None)
    modelo = FormatoX('Código do modelo do documento fiscal', 2, None)
    serie = FormatoX('Série do documento fiscal', 3, None)
    subserie = FormatoX('SubSérie do documento fiscal', 2, None)
    numero = FormatoN('Numero da nota fiscal', 6, None)
    unidade_federacao = FormatoX(
        'Unidade da Federação do remetente', 2, None)
    cnpj = FormatoN(
        'CNPJ do remetente', 14, None)
    ie = FormatoX(
        'Inscrição Estadual do remetente', 14, None)
    data_nf = FormatoNData(
        'Data de Emissão da NF', 8, datetime.now())
    modelo = FormatoX('Código do modelo do documento fiscal', 2, None)
    serie = FormatoX('Série do documento fiscal', 3, None)
    numero = FormatoN('Numero da nota fiscal', 6, None)
    valor_total = FormatoNValor('Valor Total', 14, None)
    brancos = FormatoX('Brancos', 12, '', False)


class Registro74(Registro):
    tipo = FormatoN('Tipo 74', 2, '74', False)
    data = FormatoNData(
        'Data do inventário', 8, datetime.now())
    codigo = FormatoX(
        'Código do produto/mercadoria ou serviço do informante ', 14, None)
    quantidade = FormatoNValor(
        'Quantidade do produto/mercadoria(com 3 decimais)', 13, None, decimal_places=3)
    valor = FormatoNValor(
        'Valor Unitario do Produto com 2 decimais ', 13, None)
    posse = FormatoX('Código de Posse', 1, None)
    cnpj = FormatoN(
        'CNPJ do proprietário', 14, None)
    ie = FormatoX(
        'Inscrição Estadual do proprietário', 14, None)
    uf = FormatoX('UF Do proprietário', 2, None)
    brancos = FormatoX('Brancos', 45, '', False)


class Registro75(Registro):
    tipo = FormatoN('Tipo 75', 2, '75', False)
    data_inicial = FormatoNData(
        'Data Inicial', 8, datetime.now())
    data_final = FormatoNData(
        'Data Final', 8, datetime.now())
    codigo = FormatoX(
        'Código do produto/mercadoria ou serviço do informante ', 14, None)
    ncm = FormatoX('Codificação da Nomenclatura Comum do Mercosul', 8, None)
    descricao = FormatoX(
        'Descrição da mercadoria/produto ou serviço', 53, None)
    un_com = FormatoX('Unidade de Medida de Comercialização', 6, None)
    valor_ipi = FormatoNValor(
        'Valor IPI (com 2 decimais)', 5, None)
    valor_icms = FormatoNValor(
        'Valor ICMS (com 2 decimais)', 4, None)
    red_bc_icms = FormatoNValor(
        '% \de Redução na base de cálculo do ICMS, nas operações internas', 5, None)
    valor_bc_st = FormatoNValor(
        'Base de Cálculo do ICMS de substituição tributária (com 2 decimais', 13, None)


class Registro76(Registro):
    tipo = FormatoN('Tipo 76', 2, '76', False)
    cnpj = FormatoN(
        'CNPJ do tomador do serviço', 14, None)
    ie = FormatoX(
        'Inscrição Estadual do tomador do serviço', 14, None)
    modelo = FormatoX('Código do modelo do documento fiscal', 2, None)
    serie = FormatoX('Série do documento fiscal', 3, None)
    subserie = FormatoX('SubSérie do documento fiscal', 2, None)
    numero = FormatoN('Numero da nota fiscal', 6, None)
    cfop = FormatoN('Código Fiscal de Operação e Prestação', 4, None)
    tipo_receita = FormatoN(
        'Código da identificação do tipo de receita', 1, None)
    data = FormatoNData(
        'Data Final', 8, datetime.now())
    unidade_federacao = FormatoX(
        'Unidade da Federação', 2, None)
    valor_total = FormatoNValor('Valor Total', 13, None)
    bc_icms = FormatoNValor(
        'Base de Cálculo do ICMS (com 2 decimais)', 13, None)
    valor_icms = FormatoNValor(
        'Montante do imposto (com 2 decimais)', 12, None)
    isenta = FormatoNValor(
        'Valor amparado por isenção ou não incidência (com 2 decimais)', 12, None)
    outras = FormatoNValor(
        'Valor que não confira débito ou crédito do ICMS (com 2 decimais) ', 12, None)
    aliquota = FormatoNValor('Alíquota do ICMS (valor inteiro)', 2, None)
    situacao = FormatoX('Situação da Nota Fiscal', 1, None)


class Registro85(Registro):
    tipo = FormatoN('Tipo 85', 2, '85', False)
    exportacao = FormatoN('Nº da Declaração de Exportação', 11, None)
    data_declaracao = FormatoNData(
        'Data Declaração', 8, datetime.now())
    natureza = FormatoN(
        'Preencher com: “1” – Exportação Direta “2” - Exportação Indireta', 1, None)
    registro = FormatoN('Nº do registro de Exportação', 12, None)
    data_registro = FormatoNData(
        'Data Registro', 8, datetime.now())
    conhecimento = FormatoN('Nº do conhecimento de embarque', 12, None)
    data_conhecimento = FormatoNData(
        'Data Conhecimento de Embarque', 8, datetime.now())
    tipo_conhecimento = FormatoN(
        'Informação do tipo de conhecimento de transporte ', 2, None)
    pais = FormatoN('Código do país de destino da mercadoria', 4, None)
    reservado = FormatoN('Preencher com zeros', 8, None, False)
    data_conhecimento = FormatoNData(
        'Data da averbação da Declaração de exportação ', 8, datetime.now())
    nf_exportacao = FormatoN('Nº da nota fiscal de exportação', 6, None)
    data_emissao = FormatoNData(
        'Data Conhecimento de Embarque', 8, datetime.now())
    modelo = FormatoX('Código do modelo do documento fiscal', 2, None)
    serie = FormatoX('Série do documento fiscal', 3, None)
    brancos = FormatoX('Brancos', 19, '', False)


class Registro86(Registro):
    tipo = FormatoN('Tipo 86', 2, '86', False)
    registro = FormatoN('Nº do registro de Exportação', 12, None)
    data_registro = FormatoNData(
        'Data Registro', 8, datetime.now())
    cnpj = FormatoN(
        'CNPJ do tomador do serviço', 14, None)
    ie = FormatoX(
        'Inscrição Estadual do tomador do serviço', 14, None)
    unidade_federacao = FormatoX(
        'Unidade da Federação', 2, None)
    numero = FormatoN('Numero da nota fiscal', 6, None)
    data_emissao = FormatoNData(
        'Data Emissão', 8, datetime.now())
    modelo = FormatoX('Código do modelo do documento fiscal', 2, None)
    serie = FormatoX('Série do documento fiscal', 3, None)
    codigo = FormatoX(
        'Código do produto/mercadoria ou serviço do informante ', 14, None)
    quantidade = FormatoNValor(
        'Quantidade do produto/mercadoria(com 3 decimais)', 13, None, decimal_places=3)
    valor = FormatoNValor(
        'Valor Unitario do Produto com 2 decimais ', 13, None)
    relacionamento = FormatoN(
        'Preencher conforme tabela de códigosde relacionamento entre registro deexportação e nota fiscal de remessacom fim específico', 1, None)
    brancos = FormatoX('Brancos', 5, '', False)


class Registro90(Registro):
    tipo = FormatoN('Tipo 90', 2, '90', False)
    cnpj = FormatoN(
        'CNPJ do informante', 14, None)
    ie = FormatoX(
        'Inscrição Estadual do informante', 14, None)
    tipo_totalizado = FormatoN(
        'Tipo de registro que será totalizado pelo próximo campo ', 2, None)
    total = FormatoN(
        'Total de registros do tipo informado no campo anterior', 8, None)
    numero = FormatoN('Número de registros tipo 90', 1, None)

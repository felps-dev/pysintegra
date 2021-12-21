from datetime import datetime
from pysintegra.processamento import ArquivoMagnetico

arq = ArquivoMagnetico()
arq.add_registro_10('12345678910110', 'ISENTO', 'Nome do Contribuinte / Razao Social',
                    'Rio de Janeiro', 'RJ', 'ISENTO', datetime.now(), datetime.now(), '1', '1', '1')
arq.add_registro_74(datetime.now(), '1', 2.00, 2.00, 1,
                    '00000000000000', '              ', 'RJ')
arq.add_registro_75(
    datetime.now(),
    datetime.now(),
    '0000000000012',
    '00000000',
    'Produto Teste',
    'UN',
    0.0,  # Aliquota IPI (Não implementado)
    0.0,
    0.0,
    0.0  # BC ICMS ST ??????
)
# TESTE COM SUCESSO
print(arq.gerar())

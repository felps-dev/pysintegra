from datetime import datetime
from pysintegra.processamento import ArquivoMagnetico

arq = ArquivoMagnetico()
arq.add_registro_10('12345678910110', 'ISENTO', 'Nome do Contribuinte / Razao Social',
                    'Rio de Janeiro', 'RJ', 'ISENTO', datetime.now(), datetime.now(), '1', '1', '1')
arq.add_registro_90('12345678910110', 'ISENTO', '54', '1', '1')
# TESTE COM SUCESSO
print(arq.gerar())

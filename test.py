from datetime import datetime
from pysintegra.processamento import ArquivoMagnetico

arq = ArquivoMagnetico()
arq.add_registro_10(1234567891011, 'ISENTO', 'Nome do Contribuinte / Razao Social',
                    'Rio de Janeiro', 'RJ', 'ISENTO', datetime.now(), datetime.now(), '1', '1', '1')

# TESTE COM SUCESSO
print(arq.gerar())

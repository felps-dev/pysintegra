from pysintegra.processamento import ArquivoMagnetico

arq = ArquivoMagnetico()
arq.add_registro_10(2, 'Teste')

# TESTE COM SUCESSO
print(arq.registros[0].descricao.value)

# TESTE COM ERRO
arq.add_registro_10(322, 'Teste COM ERRO')

print(arq.registros[0].descricao.value)

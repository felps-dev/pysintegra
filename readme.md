# pysintegra é uma lib simples com o objetivo de facilitar a geração do arquivo SINTEGRA seguindo o Convênio ICMS 57/95.

## Com o surgimento do SPED, muitos estados não utilizam mais este formato, confira se a UF de destino realmente exige o SINTEGRA.

A lib teve frotes inspirações de arquitetura baseadas nessas:

- https://github.com/TadaSoftware/PyNFe
- https://github.com/sped-br/python-sped

Nenhuma dependência até o momento.

### Milestone

- [x] Criar estrutura inicial para gerar os registros
- [x] Fazer serialização dos registros
- [ ] Fazer processo reverso (Importação de um TXT)
- [ ] Automatizar algumas totalizações dos registros

### Registros finalizados

- [x] Registro 10
- [x] Registro 11
- [x] Registro 50
- [x] Registro 51
- [x] Registro 53
- [x] Registro 54
- [x] Registro 55
- [x] Registro 60M
- [x] Registro 60A
- [x] Registro 60I
- [x] Registro 61
- [x] Registro 61R
- [x] Registro 70
- [x] Registro 71
- [x] Registro 74
- [x] Registro 75
- [x] Registro 76
- [x] Registro 85
- [x] Registro 86
- [x] Registro 90

### Exemplo de uso

```python
from datetime import datetime
from pysintegra.processamento import ArquivoMagnetico

arq = ArquivoMagnetico()
arq.add_registro_10('12345678910110', 'ISENTO', 'Nome do Contribuinte / Razao Social',
                    'Rio de Janeiro', 'RJ', 'ISENTO', datetime.now(), datetime.now(), '1', '1', '1')
print(arq.gerar())
```

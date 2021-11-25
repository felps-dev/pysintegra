# pysintegra é uma lib simples com o objetivo de facilitar a geração do arquivo SINTEGRA seguindo o Convênio ICMS 57/95.

## Com o surgimento do SPED, muitos estados não utilizam mais este formato, confira se a UF de destino realmente exige o SINTEGRA.

### Milestone

- [x] Criar estrutura inicial para gerar os registros
- [x] Fazer serialização dos registros
- [ ] Fazer processo reverso (Importação de um TXT)
- [ ] Automatizar algumas totalizações dos registros

### Registros finalizados

- [x] Registro 10
- [ ] Registro 11
- [ ] Registro 50
- [ ] Registro 51
- [ ] Registro 53
- [ ] Registro 54
- [ ] Registro 55
- [ ] Registro 60M
- [ ] Registro 60A
- [ ] Registro 60l
- [ ] Registro 61
- [ ] Registro 70
- [ ] Registro 71
- [ ] Registro 74
- [ ] Registro 75
- [ ] Registro 76
- [ ] Registro 85
- [ ] Registro 86
- [ ] Registro 90

### Exemplo de uso

```python
from datetime import datetime
from pysintegra.processamento import ArquivoMagnetico

arq = ArquivoMagnetico()
arq.add_registro_10('1234567891011', 'ISENTO', 'Nome do Contribuinte / Razao Social',
                    'Rio de Janeiro', 'RJ', 'ISENTO', datetime.now(), datetime.now(), '1', '1', '1')
print(arq.gerar())
```

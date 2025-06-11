# PySintegra

[![Tests](https://github.com/felps-dev/pysintegra/actions/workflows/test.yml/badge.svg)](https://github.com/felps-dev/pysintegra/actions/workflows/test.yml)
[![Coverage](https://codecov.io/gh/felps-dev/pysintegra/branch/main/graph/badge.svg)](https://codecov.io/gh/felps-dev/pysintegra)
[![PyPI version](https://badge.fury.io/py/pysintegra.svg)](https://badge.fury.io/py/pysintegra)
[![Python versions](https://img.shields.io/pypi/pyversions/pysintegra.svg)](https://pypi.org/project/pysintegra/)

Uma biblioteca Python moderna para gerar e analisar arquivos magnéticos SINTEGRA com **suporte completo a todos os tipos de registro**, modelos Pydantic para validação robusta e segurança de tipos abrangente.

## 🚀 Novidades na v1.0.0

Esta versão principal traz **cobertura completa da especificação SINTEGRA** e modernização significativa:

### ✨ Novas Funcionalidades

- **🔧 Modelos Pydantic**: Reescrita completa usando Pydantic v2 para validação robusta e segurança de tipos
- **📋 Cobertura Completa de Registros**: Todos os 20+ tipos de registro SINTEGRA implementados
- **📖 Carregamento Reverso**: Analise arquivos SINTEGRA existentes de volta para modelos tipados
- **🎯 Segurança de Tipos**: Anotações de tipo completas e validação para todos os campos
- **📚 Documentação Rica**: Docstrings abrangentes e exemplos para cada tipo de registro
- **🧪 Testes Abrangentes**: 65+ testes unitários com 85% de cobertura
- **⚡ GitHub Actions**: Testes automatizados no Python 3.9-3.13
- **📦 Empacotamento Moderno**: Dependências e padrões de empacotamento atualizados

### 🔄 Migração da v0.8

A nova API é compatível com versões anteriores através de aliases, mas recomendamos migrar para a nova abordagem baseada em Pydantic:

```python
# Forma antiga (ainda funciona)
from pysintegra.processamento import ArquivoMagnetico

# Forma nova (recomendada)
from pysintegra import SintegraProcessor
```

## 📦 Instalação

```bash
pip install pysintegra
```

Para desenvolvimento:

```bash
pip install pysintegra[dev]
```

## 🚀 Início Rápido

### Uso Básico

```python
from datetime import date
from decimal import Decimal
from pysintegra import SintegraProcessor

# Criar um novo processador
processor = SintegraProcessor()

# Adicionar registro de estabelecimento (obrigatório)
processor.add_registro_10(
    cnpj_mf='12345678901234',
    ie='123456789',
    nome_contribuinte='Minha Empresa Ltda',
    municipio='São Paulo',
    unidade_federacao='SP',
    fax='1133334444',
    data_inicial=date(2024, 1, 1),
    data_final=date(2024, 12, 31),
    cod_id_estrutura='1',
    cod_id_natureza='1',
    cod_id_finalidade='1'
)

# Adicionar informações de endereço
processor.add_registro_11(
    logradouro='Av. Paulista',
    numero=1000,
    complemento='Sala 101',
    bairro='Bela Vista',
    cep='01310100',
    nome_contato='João Silva',
    telefone='11999887766'
)

# Adicionar registro de nota fiscal
processor.add_registro_50(
    cnpj='98765432109876',
    ie='987654321',
    data=date(2024, 1, 15),
    unidade_federacao='RJ',
    modelo=55,
    serie='001',
    numero=123456,
    cfop=5102,
    emitente='P',
    valor_total=Decimal('1000.00'),
    bc_icms=Decimal('1000.00'),
    valor_icms=Decimal('180.00'),
    isenta=Decimal('0.00'),
    outras=Decimal('0.00'),
    aliquota=Decimal('18.00'),
    situacao='N'
)

# Adicionar registro de estoque
processor.add_registro_74(
    data=date(2024, 12, 31),
    codigo='PROD001',
    quantidade=Decimal('100.500'),
    valor=Decimal('25.99'),
    posse='1',
    cnpj='12345678901234',
    ie='123456789',
    uf='SP'
)

# Gerar arquivo SINTEGRA
output = processor.generate_output()
print(output)

# Salvar em arquivo
processor.save_to_file('sintegra.txt')
```

### Analisando Arquivos Existentes

```python
from pysintegra import SintegraProcessor, Registro10, Registro50

# Analisar um arquivo SINTEGRA existente
processor = SintegraProcessor.parse_from_file('arquivo_existente.txt')

# Acessar registros analisados com segurança de tipos
for record in processor.records:
    if isinstance(record, Registro10):
        print(f"Empresa: {record.nome_contribuinte}")
        print(f"CNPJ: {record.cnpj_mf}")
    elif isinstance(record, Registro50):
        print(f"Nota Fiscal: {record.numero}, Valor: {record.valor_total}")
```

### Uso Direto de Modelos

```python
from datetime import date
from decimal import Decimal
from pydantic import ValidationError
from pysintegra import Registro10, Registro74

# Criar registros diretamente com validação
registro_10 = Registro10(
    cnpj_mf='12345678901234',
    ie='123456789',
    nome_contribuinte='Empresa Teste',
    municipio='São Paulo',
    unidade_federacao='SP',
    fax='1133334444',
    data_inicial=date(2024, 1, 1),
    data_final=date(2024, 12, 31),
    cod_id_estrutura='1',
    cod_id_natureza='1',
    cod_id_finalidade='1'
)

# Validação automática
try:
    registro_invalido = Registro10(
        cnpj_mf='inválido',  # Irá gerar ValidationError
        # ... outros campos
    )
except ValidationError as e:
    print(f"Erro de validação: {e}")

# Gerar linha SINTEGRA
linha = registro_10.to_sintegra_line()
```

## 📋 Suporte Completo a Tipos de Registro

PySintegra agora suporta **todos os tipos de registro SINTEGRA**:

### 🏢 Informações do Estabelecimento

- **Registro 10**: Registro mestre do estabelecimento (obrigatório)
- **Registro 11**: Dados complementares do estabelecimento (endereço, contato)

### 📄 Registros de Notas Fiscais e Documentos

- **Registro 50**: Totais de notas fiscais (modelos 1 e 1A) com informações de ICMS
- **Registro 51**: Notas fiscais de energia/utilidades (eletricidade, gás, água, comunicações)
- **Registro 53**: Registros de substituição tributária
- **Registro 54**: Detalhes de produtos/itens para notas fiscais

### 💰 Registros de Impostos e Pagamentos

- **Registro 55**: GNRE (Guia Nacional de Recolhimento de Tributos Estaduais)

### 🖨️ Equipamento Fiscal Eletrônico (ECF)

- **Registro 60M**: Registro mestre ECF (resumo diário)
- **Registro 60A**: Registros de alíquotas ECF
- **Registro 60I**: Registros de itens ECF

### 📊 Registros de Resumo

- **Registro 61**: Resumo mensal de documentos fiscais emitidos por ECF
- **Registro 61R**: Resumo mensal de itens ECF por produto

### 🚚 Serviços de Transporte

- **Registro 70**: Notas fiscais de serviços de comunicação e telecomunicação
- **Registro 71**: Notas fiscais de serviços de transporte
- **Registro 76**: Notas fiscais de serviços de comunicação (modelo 21/22)

### 📦 Estoque e Produtos

- **Registro 74**: Registros de estoque
- **Registro 75**: Códigos de produtos e serviços com informações tributárias

### 🌍 Operações de Exportação

- **Registro 85**: Informações de exportação
- **Registro 86**: Informações complementares de exportação

### 📈 Totalização

- **Registro 90**: Registros de totalização (gerados automaticamente)

## 🔧 Funcionalidades Avançadas

### Validação Abrangente

PySintegra fornece validação extensiva para todos os tipos de registro:

- **Formato CNPJ**: Garante que o CNPJ contenha apenas dígitos e tenha o comprimento correto
- **Validação UF**: Valida todos os códigos de estado brasileiros (AC, AL, AP, AM, BA, CE, DF, ES, GO, MA, MT, MS, MG, PA, PB, PR, PE, PI, RJ, RN, RS, RO, RR, SC, SP, SE, TO)
- **Faixas CFOP**: Garante que os códigos CFOP estejam dentro das faixas válidas (1000-9999)
- **Validação de Data**: Formato de data adequado e verificação de faixa
- **Precisão Decimal**: Manipulação automática de casas decimais para valores monetários
- **Comprimento de Campo**: Garante que todos os campos atendam às especificações SINTEGRA
- **Validação NCM**: Valida códigos NCM para classificação de produtos
- **Validação de Alíquota**: Garante que as alíquotas estejam dentro das faixas válidas

### Segurança de Tipos

Todos os modelos são totalmente tipados com Pydantic v2:

```python
from pysintegra import Registro75
from decimal import Decimal
from datetime import date

# Segurança de tipos completa e autocompletar
produto = Registro75(
    data_inicial=date(2024, 1, 1),
    data_final=date(2024, 12, 31),
    codigo="PROD001",
    ncm="12345678",
    descricao="Produto Premium",
    un_com="UN",
    valor_ipi=Decimal("5.00"),
    valor_icms=Decimal("18.00"),
    red_bc_icms=Decimal("0.00"),
    valor_bc_st=Decimal("0.00")
)
```

### Processamento em Lote

Processe múltiplos registros de forma eficiente:

```python
from pysintegra import SintegraProcessor
from datetime import date
from decimal import Decimal

processor = SintegraProcessor()

# Adicionar informações do estabelecimento
processor.add_registro_10(...)

# Adicionar produtos em lote
produtos = [
    ("PROD001", "Produto 1", "12345678"),
    ("PROD002", "Produto 2", "87654321"),
    ("PROD003", "Produto 3", "11223344"),
]

for codigo, descricao, ncm in produtos:
    processor.add_registro_75(
        data_inicial=date(2024, 1, 1),
        data_final=date(2024, 12, 31),
        codigo=codigo,
        ncm=ncm,
        descricao=descricao,
        un_com="UN",
        valor_ipi=Decimal("5.00"),
        valor_icms=Decimal("18.00"),
        red_bc_icms=Decimal("0.00"),
        valor_bc_st=Decimal("0.00")
    )

# Gerar arquivo com todos os registros
processor.save_to_file('sintegra_completo.txt')
```

## 📚 Exemplos

Confira o diretório `examples/` para exemplos de uso abrangentes:

- **`basic_usage.py`**: Geração simples de arquivo com registros essenciais
- **`parse_file.py`**: Demonstração de análise e validação de arquivo
- **`advanced_usage.py`**: Cenários complexos com múltiplos tipos de registro, demonstrações de validação e processamento em lote

## 🧪 Testes

Execute a suíte de testes abrangente:

```bash
# Instalar dependências de desenvolvimento
pip install -e .[dev]

# Executar todos os 65+ testes
pytest

# Executar testes com cobertura (85%+ de cobertura)
pytest --cov=pysintegra --cov-report=html

# Executar categorias específicas de teste
pytest tests/test_models.py  # Testar todos os modelos de registro
pytest tests/test_processor.py  # Testar funcionalidade do processador
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para enviar um Pull Request. Para mudanças importantes, abra primeiro uma issue para discutir o que você gostaria de alterar.

### Configuração de Desenvolvimento

```bash
# Clonar o repositório
git clone https://github.com/felps-dev/pysintegra.git
cd pysintegra

# Criar ambiente virtual
python -m venv env
source env/bin/activate  # No Windows: env\Scripts\activate

# Instalar em modo de desenvolvimento
pip install -e .[dev]

# Executar testes
pytest
```

### Adicionando Novos Tipos de Registro

A arquitetura facilita a adição de novos tipos de registro:

1. Criar um novo modelo Pydantic em `models.py`
2. Adicionar métodos de validação conforme necessário
3. Implementar método `to_sintegra_line()`
4. Adicionar método auxiliar ao `SintegraProcessor`
5. Adicionar testes abrangentes

## 📄 Licença

Este projeto está licenciado sob a GNU Lesser General Public License v3 (LGPLv3) - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🔗 Links

- [Pacote PyPI](https://pypi.org/project/pysintegra/)
- [Repositório GitHub](https://github.com/felps-dev/pysintegra)
- [Rastreador de Issues](https://github.com/felps-dev/pysintegra/issues)
- [Documentação Oficial SINTEGRA](http://www.sintegra.gov.br/)

## 📈 Changelog

### v1.0.0 (11 de Junho de 2025)

- **BREAKING**: Reescrita completa com modelos Pydantic
- **NOVO**: Cobertura completa de tipos de registro SINTEGRA (20+ tipos)
- **NOVO**: Carregamento reverso de arquivos SINTEGRA
- **NOVO**: Segurança de tipos e validação abrangentes
- **NOVO**: 65+ testes unitários com 85% de cobertura
- **NOVO**: Pipeline CI/CD GitHub Actions
- **NOVO**: Empacotamento Python moderno (suporta 3.9-3.13)
- **NOVO**: Todos os tipos de registro: 10, 11, 50, 51, 53, 54, 55, 60M, 60A, 60I, 61, 61R, 70, 71, 74, 75, 76, 85, 86, 90
- **MELHORADO**: Melhores mensagens de erro e validação
- **MELHORADO**: Documentação e exemplos abrangentes
- **MELHORADO**: Performance e eficiência de memória

### v0.8 (Anterior)

- Geração básica de arquivo SINTEGRA
- Abordagem manual baseada em classes
- Suporte limitado a tipos de registro
- Validação limitada

---

Feito com ❤️ por [Felipe Correa](https://github.com/felps-dev)

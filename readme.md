# PySintegra

[![Tests](https://github.com/felps-dev/pysintegra/actions/workflows/test.yml/badge.svg)](https://github.com/felps-dev/pysintegra/actions/workflows/test.yml)
[![Coverage](https://codecov.io/gh/felps-dev/pysintegra/branch/main/graph/badge.svg)](https://codecov.io/gh/felps-dev/pysintegra)
[![PyPI version](https://badge.fury.io/py/pysintegra.svg)](https://badge.fury.io/py/pysintegra)
[![Python versions](https://img.shields.io/pypi/pyversions/pysintegra.svg)](https://pypi.org/project/pysintegra/)

A modern Python library for generating and parsing SINTEGRA magnetic files with **complete registry type support**, Pydantic models for robust validation, and comprehensive type safety.

## 🚀 What's New in v1.0.0

This major release brings **complete SINTEGRA specification coverage** and significant modernization:

### ✨ New Features

- **🔧 Pydantic Models**: Complete rewrite using Pydantic v2 for robust validation and type safety
- **📋 Complete Registry Coverage**: All 20+ SINTEGRA registry types implemented
- **📖 Reverse Loading**: Parse existing SINTEGRA files back into typed models
- **🎯 Type Safety**: Full type annotations and validation for all fields
- **📚 Rich Documentation**: Comprehensive docstrings and examples for every registry type
- **🧪 Comprehensive Testing**: 65+ unit tests with 85% coverage
- **⚡ GitHub Actions**: Automated testing across Python 3.9-3.13
- **📦 Modern Packaging**: Updated dependencies and packaging standards

### 🔄 Migration from v0.8

The new API is backward compatible through aliases, but we recommend migrating to the new Pydantic-based approach:

```python
# Old way (still works)
from pysintegra.processamento import ArquivoMagnetico

# New way (recommended)
from pysintegra import SintegraProcessor
```

## 📦 Installation

```bash
pip install pysintegra
```

For development:

```bash
pip install pysintegra[dev]
```

## 🚀 Quick Start

### Basic Usage

```python
from datetime import date
from decimal import Decimal
from pysintegra import SintegraProcessor

# Create a new processor
processor = SintegraProcessor()

# Add establishment record (required)
processor.add_registro_10(
    cnpj_mf='12345678901234',
    ie='123456789',
    nome_contribuinte='My Company Ltd',
    municipio='São Paulo',
    unidade_federacao='SP',
    fax='1133334444',
    data_inicial=date(2024, 1, 1),
    data_final=date(2024, 12, 31),
    cod_id_estrutura='1',
    cod_id_natureza='1',
    cod_id_finalidade='1'
)

# Add address information
processor.add_registro_11(
    logradouro='Av. Paulista',
    numero=1000,
    complemento='Sala 101',
    bairro='Bela Vista',
    cep='01310100',
    nome_contato='João Silva',
    telefone='11999887766'
)

# Add invoice record
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

# Add inventory record
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

# Generate SINTEGRA file
output = processor.generate_output()
print(output)

# Save to file
processor.save_to_file('sintegra.txt')
```

### Parsing Existing Files

```python
from pysintegra import SintegraProcessor, Registro10, Registro50

# Parse an existing SINTEGRA file
processor = SintegraProcessor.parse_from_file('existing_file.txt')

# Access parsed records with type safety
for record in processor.records:
    if isinstance(record, Registro10):
        print(f"Company: {record.nome_contribuinte}")
        print(f"CNPJ: {record.cnpj_mf}")
    elif isinstance(record, Registro50):
        print(f"Invoice: {record.numero}, Value: {record.valor_total}")
```

### Direct Model Usage

```python
from datetime import date
from decimal import Decimal
from pydantic import ValidationError
from pysintegra import Registro10, Registro74

# Create records directly with validation
registro_10 = Registro10(
    cnpj_mf='12345678901234',
    ie='123456789',
    nome_contribuinte='Test Company',
    municipio='São Paulo',
    unidade_federacao='SP',
    fax='1133334444',
    data_inicial=date(2024, 1, 1),
    data_final=date(2024, 12, 31),
    cod_id_estrutura='1',
    cod_id_natureza='1',
    cod_id_finalidade='1'
)

# Automatic validation
try:
    invalid_record = Registro10(
        cnpj_mf='invalid',  # Will raise ValidationError
        # ... other fields
    )
except ValidationError as e:
    print(f"Validation error: {e}")

# Generate SINTEGRA line
line = registro_10.to_sintegra_line()
```

## 📋 Complete Registry Type Support

PySintegra now supports **all SINTEGRA registry types**:

### 🏢 Establishment Information

- **Registro 10**: Master establishment record (required)
- **Registro 11**: Complementary establishment data (address, contact)

### 📄 Invoice and Document Records

- **Registro 50**: Invoice totals (models 1 and 1A) with ICMS information
- **Registro 51**: Energy/utilities invoices (electricity, gas, water, communications)
- **Registro 53**: Tax substitution records
- **Registro 54**: Product/item details for invoices

### 💰 Tax and Payment Records

- **Registro 55**: GNRE (National Guide for State Tax Collection)

### 🖨️ Electronic Fiscal Equipment (ECF)

- **Registro 60M**: ECF master record (daily summary)
- **Registro 60A**: ECF tax rate records
- **Registro 60I**: ECF item records

### 📊 Summary Records

- **Registro 61**: Monthly summary of fiscal documents issued by ECF
- **Registro 61R**: Monthly summary of ECF items by product

### 🚚 Transportation Services

- **Registro 70**: Communication and telecommunication service invoices
- **Registro 71**: Transportation service invoices
- **Registro 76**: Communication service invoices (model 21/22)

### 📦 Inventory and Products

- **Registro 74**: Inventory records
- **Registro 75**: Product and service codes with tax information

### 🌍 Export Operations

- **Registro 85**: Export information
- **Registro 86**: Complementary export information

### 📈 Totalization

- **Registro 90**: Totalization records (auto-generated)

## 🔧 Advanced Features

### Comprehensive Validation

PySintegra provides extensive validation for all registry types:

- **CNPJ Format**: Ensures CNPJ contains only digits and has correct length
- **UF Validation**: Validates all Brazilian state codes (AC, AL, AP, AM, BA, CE, DF, ES, GO, MA, MT, MS, MG, PA, PB, PR, PE, PI, RJ, RN, RS, RO, RR, SC, SP, SE, TO)
- **CFOP Ranges**: Ensures CFOP codes are within valid ranges (1000-9999)
- **Date Validation**: Proper date format and range checking
- **Decimal Precision**: Automatic handling of decimal places for monetary values
- **Field Length**: Ensures all fields meet SINTEGRA specifications
- **NCM Validation**: Validates NCM codes for product classification
- **Tax Rate Validation**: Ensures tax rates are within valid ranges

### Type Safety

All models are fully typed with Pydantic v2:

```python
from pysintegra import Registro75
from decimal import Decimal
from datetime import date

# Full type safety and autocompletion
product = Registro75(
    data_inicial=date(2024, 1, 1),
    data_final=date(2024, 12, 31),
    codigo="PROD001",
    ncm="12345678",
    descricao="Premium Product",
    un_com="UN",
    valor_ipi=Decimal("5.00"),
    valor_icms=Decimal("18.00"),
    red_bc_icms=Decimal("0.00"),
    valor_bc_st=Decimal("0.00")
)
```

### Batch Processing

Process multiple records efficiently:

```python
from pysintegra import SintegraProcessor
from datetime import date
from decimal import Decimal

processor = SintegraProcessor()

# Add establishment info
processor.add_registro_10(...)

# Batch add products
products = [
    ("PROD001", "Product 1", "12345678"),
    ("PROD002", "Product 2", "87654321"),
    ("PROD003", "Product 3", "11223344"),
]

for codigo, descricao, ncm in products:
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

# Generate file with all records
processor.save_to_file('complete_sintegra.txt')
```

## 📚 Examples

Check out the `examples/` directory for comprehensive usage examples:

- **`basic_usage.py`**: Simple file generation with essential records
- **`parse_file.py`**: File parsing and validation demonstration
- **`advanced_usage.py`**: Complex scenarios with multiple record types, validation demos, and batch processing

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Install development dependencies
pip install -e .[dev]

# Run all 65+ tests
pytest

# Run tests with coverage (85%+ coverage)
pytest --cov=pysintegra --cov-report=html

# Run specific test categories
pytest tests/test_models.py  # Test all registry models
pytest tests/test_processor.py  # Test processor functionality
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/felps-dev/pysintegra.git
cd pysintegra

# Create virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install in development mode
pip install -e .[dev]

# Run tests
pytest
```

### Adding New Registry Types

The architecture makes it easy to add new registry types:

1. Create a new Pydantic model in `models.py`
2. Add validation methods as needed
3. Implement `to_sintegra_line()` method
4. Add helper method to `SintegraProcessor`
5. Add comprehensive tests

## 📄 License

This project is licensed under the GNU Lesser General Public License v3 (LGPLv3) - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [PyPI Package](https://pypi.org/project/pysintegra/)
- [GitHub Repository](https://github.com/felps-dev/pysintegra)
- [Issue Tracker](https://github.com/felps-dev/pysintegra/issues)
- [SINTEGRA Official Documentation](http://www.sintegra.gov.br/)

## 📈 Changelog

### v1.0.0 (June 11, 2025)

- **BREAKING**: Complete rewrite with Pydantic models
- **NEW**: Complete SINTEGRA registry type coverage (20+ types)
- **NEW**: Reverse loading from SINTEGRA files
- **NEW**: Comprehensive type safety and validation
- **NEW**: 65+ unit tests with 85% coverage
- **NEW**: GitHub Actions CI/CD pipeline
- **NEW**: Modern Python packaging (supports 3.9-3.13)
- **NEW**: All registry types: 10, 11, 50, 51, 53, 54, 55, 60M, 60A, 60I, 61, 61R, 70, 71, 74, 75, 76, 85, 86, 90
- **IMPROVED**: Better error messages and validation
- **IMPROVED**: Comprehensive documentation and examples
- **IMPROVED**: Performance and memory efficiency

### v0.8 (Previous)

- Basic SINTEGRA file generation
- Manual class-based approach
- Limited registry type support
- Limited validation

---

Made with ❤️ by [Felipe Correa](https://github.com/felps-dev)

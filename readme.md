# PySintegra

[![Tests](https://github.com/felps-dev/pysintegra/actions/workflows/test.yml/badge.svg)](https://github.com/felps-dev/pysintegra/actions/workflows/test.yml)
[![Coverage](https://codecov.io/gh/felps-dev/pysintegra/branch/main/graph/badge.svg)](https://codecov.io/gh/felps-dev/pysintegra)
[![PyPI version](https://badge.fury.io/py/pysintegra.svg)](https://badge.fury.io/py/pysintegra)
[![Python versions](https://img.shields.io/pypi/pyversions/pysintegra.svg)](https://pypi.org/project/pysintegra/)

A modern Python library for generating and parsing SINTEGRA magnetic files with Pydantic models for robust validation and type safety.

## 🚀 What's New in v1.0.0

This major release brings significant improvements and modernization:

### ✨ New Features

- **🔧 Pydantic Models**: Complete rewrite using Pydantic v2 for robust validation and type safety
- **📖 Reverse Loading**: Parse existing SINTEGRA files back into typed models
- **🎯 Type Safety**: Full type annotations and validation for all fields
- **📚 Rich Documentation**: Comprehensive docstrings and examples
- **🧪 Unit Tests**: Extensive test suite with 83% coverage
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

# Add inventory record
processor.add_registro_74(
    data=date(2024, 12, 31),
    codigo='PROD001',
    quantidade=100.5,
    valor=25.99,
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
from pysintegra import SintegraProcessor

# Parse an existing SINTEGRA file
processor = SintegraProcessor.parse_from_file('existing_file.txt')

# Access parsed records with type safety
for record in processor.records:
    if isinstance(record, Registro10):
        print(f"Company: {record.nome_contribuinte}")
        print(f"CNPJ: {record.cnpj_mf}")
```

### Direct Model Usage

```python
from datetime import date
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

## 📋 Supported Record Types

- **Registro 10**: Master establishment record
- **Registro 11**: Complementary establishment data
- **Registro 50**: Invoice totals (models 1 and 1A)
- **Registro 74**: Inventory records
- **Registro 75**: Product and service codes
- **Registro 90**: Totalization records (auto-generated)

More record types can be easily added following the same Pydantic pattern.

## 🔧 Validation Features

PySintegra provides comprehensive validation:

- **CNPJ Format**: Ensures CNPJ contains only digits and has correct length
- **UF Validation**: Validates Brazilian state codes
- **CFOP Ranges**: Ensures CFOP codes are within valid ranges
- **Date Validation**: Proper date format and range checking
- **Decimal Precision**: Automatic handling of decimal places for monetary values
- **Field Length**: Ensures all fields meet SINTEGRA specifications

## 📚 Examples

Check out the `examples/` directory for comprehensive usage examples:

- `basic_usage.py`: Simple file generation
- `parse_file.py`: File parsing and validation demonstration
- `advanced_usage.py`: Complex scenarios with multiple record types

## 🧪 Testing

Run the test suite:

```bash
# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Run tests with coverage
pytest --cov=pysintegra --cov-report=html
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

## 📄 License

This project is licensed under the GNU Lesser General Public License v3 (LGPLv3) - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [PyPI Package](https://pypi.org/project/pysintegra/)
- [GitHub Repository](https://github.com/felps-dev/pysintegra)
- [Issue Tracker](https://github.com/felps-dev/pysintegra/issues)

## 📈 Changelog

### v1.0.0 (2024-12-XX)

- **BREAKING**: Complete rewrite with Pydantic models
- **NEW**: Reverse loading from SINTEGRA files
- **NEW**: Comprehensive type safety and validation
- **NEW**: Unit tests with 83% coverage
- **NEW**: GitHub Actions CI/CD
- **NEW**: Modern Python packaging (supports 3.9-3.13)
- **IMPROVED**: Better error messages and validation
- **IMPROVED**: Documentation and examples

### v0.8 (Previous)

- Basic SINTEGRA file generation
- Manual class-based approach
- Limited validation

---

Made with ❤️ by [Felipe Correa](https://github.com/felps-dev)

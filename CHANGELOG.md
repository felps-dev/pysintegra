# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-06-11

### Added

- **Complete rewrite using Pydantic models** for type safety and validation
- **All SINTEGRA registry types** implemented:
  - Registro10, Registro11 (Company information)
  - Registro50, Registro51, Registro53, Registro54, Registro55 (Invoice records)
  - Registro60M, Registro60A, Registro60I (ECF records)
  - Registro61, Registro61R (ECF summaries)
  - Registro70, Registro71, Registro76 (Service records)
  - Registro74, Registro75 (Inventory and product records)
  - Registro85, Registro86 (Export records)
  - Registro90 (Totalization record)
- **Reverse loading functionality** - parse existing SINTEGRA files back to models
- **Comprehensive validation** with proper error messages
- **Type hints** throughout the codebase
- **Rich docstrings** explaining each record type's purpose
- **Unit tests** with pytest and coverage reporting
- **GitHub Actions** CI/CD pipeline with matrix testing
- **Examples directory** with practical usage demonstrations
- **Modern Python packaging** with proper dependencies

### Changed

- **Breaking**: Switched from manual classes to Pydantic models
- **Breaking**: New API with `SintegraProcessor` class
- **Breaking**: Field names now follow Python conventions
- Updated to require Python 3.9+
- Improved error handling and validation

### Deprecated

- Legacy `ArquivoMagnetico` class (maintained as alias for backward compatibility)
- Manual field classes (`FormatoN`, `FormatoX`, etc.)

### Removed

- `test.py` file (replaced with proper examples and unit tests)
- Manual validation logic (replaced with Pydantic validators)

### Fixed

- Field formatting issues
- Date handling improvements
- CNPJ and UF validation
- Proper decimal handling for monetary values

## [0.8] - Previous Release

### Added

- Basic SINTEGRA file generation
- Support for multiple record types (10, 11, 50, 51, 53, 54, 55, 60M, 60A, 60I, 61, 61R, 70, 71, 74, 75, 76, 85, 86, 90)
- Automatic totalization records (Type 90)
- Manual class-based validation

### Features

- Manual field validation
- Basic serialization to SINTEGRA format
- Simple API for adding records

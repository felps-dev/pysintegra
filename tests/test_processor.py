"""
Unit tests for PySintegra processor.
"""

import tempfile
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from pysintegra.models import Registro10, Registro74, Registro75
from pysintegra.processor import SintegraProcessor


class TestSintegraProcessor:
    """Tests for SintegraProcessor class."""

    def test_initialization(self):
        """Test processor initialization."""
        processor = SintegraProcessor()
        assert len(processor.records) == 0
        assert len(processor.get_record_counts()) == 0

    def test_add_record(self):
        """Test adding records directly."""
        processor = SintegraProcessor()

        record = Registro10(
            cnpj_mf="12345678901234",
            ie="123456789",
            nome_contribuinte="Test Company",
            municipio="São Paulo",
            unidade_federacao="SP",
            fax="1133334444",
            data_inicial=date(2024, 1, 1),
            data_final=date(2024, 12, 31),
            cod_id_estrutura="1",
            cod_id_natureza="1",
            cod_id_finalidade="1",
        )

        processor.add_record(record)
        assert len(processor.records) == 1
        assert processor.get_record_counts()["Registro10"] == 1

    def test_add_registro_10(self):
        """Test adding Registro 10 via helper method."""
        processor = SintegraProcessor()

        processor.add_registro_10(
            cnpj_mf="12345678901234",
            ie="123456789",
            nome_contribuinte="Test Company",
            municipio="São Paulo",
            unidade_federacao="SP",
            fax="1133334444",
            data_inicial=date(2024, 1, 1),
            data_final=date(2024, 12, 31),
            cod_id_estrutura="1",
            cod_id_natureza="1",
            cod_id_finalidade="1",
        )

        assert len(processor.records) == 1
        assert isinstance(processor.records[0], Registro10)
        assert processor.records[0].nome_contribuinte == "Test Company"

    def test_add_registro_74(self):
        """Test adding Registro 74 via helper method."""
        processor = SintegraProcessor()

        processor.add_registro_74(
            data=date(2024, 12, 31),
            codigo="PROD001",
            quantidade=100.5,
            valor=25.99,
            posse="1",
            cnpj="12345678901234",
            ie="123456789",
            uf="SP",
        )

        assert len(processor.records) == 1
        assert isinstance(processor.records[0], Registro74)
        assert processor.records[0].quantidade == Decimal("100.5")

    def test_add_registro_75(self):
        """Test adding Registro 75 via helper method."""
        processor = SintegraProcessor()

        processor.add_registro_75(
            data_inicial=date(2024, 1, 1),
            data_final=date(2024, 12, 31),
            codigo="PROD001",
            ncm="12345678",
            descricao="Test Product",
            un_com="UN",
            valor_ipi=5.0,
            valor_icms=18.0,
            red_bc_icms=0.0,
            valor_bc_st=0.0,
        )

        assert len(processor.records) == 1
        assert isinstance(processor.records[0], Registro75)
        assert processor.records[0].descricao == "Test Product"

    def test_generate_output_without_records(self):
        """Test that generating output without records raises error."""
        processor = SintegraProcessor()

        with pytest.raises(ValueError, match="No records added"):
            processor.generate_output()

    def test_generate_output_without_registro_10(self):
        """Test that generating output without Registro 10 raises error."""
        processor = SintegraProcessor()

        processor.add_registro_74(
            data=date(2024, 12, 31),
            codigo="PROD001",
            quantidade=100.5,
            valor=25.99,
            posse="1",
            cnpj="12345678901234",
            ie="123456789",
            uf="SP",
        )

        with pytest.raises(ValueError, match="Registro 10 is required"):
            processor.generate_output()

    def test_generate_output_complete(self):
        """Test complete output generation."""
        processor = SintegraProcessor()

        # Add required Registro 10
        processor.add_registro_10(
            cnpj_mf="12345678901234",
            ie="123456789",
            nome_contribuinte="Test Company",
            municipio="São Paulo",
            unidade_federacao="SP",
            fax="1133334444",
            data_inicial=date(2024, 1, 1),
            data_final=date(2024, 12, 31),
            cod_id_estrutura="1",
            cod_id_natureza="1",
            cod_id_finalidade="1",
        )

        # Add other records
        processor.add_registro_74(
            data=date(2024, 12, 31),
            codigo="PROD001",
            quantidade=100.5,
            valor=25.99,
            posse="1",
            cnpj="12345678901234",
            ie="123456789",
            uf="SP",
        )

        output = processor.generate_output()
        lines = output.strip().split("\r\n")

        # Should have original records + Registro 90
        assert len(lines) == 3
        assert lines[0].startswith("10")
        assert lines[1].startswith("74")
        assert lines[2].startswith("90")  # Totalization record

    def test_save_and_load_file(self):
        """Test saving to file and loading back."""
        processor = SintegraProcessor()

        # Add records
        processor.add_registro_10(
            cnpj_mf="12345678901234",
            ie="123456789",
            nome_contribuinte="Test Company",
            municipio="São Paulo",
            unidade_federacao="SP",
            fax="1133334444",
            data_inicial=date(2024, 1, 1),
            data_final=date(2024, 12, 31),
            cod_id_estrutura="1",
            cod_id_natureza="1",
            cod_id_finalidade="1",
        )

        processor.add_registro_75(
            data_inicial=date(2024, 1, 1),
            data_final=date(2024, 12, 31),
            codigo="PROD001",
            ncm="12345678",
            descricao="Test Product",
            un_com="UN",
            valor_ipi=5.0,
            valor_icms=18.0,
            red_bc_icms=0.0,
            valor_bc_st=0.0,
        )

        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            temp_path = f.name

        try:
            processor.save_to_file(temp_path)

            # Verify file exists and has content
            assert Path(temp_path).exists()
            content = Path(temp_path).read_text(encoding="latin-1")
            assert len(content) > 0
            assert content.startswith("10")

            # Parse back
            parsed_processor = SintegraProcessor.parse_from_file(temp_path)

            # Should have parsed the main records (excluding Registro 90)
            assert len(parsed_processor.records) >= 2

            # Check that we have the expected record types
            record_types = [type(r).__name__ for r in parsed_processor.records]
            assert "Registro10" in record_types
            assert "Registro75" in record_types

        finally:
            # Clean up
            Path(temp_path).unlink(missing_ok=True)

    def test_parse_date(self):
        """Test date parsing utility."""
        result = SintegraProcessor._parse_date("20240615")
        assert result == date(2024, 6, 15)

        with pytest.raises(ValueError):
            SintegraProcessor._parse_date("invalid")

    def test_parse_decimal(self):
        """Test decimal parsing utility."""
        # Test with 2 decimal places
        result = SintegraProcessor._parse_decimal("12345", 2)
        assert result == Decimal("123.45")

        # Test with 3 decimal places
        result = SintegraProcessor._parse_decimal("12345", 3)
        assert result == Decimal("12.345")

        # Test with no decimal places
        result = SintegraProcessor._parse_decimal("12345", 0)
        assert result == Decimal("12345")

        # Test empty string
        result = SintegraProcessor._parse_decimal("", 2)
        assert result == Decimal("0")

        # Test short number
        result = SintegraProcessor._parse_decimal("45", 2)
        assert result == Decimal("0.45")

    def test_clear_records(self):
        """Test clearing all records."""
        processor = SintegraProcessor()

        processor.add_registro_10(
            cnpj_mf="12345678901234",
            ie="123456789",
            nome_contribuinte="Test Company",
            municipio="São Paulo",
            unidade_federacao="SP",
            fax="1133334444",
            data_inicial=date(2024, 1, 1),
            data_final=date(2024, 12, 31),
            cod_id_estrutura="1",
            cod_id_natureza="1",
            cod_id_finalidade="1",
        )

        assert len(processor.records) == 1

        processor.clear_records()
        assert len(processor.records) == 0
        assert len(processor.get_record_counts()) == 0

    def test_record_counts(self):
        """Test record counting functionality."""
        processor = SintegraProcessor()

        # Add multiple records of different types
        processor.add_registro_10(
            cnpj_mf="12345678901234",
            ie="123456789",
            nome_contribuinte="Test Company",
            municipio="São Paulo",
            unidade_federacao="SP",
            fax="1133334444",
            data_inicial=date(2024, 1, 1),
            data_final=date(2024, 12, 31),
            cod_id_estrutura="1",
            cod_id_natureza="1",
            cod_id_finalidade="1",
        )

        # Add two Registro 74 records
        for i in range(2):
            processor.add_registro_74(
                data=date(2024, 12, 31),
                codigo=f"PROD00{i + 1}",
                quantidade=100.5,
                valor=25.99,
                posse="1",
                cnpj="12345678901234",
                ie="123456789",
                uf="SP",
            )

        counts = processor.get_record_counts()
        assert counts["Registro10"] == 1
        assert counts["Registro74"] == 2

    def test_backward_compatibility_alias(self):
        """Test that ArquivoMagnetico alias works."""
        from pysintegra.processor import ArquivoMagnetico

        # Should be the same class
        assert ArquivoMagnetico is SintegraProcessor

        # Should work the same way
        arq = ArquivoMagnetico()
        assert isinstance(arq, SintegraProcessor)

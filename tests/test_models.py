"""
Unit tests for PySintegra Pydantic models.
"""

from datetime import date
from decimal import Decimal

import pytest
from pydantic import ValidationError

from pysintegra.models import (
    BaseRecord,
    Registro10,
    Registro11,
    Registro50,
    Registro74,
    Registro75,
    Registro90,
)


class TestRegistro10:
    """Tests for Registro10 model."""

    def test_valid_registro10(self):
        """Test creating a valid Registro10."""
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

        assert record.cnpj_mf == "12345678901234"
        assert record.nome_contribuinte == "Test Company"
        assert record.unidade_federacao == "SP"

    def test_invalid_cnpj(self):
        """Test validation of invalid CNPJ."""
        with pytest.raises(ValidationError) as exc_info:
            Registro10(
                cnpj_mf="invalid_cnpj",
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

        # Check for either length validation or digit validation
        error_str = str(exc_info.value)
        assert (
            "String should have at least 14 characters" in error_str
            or "CNPJ must contain only digits" in error_str
        )

    def test_invalid_uf(self):
        """Test validation of invalid UF."""
        with pytest.raises(ValidationError) as exc_info:
            Registro10(
                cnpj_mf="12345678901234",
                ie="123456789",
                nome_contribuinte="Test Company",
                municipio="São Paulo",
                unidade_federacao="XX",  # Invalid UF
                fax="1133334444",
                data_inicial=date(2024, 1, 1),
                data_final=date(2024, 12, 31),
                cod_id_estrutura="1",
                cod_id_natureza="1",
                cod_id_finalidade="1",
            )

        assert "Invalid UF" in str(exc_info.value)

    def test_uf_case_normalization(self):
        """Test that UF is normalized to uppercase."""
        record = Registro10(
            cnpj_mf="12345678901234",
            ie="123456789",
            nome_contribuinte="Test Company",
            municipio="São Paulo",
            unidade_federacao="sp",  # lowercase
            fax="1133334444",
            data_inicial=date(2024, 1, 1),
            data_final=date(2024, 12, 31),
            cod_id_estrutura="1",
            cod_id_natureza="1",
            cod_id_finalidade="1",
        )

        assert record.unidade_federacao == "SP"

    def test_to_sintegra_line(self):
        """Test SINTEGRA line generation."""
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

        line = record.to_sintegra_line()
        assert line.startswith("10")
        assert "12345678901234" in line
        assert "Test Company" in line
        assert len(line) == 126  # Expected length for Registro 10


class TestRegistro11:
    """Tests for Registro11 model."""

    def test_valid_registro11(self):
        """Test creating a valid Registro11."""
        record = Registro11(
            logradouro="Rua das Flores, 123",
            numero=123,
            complemento="Apto 45",
            bairro="Centro",
            cep="01234567",
            nome_contato="João Silva",
            telefone="11999887766",
        )

        assert record.logradouro == "Rua das Flores, 123"
        assert record.numero == 123
        assert record.cep == "01234567"

    def test_invalid_cep(self):
        """Test validation of invalid CEP."""
        with pytest.raises(ValidationError) as exc_info:
            Registro11(
                logradouro="Rua das Flores, 123",
                numero=123,
                complemento="Apto 45",
                bairro="Centro",
                cep="invalid_cep",
                nome_contato="João Silva",
                telefone="11999887766",
            )

        # Check for either length validation or digit validation
        error_str = str(exc_info.value)
        assert (
            "String should have at most 8 characters" in error_str
            or "CEP must contain only digits" in error_str
        )


class TestRegistro50:
    """Tests for Registro50 model."""

    def test_valid_registro50(self):
        """Test creating a valid Registro50."""
        record = Registro50(
            cnpj="12345678901234",
            ie="123456789",
            data=date(2024, 6, 15),
            unidade_federacao="SP",
            modelo=1,
            serie="001",
            numero=12345,
            cfop=5102,
            emitente="P",
            valor_total=Decimal("1000.00"),
            bc_icms=Decimal("800.00"),
            valor_icms=Decimal("144.00"),
            isenta=Decimal("0.00"),
            outras=Decimal("56.00"),
            aliquota=Decimal("18.00"),
            situacao="N",
        )

        assert record.cnpj == "12345678901234"
        assert record.cfop == 5102
        assert record.valor_total == Decimal("1000.00")
        assert record.emitente == "P"

    def test_invalid_cfop(self):
        """Test validation of invalid CFOP."""
        with pytest.raises(ValidationError) as exc_info:
            Registro50(
                cnpj="12345678901234",
                ie="123456789",
                data=date(2024, 6, 15),
                unidade_federacao="SP",
                modelo=1,
                serie="001",
                numero=12345,
                cfop=999,  # Invalid CFOP
                emitente="P",
                valor_total=Decimal("1000.00"),
                bc_icms=Decimal("800.00"),
                valor_icms=Decimal("144.00"),
                isenta=Decimal("0.00"),
                outras=Decimal("56.00"),
                aliquota=Decimal("18.00"),
                situacao="N",
            )

        assert "Input should be greater than or equal to 1000" in str(exc_info.value)

    def test_invalid_emitente(self):
        """Test validation of invalid emitente."""
        with pytest.raises(ValidationError) as exc_info:
            Registro50(
                cnpj="12345678901234",
                ie="123456789",
                data=date(2024, 6, 15),
                unidade_federacao="SP",
                modelo=1,
                serie="001",
                numero=12345,
                cfop=5102,
                emitente="X",  # Invalid emitente
                valor_total=Decimal("1000.00"),
                bc_icms=Decimal("800.00"),
                valor_icms=Decimal("144.00"),
                isenta=Decimal("0.00"),
                outras=Decimal("56.00"),
                aliquota=Decimal("18.00"),
                situacao="N",
            )

        assert "Input should be" in str(exc_info.value)


class TestRegistro74:
    """Tests for Registro74 model."""

    def test_valid_registro74(self):
        """Test creating a valid Registro74."""
        record = Registro74(
            data=date(2024, 12, 31),
            codigo="PROD001",
            quantidade=Decimal("100.500"),
            valor=Decimal("25.99"),
            posse="1",
            cnpj="12345678901234",
            ie="123456789",
            uf="SP",
        )

        assert record.codigo == "PROD001"
        assert record.quantidade == Decimal("100.500")
        assert record.valor == Decimal("25.99")

    def test_negative_values_rejected(self):
        """Test that negative values are rejected."""
        with pytest.raises(ValidationError):
            Registro74(
                data=date(2024, 12, 31),
                codigo="PROD001",
                quantidade=Decimal("-10.0"),  # Negative quantity
                valor=Decimal("25.99"),
                posse="1",
                cnpj="12345678901234",
                ie="123456789",
                uf="SP",
            )


class TestRegistro75:
    """Tests for Registro75 model."""

    def test_valid_registro75(self):
        """Test creating a valid Registro75."""
        record = Registro75(
            data_inicial=date(2024, 1, 1),
            data_final=date(2024, 12, 31),
            codigo="PROD001",
            ncm="12345678",
            descricao="Produto de Teste",
            un_com="UN",
            valor_ipi=Decimal("5.0"),
            valor_icms=Decimal("18.0"),
            red_bc_icms=Decimal("0.0"),
            valor_bc_st=Decimal("0.0"),
        )

        assert record.codigo == "PROD001"
        assert record.ncm == "12345678"
        assert record.descricao == "Produto de Teste"
        assert record.valor_icms == Decimal("18.0")

    def test_invalid_ncm_length(self):
        """Test validation of NCM length."""
        with pytest.raises(ValidationError):
            Registro75(
                data_inicial=date(2024, 1, 1),
                data_final=date(2024, 12, 31),
                codigo="PROD001",
                ncm="123",  # Too short
                descricao="Produto de Teste",
                un_com="UN",
                valor_ipi=Decimal("5.0"),
                valor_icms=Decimal("18.0"),
                red_bc_icms=Decimal("0.0"),
                valor_bc_st=Decimal("0.0"),
            )


class TestRegistro90:
    """Tests for Registro90 model."""

    def test_valid_registro90(self):
        """Test creating a valid Registro90."""
        record = Registro90(
            cnpj="12345678901234",
            ie="123456789",
            totalizacoes="10000000017400000175000000030000000190000001",
            numero=1,
        )

        assert record.cnpj == "12345678901234"
        assert record.numero == 1
        assert len(record.totalizacoes) <= 95


class TestBaseRecord:
    """Tests for BaseRecord functionality."""

    def test_format_numeric(self):
        """Test numeric formatting."""
        # Test integer formatting
        result = BaseRecord._format_numeric(123, 6)
        assert result == "000123"

        # Test decimal formatting
        result = BaseRecord._format_numeric(Decimal("123.45"), 8, 2)
        assert result == "00012345"

        # Test float formatting
        result = BaseRecord._format_numeric(123.45, 8, 2)
        assert result == "00012345"

    def test_format_text(self):
        """Test text formatting."""
        # Test normal text
        result = BaseRecord._format_text("Hello", 10)
        assert result == "Hello     "

        # Test text truncation
        result = BaseRecord._format_text("Very long text", 5)
        assert result == "Very "

    def test_format_date(self):
        """Test date formatting."""
        test_date = date(2024, 6, 15)
        result = BaseRecord._format_date(test_date)
        assert result == "20240615"

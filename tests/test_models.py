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
    Registro51,
    Registro53,
    Registro54,
    Registro55,
    Registro60A,
    Registro60I,
    Registro60M,
    Registro61,
    Registro61R,
    Registro70,
    Registro71,
    Registro74,
    Registro75,
    Registro76,
    Registro85,
    Registro86,
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


class TestRegistro51:
    """Tests for Registro51 model."""

    def test_valid_registro51(self):
        """Test creating a valid Registro51."""
        record = Registro51(
            cnpj="12345678901234",
            ie="123456789",
            data=date(2024, 1, 15),
            uf="SP",
            serie="001",
            numero=123456,
            cfop=5102,
            valor_total=Decimal("1000.00"),
            valor_ipi=Decimal("50.00"),
            isenta=Decimal("0.00"),
            outras=Decimal("0.00"),
            situacao="N",
        )
        assert record.cnpj == "12345678901234"
        assert record.valor_total == Decimal("1000.00")

    def test_to_sintegra_line(self):
        """Test SINTEGRA line generation."""
        record = Registro51(
            cnpj="12345678901234",
            ie="123456789",
            data=date(2024, 1, 15),
            uf="SP",
            serie="001",
            numero=123456,
            cfop=5102,
            valor_total=Decimal("1000.00"),
            valor_ipi=Decimal("50.00"),
            isenta=Decimal("0.00"),
            outras=Decimal("0.00"),
            situacao="N",
        )
        line = record.to_sintegra_line()
        assert line.startswith("51")
        assert "12345678901234" in line


class TestRegistro53:
    """Tests for Registro53 model."""

    def test_valid_registro53(self):
        """Test creating a valid Registro53."""
        record = Registro53(
            cnpj="12345678901234",
            ie="123456789",
            data=date(2024, 1, 15),
            uf="SP",
            modelo=55,
            serie="001",
            numero=123456,
            cfop=5102,
            emitente="P",
            bc_icms=Decimal("1000.00"),
            icms_retido=Decimal("180.00"),
            despesas_acessorias=Decimal("50.00"),
            situacao="N",
        )
        assert record.cnpj == "12345678901234"
        assert record.icms_retido == Decimal("180.00")


class TestRegistro54:
    """Tests for Registro54 model."""

    def test_valid_registro54(self):
        """Test creating a valid Registro54."""
        record = Registro54(
            cnpj="12345678901234",
            modelo=55,
            serie="001",
            numero=123456,
            cfop=5102,
            cst=0,
            item=1,
            codigo="PROD001",
            quantidade=Decimal("10.000"),
            valor=Decimal("100.00"),
            desconto=Decimal("5.00"),
            bc_icms=Decimal("95.00"),
            bc_icms_st=Decimal("0.00"),
            valor_ipi=Decimal("5.00"),
            aliquota=Decimal("18.00"),
        )
        assert record.codigo == "PROD001"
        assert record.quantidade == Decimal("10.000")


class TestRegistro55:
    """Tests for Registro55 model."""

    def test_valid_registro55(self):
        """Test creating a valid Registro55."""
        record = Registro55(
            cnpj="12345678901234",
            ie="123456789",
            data=date(2024, 1, 15),
            uf="SP",
            uf_favorecida="RJ",
            banco=341,
            agencia=1234,
            numero=123456789,
            valor=Decimal("1000.00"),
            data_vencimento=date(2024, 1, 30),
            mes_ano_referencia=202401,
            convenio="CONV001",
        )
        assert record.uf == "SP"
        assert record.uf_favorecida == "RJ"
        assert record.valor == Decimal("1000.00")


class TestRegistro60M:
    """Tests for Registro60M model."""

    def test_valid_registro60m(self):
        """Test creating a valid Registro60M."""
        record = Registro60M(
            data=date(2024, 1, 15),
            serie="ECF001",
            sequencia=1,
            modelo="2D",
            coo_inicio=1,
            coo_fim=100,
            crz=1,
            cro=1,
            venda_bruta=Decimal("10000.00"),
            totalizador=Decimal("10000.00"),
        )
        assert record.tipo == "60"
        assert record.subtipo == "M"
        assert record.serie == "ECF001"


class TestRegistro60A:
    """Tests for Registro60A model."""

    def test_valid_registro60a(self):
        """Test creating a valid Registro60A."""
        record = Registro60A(
            data=date(2024, 1, 15),
            serie="ECF001",
            st_aliquota="T18",
            bc_icms=Decimal("1000.00"),
        )
        assert record.tipo == "60"
        assert record.subtipo == "A"
        assert record.st_aliquota == "T18"


class TestRegistro60I:
    """Tests for Registro60I model."""

    def test_valid_registro60i(self):
        """Test creating a valid Registro60I."""
        record = Registro60I(
            data=date(2024, 1, 15),
            modelo="2D",
            coo=50,
            item=1,
            codigo="PROD001",
            quantidade=Decimal("2.000"),
            valor=Decimal("100.00"),
            bc_icms=Decimal("100.00"),
            st_aliquota="T18",
            valor_icms=Decimal("18.00"),
        )
        assert record.tipo == "60"
        assert record.subtipo == "I"
        assert record.codigo == "PROD001"


class TestRegistro61:
    """Tests for Registro61 model."""

    def test_valid_registro61(self):
        """Test creating a valid Registro61."""
        record = Registro61(
            data=date(2024, 1, 15),
            modelo="2D",
            serie="001",
            subserie="01",
            coo_inicio=1,
            coo_fim=100,
            valor_total=Decimal("10000.00"),
            bc_icms=Decimal("10000.00"),
            valor_icms=Decimal("1800.00"),
            isenta=Decimal("0.00"),
            outras=Decimal("0.00"),
            aliquota=Decimal("18.00"),
        )
        assert record.tipo == "61"
        assert record.valor_total == Decimal("10000.00")


class TestRegistro61R:
    """Tests for Registro61R model."""

    def test_valid_registro61r(self):
        """Test creating a valid Registro61R."""
        record = Registro61R(
            mes_ano="202401",
            codigo_produto="PROD001",
            quantidade=Decimal("100.000"),
            valor_total=Decimal("10000.00"),
            bc_icms=Decimal("10000.00"),
            aliquota=Decimal("18.00"),
        )
        assert record.tipo == "61"
        assert record.subtipo == "R"
        assert record.mes_ano == "202401"


class TestRegistro70:
    """Tests for Registro70 model."""

    def test_valid_registro70(self):
        """Test creating a valid Registro70."""
        record = Registro70(
            cnpj="12345678901234",
            ie="123456789",
            data=date(2024, 1, 15),
            uf="SP",
            modelo="21",
            serie="001",
            subserie="01",
            numero=123456,
            cfop=5102,
            valor_total=Decimal("1000.00"),
            bc_icms=Decimal("1000.00"),
            valor_icms=Decimal("180.00"),
            isenta=Decimal("0.00"),
            outras=Decimal("0.00"),
            cif_fob=1,
            situacao="N",
        )
        assert record.tipo == "70"
        assert record.modelo == "21"


class TestRegistro71:
    """Tests for Registro71 model."""

    def test_valid_registro71(self):
        """Test creating a valid Registro71."""
        record = Registro71(
            cnpj_tomador="12345678901234",
            ie_tomador="123456789",
            data=date(2024, 1, 15),
            uf_tomador="SP",
            modelo="08",
            serie="001",
            subserie="01",
            numero=123456,
            uf_remetente="RJ",
            cnpj_remetente="98765432109876",
            ie_remetente="987654321",
            data_nf=date(2024, 1, 14),
            modelo_nf="55",
            serie_nf="001",
            numero_nf=654321,
            valor_total=Decimal("1000.00"),
        )
        assert record.tipo == "71"
        assert record.uf_tomador == "SP"
        assert record.uf_remetente == "RJ"


class TestRegistro76:
    """Tests for Registro76 model."""

    def test_valid_registro76(self):
        """Test creating a valid Registro76."""
        record = Registro76(
            cnpj="12345678901234",
            ie="123456789",
            modelo="22",
            serie="001",
            subserie="01",
            numero=123456,
            cfop=5102,
            tipo_receita=1,
            data=date(2024, 1, 15),
            uf="SP",
            valor_total=Decimal("1000.00"),
            bc_icms=Decimal("1000.00"),
            valor_icms=Decimal("180.00"),
            isenta=Decimal("0.00"),
            outras=Decimal("0.00"),
            aliquota=18,
            situacao="N",
        )
        assert record.tipo == "76"
        assert record.aliquota == 18


class TestRegistro85:
    """Tests for Registro85 model."""

    def test_valid_registro85(self):
        """Test creating a valid Registro85."""
        record = Registro85(
            exportacao=123456789,
            data_declaracao=date(2024, 1, 15),
            natureza=1,
            registro=987654321,
            data_registro=date(2024, 1, 10),
            conhecimento=555666777,
            data_conhecimento=date(2024, 1, 20),
            tipo_conhecimento=1,
            pais=249,
            data_averbacao=date(2024, 1, 25),
            nf_exportacao=123456,
            data_emissao=date(2024, 1, 15),
            modelo="55",
            serie="001",
        )
        assert record.tipo == "85"
        assert record.natureza == 1
        assert record.pais == 249


class TestRegistro86:
    """Tests for Registro86 model."""

    def test_valid_registro86(self):
        """Test creating a valid Registro86."""
        record = Registro86(
            registro=987654321,
            data_registro=date(2024, 1, 10),
            cnpj="12345678901234",
            ie="123456789",
            uf="SP",
            numero=123456,
            data_emissao=date(2024, 1, 15),
            modelo="55",
            serie="001",
            codigo="PROD001",
            quantidade=Decimal("10.000"),
            valor=Decimal("100.00"),
            relacionamento=1,
        )
        assert record.tipo == "86"
        assert record.codigo == "PROD001"
        assert record.relacionamento == 1


class TestRegistro74:
    """Tests for Registro74 model."""

    def test_valid_registro74(self):
        """Test creating a valid Registro74."""
        record = Registro74(
            data=date(2024, 1, 31),
            codigo="PROD001",
            quantidade=Decimal("100.000"),
            valor=Decimal("25.99"),
            posse="1",
            cnpj="12345678901234",
            ie="123456789",
            uf="SP",
        )
        assert record.codigo == "PROD001"
        assert record.quantidade == Decimal("100.000")

    def test_negative_values_rejected(self):
        """Test that negative values are rejected."""
        with pytest.raises(ValidationError):
            Registro74(
                data=date(2024, 1, 31),
                codigo="PROD001",
                quantidade=Decimal("-1.000"),
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
            descricao="Test Product",
            un_com="UN",
            valor_ipi=Decimal("5.00"),
            valor_icms=Decimal("18.00"),
            red_bc_icms=Decimal("0.00"),
            valor_bc_st=Decimal("0.00"),
        )
        assert record.codigo == "PROD001"
        assert record.ncm == "12345678"

    def test_invalid_ncm_length(self):
        """Test NCM length validation."""
        with pytest.raises(ValidationError) as exc_info:
            Registro75(
                data_inicial=date(2024, 1, 1),
                data_final=date(2024, 12, 31),
                codigo="PROD001",
                ncm="123",
                descricao="Test Product",
                un_com="UN",
                valor_ipi=Decimal("5.00"),
                valor_icms=Decimal("18.00"),
                red_bc_icms=Decimal("0.00"),
                valor_bc_st=Decimal("0.00"),
            )
        assert "String should have at least 8 characters" in str(exc_info.value)


class TestRegistro90:
    """Tests for Registro90 model."""

    def test_valid_registro90(self):
        """Test creating a valid Registro90."""
        record = Registro90(
            cnpj="12345678901234",
            ie="123456789",
            totalizacoes="1" * 95,
            numero=1,
        )
        assert record.cnpj == "12345678901234"
        assert record.numero == 1


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

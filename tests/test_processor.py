"""Tests for pysintegra processor."""

import tempfile
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from pysintegra.models import (
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
)
from pysintegra.processor import SintegraProcessor


class TestSintegraProcessor:
    """Test SintegraProcessor functionality."""

    def test_initialization(self):
        """Test processor initialization."""
        processor = SintegraProcessor()
        assert len(processor.records) == 0

    def test_add_record(self):
        """Test adding a record directly."""
        processor = SintegraProcessor()
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
        processor.add_record(record)
        assert len(processor.records) == 1
        assert processor.records[0] == record

    def test_add_registro_10(self):
        """Test adding Registro 10."""
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

    def test_add_registro_11(self):
        """Test adding Registro 11."""
        processor = SintegraProcessor()
        processor.add_registro_11(
            logradouro="Rua das Flores",
            numero=123,
            complemento="Apto 45",
            bairro="Centro",
            cep="01234567",
            nome_contato="João Silva",
            telefone="11999887766",
        )
        assert len(processor.records) == 1
        assert isinstance(processor.records[0], Registro11)

    def test_add_registro_50(self):
        """Test adding Registro 50."""
        processor = SintegraProcessor()
        processor.add_registro_50(
            cnpj="12345678901234",
            ie="123456789",
            data=date(2024, 1, 15),
            unidade_federacao="SP",
            modelo=55,
            serie="001",
            numero=123456,
            cfop=5102,
            emitente="P",
            valor_total=Decimal("1000.00"),
            bc_icms=Decimal("1000.00"),
            valor_icms=Decimal("180.00"),
            isenta=Decimal("0.00"),
            outras=Decimal("0.00"),
            aliquota=Decimal("18.00"),
            situacao="N",
        )
        assert len(processor.records) == 1
        assert isinstance(processor.records[0], Registro50)

    def test_add_registro_51(self):
        """Test adding Registro 51."""
        processor = SintegraProcessor()
        processor.add_registro_51(
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
        assert len(processor.records) == 1
        assert isinstance(processor.records[0], Registro51)

    def test_add_registro_53(self):
        """Test adding Registro 53."""
        processor = SintegraProcessor()
        processor.add_registro_53(
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
        assert len(processor.records) == 1
        assert isinstance(processor.records[0], Registro53)

    def test_add_registro_54(self):
        """Test adding Registro 54."""
        processor = SintegraProcessor()
        processor.add_registro_54(
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
        assert len(processor.records) == 1
        assert isinstance(processor.records[0], Registro54)

    def test_add_registro_55(self):
        """Test adding Registro 55."""
        processor = SintegraProcessor()
        processor.add_registro_55(
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
        assert len(processor.records) == 1
        assert isinstance(processor.records[0], Registro55)

    def test_add_registro_60m(self):
        """Test adding Registro 60M."""
        processor = SintegraProcessor()
        processor.add_registro_60m(
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
        assert len(processor.records) == 1
        assert isinstance(processor.records[0], Registro60M)

    def test_add_registro_60a(self):
        """Test adding Registro 60A."""
        processor = SintegraProcessor()
        processor.add_registro_60a(
            data=date(2024, 1, 15),
            serie="ECF001",
            st_aliquota="T18",
            bc_icms=Decimal("1000.00"),
        )
        assert len(processor.records) == 1
        assert isinstance(processor.records[0], Registro60A)

    def test_add_registro_60i(self):
        """Test adding Registro 60I."""
        processor = SintegraProcessor()
        processor.add_registro_60i(
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
        assert len(processor.records) == 1
        assert isinstance(processor.records[0], Registro60I)

    def test_add_registro_61(self):
        """Test adding Registro 61."""
        processor = SintegraProcessor()
        processor.add_registro_61(
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
        assert len(processor.records) == 1
        assert isinstance(processor.records[0], Registro61)

    def test_add_registro_61r(self):
        """Test adding Registro 61R."""
        processor = SintegraProcessor()
        processor.add_registro_61r(
            mes_ano="202401",
            codigo_produto="PROD001",
            quantidade=Decimal("100.000"),
            valor_total=Decimal("10000.00"),
            bc_icms=Decimal("10000.00"),
            aliquota=Decimal("18.00"),
        )
        assert len(processor.records) == 1
        assert isinstance(processor.records[0], Registro61R)

    def test_add_registro_70(self):
        """Test adding Registro 70."""
        processor = SintegraProcessor()
        processor.add_registro_70(
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
        assert len(processor.records) == 1
        assert isinstance(processor.records[0], Registro70)

    def test_add_registro_71(self):
        """Test adding Registro 71."""
        processor = SintegraProcessor()
        processor.add_registro_71(
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
        assert len(processor.records) == 1
        assert isinstance(processor.records[0], Registro71)

    def test_add_registro_74(self):
        """Test adding Registro 74."""
        processor = SintegraProcessor()
        processor.add_registro_74(
            data=date(2024, 1, 31),
            codigo="PROD001",
            quantidade=Decimal("100.000"),
            valor=Decimal("25.99"),
            posse="1",
            cnpj="12345678901234",
            ie="123456789",
            uf="SP",
        )
        assert len(processor.records) == 1
        assert isinstance(processor.records[0], Registro74)

    def test_add_registro_75(self):
        """Test adding Registro 75."""
        processor = SintegraProcessor()
        processor.add_registro_75(
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
        assert len(processor.records) == 1
        assert isinstance(processor.records[0], Registro75)

    def test_add_registro_76(self):
        """Test adding Registro 76."""
        processor = SintegraProcessor()
        processor.add_registro_76(
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
        assert len(processor.records) == 1
        assert isinstance(processor.records[0], Registro76)

    def test_add_registro_85(self):
        """Test adding Registro 85."""
        processor = SintegraProcessor()
        processor.add_registro_85(
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
        assert len(processor.records) == 1
        assert isinstance(processor.records[0], Registro85)

    def test_add_registro_86(self):
        """Test adding Registro 86."""
        processor = SintegraProcessor()
        processor.add_registro_86(
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
        assert len(processor.records) == 1
        assert isinstance(processor.records[0], Registro86)

    def test_generate_output_without_records(self):
        """Test generating output without any records."""
        processor = SintegraProcessor()
        with pytest.raises(ValueError, match="No records added to generate output"):
            processor.generate_output()

    def test_generate_output_without_registro_10(self):
        """Test generating output without Registro 10."""
        processor = SintegraProcessor()
        processor.add_registro_74(
            data=date(2024, 1, 31),
            codigo="PROD001",
            quantidade=Decimal("100.000"),
            valor=Decimal("25.99"),
            posse="1",
            cnpj="12345678901234",
            ie="123456789",
            uf="SP",
        )
        with pytest.raises(
            ValueError, match="Registro 10 is required to generate totalization records"
        ):
            processor.generate_output()

    def test_generate_output_complete(self):
        """Test generating complete output."""
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

        # Add some other records
        processor.add_registro_75(
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

        output = processor.generate_output()
        lines = output.strip().split("\n")

        # Should have Registro 10, Registro 75, and auto-generated Registro 90
        assert len(lines) == 3
        assert lines[0].startswith("10")
        assert lines[1].startswith("75")
        assert lines[2].startswith("90")

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
            valor_ipi=Decimal("5.0"),
            valor_icms=Decimal("18.0"),
            red_bc_icms=Decimal("0.0"),
            valor_bc_st=Decimal("0.0"),
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

        finally:
            # Clean up
            Path(temp_path).unlink(missing_ok=True)

    def test_parse_date(self):
        """Test date parsing utility."""
        result = SintegraProcessor._parse_date("20240115")
        assert result == date(2024, 1, 15)

    def test_parse_decimal(self):
        """Test decimal parsing utility."""
        result = SintegraProcessor._parse_decimal("00012345", 2)
        assert result == Decimal("123.45")

    def test_clear_records(self):
        """Test clearing all records."""
        processor = SintegraProcessor()
        processor.add_registro_74(
            data=date(2024, 1, 31),
            codigo="PROD001",
            quantidade=Decimal("100.000"),
            valor=Decimal("25.99"),
            posse="1",
            cnpj="12345678901234",
            ie="123456789",
            uf="SP",
        )
        assert len(processor.records) == 1

        processor.clear_records()
        assert len(processor.records) == 0

    def test_record_counts(self):
        """Test record counting functionality."""
        processor = SintegraProcessor()

        # Add various records
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

        processor.add_registro_74(
            data=date(2024, 1, 31),
            codigo="PROD001",
            quantidade=Decimal("100.000"),
            valor=Decimal("25.99"),
            posse="1",
            cnpj="12345678901234",
            ie="123456789",
            uf="SP",
        )

        processor.add_registro_75(
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

        counts = processor.get_record_counts()
        assert counts["Registro10"] == 1
        assert counts["Registro74"] == 1
        assert counts["Registro75"] == 1

    def test_backward_compatibility_alias(self):
        """Test that ArquivoMagnetico alias works."""
        from pysintegra.processor import ArquivoMagnetico

        # Should be the same class
        assert ArquivoMagnetico is SintegraProcessor

        # Should work the same way
        processor = ArquivoMagnetico()
        assert isinstance(processor, SintegraProcessor)

    def test_multiple_registry_types_integration(self):
        """Test integration with multiple registry types."""
        processor = SintegraProcessor()

        # Add company info
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

        processor.add_registro_11(
            logradouro="Rua das Flores",
            numero=123,
            complemento="Apto 45",
            bairro="Centro",
            cep="01234567",
            nome_contato="João Silva",
            telefone="11999887766",
        )

        # Add invoice
        processor.add_registro_50(
            cnpj="98765432109876",
            ie="987654321",
            data=date(2024, 1, 15),
            unidade_federacao="RJ",
            modelo=55,
            serie="001",
            numero=123456,
            cfop=5102,
            emitente="P",
            valor_total=Decimal("1000.00"),
            bc_icms=Decimal("1000.00"),
            valor_icms=Decimal("180.00"),
            isenta=Decimal("0.00"),
            outras=Decimal("0.00"),
            aliquota=Decimal("18.00"),
            situacao="N",
        )

        # Add product info
        processor.add_registro_75(
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

        # Add inventory
        processor.add_registro_74(
            data=date(2024, 1, 31),
            codigo="PROD001",
            quantidade=Decimal("100.000"),
            valor=Decimal("25.99"),
            posse="1",
            cnpj="12345678901234",
            ie="123456789",
            uf="SP",
        )

        # Add ECF records
        processor.add_registro_60m(
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

        # Generate output
        output = processor.generate_output()
        lines = output.strip().split("\n")

        # Should have all records plus auto-generated Registro 90
        assert len(lines) == 7  # 6 records + 1 Registro90

        # Verify record counts
        counts = processor.get_record_counts()
        assert counts["Registro10"] == 1
        assert counts["Registro11"] == 1
        assert counts["Registro50"] == 1
        assert counts["Registro74"] == 1
        assert counts["Registro75"] == 1
        assert counts["Registro60M"] == 1

    def test_validation_in_processor_methods(self):
        """Test that validation works through processor methods."""
        from pydantic import ValidationError

        processor = SintegraProcessor()

        # Test invalid CNPJ
        with pytest.raises(ValidationError):  # Should raise validation error
            processor.add_registro_10(
                cnpj_mf="invalid",
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

        # Test invalid UF
        with pytest.raises(ValidationError):  # Should raise validation error
            processor.add_registro_50(
                cnpj="12345678901234",
                ie="123456789",
                data=date(2024, 1, 15),
                unidade_federacao="XX",  # Invalid UF
                modelo=55,
                serie="001",
                numero=123456,
                cfop=5102,
                emitente="P",
                valor_total=Decimal("1000.00"),
                bc_icms=Decimal("1000.00"),
                valor_icms=Decimal("180.00"),
                isenta=Decimal("0.00"),
                outras=Decimal("0.00"),
                aliquota=Decimal("18.00"),
                situacao="N",
            )

"""SINTEGRA magnetic file processor.

This module provides functionality to generate and parse SINTEGRA magnetic files
using Pydantic models for validation and type safety.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
import logging
from pathlib import Path
from typing import Any

from .models import (
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

logger = logging.getLogger(__name__)


class SintegraProcessor:
    """Main processor for SINTEGRA magnetic files.

    Provides methods to add records, generate output files, and parse existing files.
    """

    def __init__(self) -> None:
        """Initialize the processor with an empty record list."""
        self.records: list[BaseRecord] = []
        self._record_counts: dict[str, int] = {}

    def add_record(self, record: BaseRecord) -> None:
        """Add a record to the processor.

        Args:
            record: A validated Pydantic record instance
        """
        self.records.append(record)
        record_type = record.__class__.__name__
        self._record_counts[record_type] = self._record_counts.get(record_type, 0) + 1

    def add_registro_10(
        self,
        cnpj_mf: str,
        ie: str,
        nome_contribuinte: str,
        municipio: str,
        unidade_federacao: str,
        fax: str,
        data_inicial: date,
        data_final: date,
        cod_id_estrutura: str,
        cod_id_natureza: str,
        cod_id_finalidade: str,
    ) -> None:
        """Add a Registro 10 (establishment master record)."""
        record = Registro10(
            cnpj_mf=cnpj_mf,
            ie=ie,
            nome_contribuinte=nome_contribuinte,
            municipio=municipio,
            unidade_federacao=unidade_federacao,
            fax=fax,
            data_inicial=data_inicial,
            data_final=data_final,
            cod_id_estrutura=cod_id_estrutura,
            cod_id_natureza=cod_id_natureza,
            cod_id_finalidade=cod_id_finalidade,
        )
        self.add_record(record)

    def add_registro_11(
        self,
        logradouro: str,
        numero: int,
        complemento: str,
        bairro: str,
        cep: str,
        nome_contato: str,
        telefone: str,
    ) -> None:
        """Add a Registro 11 (complementary data)."""
        record = Registro11(
            logradouro=logradouro,
            numero=numero,
            complemento=complemento,
            bairro=bairro,
            cep=cep,
            nome_contato=nome_contato,
            telefone=telefone,
        )
        self.add_record(record)

    def add_registro_50(
        self,
        cnpj: str,
        ie: str,
        data: date,
        unidade_federacao: str,
        modelo: int,
        serie: str,
        numero: int,
        cfop: int,
        emitente: str,
        valor_total: float | Decimal,
        bc_icms: float | Decimal,
        valor_icms: float | Decimal,
        isenta: float | Decimal,
        outras: float | Decimal,
        aliquota: float | Decimal,
        situacao: str,
    ) -> None:
        """Add a Registro 50 (invoice total record)."""
        record = Registro50(
            cnpj=cnpj,
            ie=ie,
            data=data,
            unidade_federacao=unidade_federacao,
            modelo=modelo,
            serie=serie,
            numero=numero,
            cfop=cfop,
            emitente=emitente,
            valor_total=Decimal(str(valor_total)),
            bc_icms=Decimal(str(bc_icms)),
            valor_icms=Decimal(str(valor_icms)),
            isenta=Decimal(str(isenta)),
            outras=Decimal(str(outras)),
            aliquota=Decimal(str(aliquota)),
            situacao=situacao,
        )
        self.add_record(record)

    def add_registro_74(
        self,
        data: date,
        codigo: str,
        quantidade: float | Decimal,
        valor: float | Decimal,
        posse: str,
        cnpj: str,
        ie: str,
        uf: str,
    ) -> None:
        """Add a Registro 74 (inventory record)."""
        record = Registro74(
            data=data,
            codigo=codigo,
            quantidade=Decimal(str(quantidade)),
            valor=Decimal(str(valor)),
            posse=posse,
            cnpj=cnpj,
            ie=ie,
            uf=uf,
        )
        self.add_record(record)

    def add_registro_75(self, **kwargs: Any) -> None:
        """Adiciona um registro tipo 75 (Código do produto ou serviço e alíquota de ICMS)."""
        registro = Registro75(**kwargs)
        self.add_record(registro)

    def add_registro_51(self, **kwargs: Any) -> None:
        """Adiciona um registro tipo 51 (Nota Fiscal/Conta de Energia Elétrica, Gás, Água, Comunicações e Similares)."""
        registro = Registro51(**kwargs)
        self.add_record(registro)

    def add_registro_53(self, **kwargs: Any) -> None:
        """Adiciona um registro tipo 53 (Substituição Tributária)."""
        registro = Registro53(**kwargs)
        self.add_record(registro)

    def add_registro_54(self, **kwargs: Any) -> None:
        """Adiciona um registro tipo 54 (Produto)."""
        registro = Registro54(**kwargs)
        self.add_record(registro)

    def add_registro_55(self, **kwargs: Any) -> None:
        """Adiciona um registro tipo 55 (GNRE)."""
        registro = Registro55(**kwargs)
        self.add_record(registro)

    def add_registro_60m(self, **kwargs: Any) -> None:
        """Adiciona um registro tipo 60M (ECF - Mestre)."""
        registro = Registro60M(**kwargs)
        self.add_record(registro)

    def add_registro_60a(self, **kwargs: Any) -> None:
        """Adiciona um registro tipo 60A (ECF - Alíquota)."""
        registro = Registro60A(**kwargs)
        self.add_record(registro)

    def add_registro_60i(self, **kwargs: Any) -> None:
        """Adiciona um registro tipo 60I (ECF - Item)."""
        registro = Registro60I(**kwargs)
        self.add_record(registro)

    def add_registro_61(self, **kwargs: Any) -> None:
        """Adiciona um registro tipo 61 (Resumo Mensal de Documento Fiscal Emitido por ECF)."""
        registro = Registro61(**kwargs)
        self.add_record(registro)

    def add_registro_61r(self, **kwargs: Any) -> None:
        """Adiciona um registro tipo 61R (Resumo Mensal de Itens do ECF por Produto)."""
        registro = Registro61R(**kwargs)
        self.add_record(registro)

    def add_registro_70(self, **kwargs: Any) -> None:
        """Adiciona um registro tipo 70 (Nota Fiscal de Serviços de Comunicação e de Telecomunicação)."""
        registro = Registro70(**kwargs)
        self.add_record(registro)

    def add_registro_71(self, **kwargs: Any) -> None:
        """Adiciona um registro tipo 71 (Nota Fiscal de Serviços de Transporte)."""
        registro = Registro71(**kwargs)
        self.add_record(registro)

    def add_registro_76(self, **kwargs: Any) -> None:
        """Adiciona um registro tipo 76 (Nota Fiscal de Serviços de Comunicação)."""
        registro = Registro76(**kwargs)
        self.add_record(registro)

    def add_registro_85(self, **kwargs: Any) -> None:
        """Adiciona um registro tipo 85 (Informações de Exportação)."""
        registro = Registro85(**kwargs)
        self.add_record(registro)

    def add_registro_86(self, **kwargs: Any) -> None:
        """Adiciona um registro tipo 86 (Informações Complementares de Exportação)."""
        registro = Registro86(**kwargs)
        self.add_record(registro)

    def generate_output(self) -> str:
        """Generate the complete SINTEGRA file content.

        Returns:
            String containing the formatted SINTEGRA file content
        """
        if not self.records:
            msg = "No records added to generate output"
            raise ValueError(msg)

        # Generate main records
        lines = [record.to_sintegra_line() for record in self.records]

        # Generate Registro 90 (totalization records)
        registro_10 = next((r for r in self.records if isinstance(r, Registro10)), None)
        if not registro_10:
            msg = "Registro 10 is required to generate totalization records"
            raise ValueError(msg)

        # Create totalization string
        totals = {}
        for record in self.records:
            record_type = record.__class__.__name__
            totals[record_type] = totals.get(record_type, 0) + 1

        # Format totalization data
        total_str = ""
        for record_type, count in totals.items():
            total_str += f"{record_type[-2:]:0>2}{count:0>8}"

        # Pad to 95 characters
        total_str = total_str.ljust(95)[:95]

        # Create Registro 90
        registro_90 = Registro90(
            cnpj=registro_10.cnpj_mf,
            ie=registro_10.ie,
            totalizacoes=total_str,
            numero=1,
        )
        lines.append(registro_90.to_sintegra_line())

        return "\r\n".join(lines) + "\r\n"

    def save_to_file(self, filepath: str | Path) -> None:
        """Save the generated SINTEGRA content to a file.

        Args:
            filepath: Path where to save the file
        """
        content = self.generate_output()
        Path(filepath).write_text(content, encoding="latin-1")

    @classmethod
    def parse_from_file(cls, filepath: str | Path) -> SintegraProcessor:
        """Parse a SINTEGRA file and create a processor instance.

        Args:
            filepath: Path to the SINTEGRA file to parse

        Returns:
            SintegraProcessor instance with parsed records
        """
        processor = cls()
        content = Path(filepath).read_text(encoding="latin-1")

        # Registry mapping for parsing
        registry_map = {
            "10": Registro10,
            "11": Registro11,
            "50": Registro50,
            "51": Registro51,
            "53": Registro53,
            "54": Registro54,
            "55": Registro55,
            "60": "special",  # Needs subtype handling
            "61": "special",  # Needs subtype handling
            "70": Registro70,
            "71": Registro71,
            "74": Registro74,
            "75": Registro75,
            "76": Registro76,
            "85": Registro85,
            "86": Registro86,
            "90": Registro90,
        }

        # Parse each line
        for line in content.strip().split("\n"):
            line = line.rstrip("\r")
            if len(line) < 2:
                continue

            record_type = line[:2]
            processor._parse_line(line, record_type, registry_map)

        return processor

    def _parse_line(
        self, line: str, record_type: str, registry_map: dict[str, type | str]
    ) -> None:
        """Parse a single line from a SINTEGRA file."""
        try:
            if record_type in registry_map:
                handler = registry_map[record_type]
                if handler == "special":
                    if record_type == "60":
                        self._parse_registro_60(line)
                    elif record_type == "61":
                        self._parse_registro_61(line)
                else:
                    self._parse_generic_registry(line, handler)
            else:
                logger.warning("Unknown record type: %s", record_type)
        except Exception:
            logger.exception("Could not parse line with record type %s", record_type)

    def _parse_generic_registry(self, line: str, registry_class: type) -> None:
        """Parse a line using a generic registry class."""
        # For now, this is a simplified implementation
        # In a full implementation, you would parse each field according to the
        # SINTEGRA specification
        # For testing purposes, we'll create a minimal record
        try:
            if registry_class == Registro10:
                self._parse_registro_10(line)
            elif registry_class == Registro11:
                self._parse_registro_11(line)
            elif registry_class == Registro50:
                self._parse_registro_50(line)
            elif registry_class == Registro74:
                self._parse_registro_74(line)
            elif registry_class == Registro75:
                self._parse_registro_75(line)
            elif registry_class == Registro90:
                self._parse_registro_90(line)
            else:
                # For other registry types, just log for now
                logger.info(
                    "Parsing %s from line: %s...", registry_class.__name__, line[:50]
                )
        except Exception:
            logger.exception("Error parsing %s", registry_class.__name__)

    def _parse_registro_10(self, line: str) -> None:
        """Parse a Registro 10 line."""
        # Extract fields according to SINTEGRA specification
        cnpj_mf = line[2:16].strip()
        ie = line[16:30].strip()
        nome_contribuinte = line[30:65].strip()
        municipio = line[65:95].strip()
        uf = line[95:97].strip()
        fax = line[97:107].strip()
        data_inicial = self._parse_date(line[107:115])
        data_final = self._parse_date(line[115:123])
        cod_id_estrutura = line[123:124].strip()
        cod_id_natureza = line[124:125].strip()
        cod_id_finalidade = line[125:126].strip()

        record = Registro10(
            cnpj_mf=cnpj_mf,
            ie=ie,
            nome_contribuinte=nome_contribuinte,
            municipio=municipio,
            unidade_federacao=uf,
            fax=fax,
            data_inicial=data_inicial,
            data_final=data_final,
            cod_id_estrutura=cod_id_estrutura,
            cod_id_natureza=cod_id_natureza,
            cod_id_finalidade=cod_id_finalidade,
        )
        self.add_record(record)

    def _parse_registro_11(self, line: str) -> None:
        """Parse a Registro 11 line."""
        logradouro = line[2:36].strip()
        numero = int(line[36:41].strip() or "0")
        complemento = line[41:63].strip()
        bairro = line[63:78].strip()
        cep = line[78:86].strip()
        nome_contato = line[86:114].strip()
        telefone = line[114:126].strip()

        record = Registro11(
            logradouro=logradouro,
            numero=numero,
            complemento=complemento,
            bairro=bairro,
            cep=cep,
            nome_contato=nome_contato,
            telefone=telefone,
        )
        self.add_record(record)

    def _parse_registro_50(self, line: str) -> None:
        """Parse a Registro 50 line."""
        # This is a simplified parsing - in practice you'd need to handle all fields
        cnpj = line[2:16].strip()
        ie = line[16:30].strip()
        data = self._parse_date(line[30:38])
        uf = line[38:40].strip()
        modelo = int(line[40:42].strip() or "0")
        serie = line[42:45].strip()
        numero = int(line[45:51].strip() or "0")
        cfop = int(line[51:55].strip() or "0")
        emitente = line[55:56].strip()

        # For now, create with minimal data
        record = Registro50(
            cnpj=cnpj,
            ie=ie,
            data=data,
            unidade_federacao=uf,
            modelo=modelo,
            serie=serie,
            numero=numero,
            cfop=cfop,
            emitente=emitente,
            valor_total=Decimal("0"),
            bc_icms=Decimal("0"),
            valor_icms=Decimal("0"),
            isenta=Decimal("0"),
            outras=Decimal("0"),
            aliquota=Decimal("0"),
            situacao="N",
        )
        self.add_record(record)

    def _parse_registro_74(self, line: str) -> None:
        """Parse a Registro 74 line."""
        data = self._parse_date(line[2:10])
        codigo = line[10:24].strip()
        quantidade = self._parse_decimal(line[24:37], 3)
        valor = self._parse_decimal(line[37:50], 2)
        posse = line[50:51].strip()
        cnpj = line[51:65].strip()
        ie = line[65:79].strip()
        uf = line[79:81].strip()

        record = Registro74(
            data=data,
            codigo=codigo,
            quantidade=quantidade,
            valor=valor,
            posse=posse,
            cnpj=cnpj,
            ie=ie,
            uf=uf,
        )
        self.add_record(record)

    def _parse_registro_75(self, line: str) -> None:
        """Parse a Registro 75 line."""
        # Simplified parsing for Registro 75
        data_inicial = self._parse_date(line[2:10])
        data_final = self._parse_date(line[10:18])
        codigo = line[18:32].strip()
        ncm = line[32:40].strip()
        descricao = line[40:93].strip()

        record = Registro75(
            data_inicial=data_inicial,
            data_final=data_final,
            codigo=codigo,
            ncm=ncm,
            descricao=descricao,
            un_com="UN",
            valor_ipi=Decimal("0"),
            valor_icms=Decimal("0"),
            red_bc_icms=Decimal("0"),
            valor_bc_st=Decimal("0"),
        )
        self.add_record(record)

    def _parse_registro_90(self, line: str) -> None:
        """Parse a Registro 90 line."""
        # Simplified parsing for totalization record
        cnpj = line[2:16].strip()
        ie = line[16:30].strip()
        totalizacoes = line[30:125].strip()
        numero = int(line[125:126].strip() or "1")

        record = Registro90(
            cnpj=cnpj,
            ie=ie,
            totalizacoes=totalizacoes,
            numero=numero,
        )
        self.add_record(record)

    def _parse_registro_60(self, line: str) -> None:
        """Parse Registro 60 with subtype handling."""
        if len(line) > 2:
            subtype = line[2:3]
            if subtype == "M":
                self._parse_generic_registry(line, Registro60M)
            elif subtype == "A":
                self._parse_generic_registry(line, Registro60A)
            elif subtype == "I":
                self._parse_generic_registry(line, Registro60I)
            else:
                logger.warning("Unknown 60 subtype: %s", subtype)

    def _parse_registro_61(self, line: str) -> None:
        """Parse Registro 61 with subtype handling."""
        if len(line) > 2 and line[2:3] == "R":
            self._parse_generic_registry(line, Registro61R)
        else:
            self._parse_generic_registry(line, Registro61)

    @staticmethod
    def _parse_date(date_str: str) -> date:
        """Parse a date string in YYYYMMDD format."""
        date_str = date_str.strip()
        if len(date_str) != 8:
            msg = f"Invalid date format: {date_str}"
            raise ValueError(msg)

        year = int(date_str[:4])
        month = int(date_str[4:6])
        day = int(date_str[6:8])
        return date(year, month, day)

    @staticmethod
    def _parse_decimal(value_str: str, decimal_places: int) -> Decimal:
        """Parse a decimal value from a string with implied decimal places."""
        value_str = value_str.strip()
        if not value_str:
            return Decimal("0")

        # Remove leading zeros and convert to decimal
        value_int = int(value_str)
        divisor = 10**decimal_places
        return Decimal(value_int) / Decimal(divisor)

    def get_record_counts(self) -> dict[str, int]:
        """Get the count of each record type."""
        return self._record_counts.copy()

    def clear_records(self) -> None:
        """Clear all records from the processor."""
        self.records.clear()
        self._record_counts.clear()


# Backward compatibility alias
ArquivoMagnetico = SintegraProcessor

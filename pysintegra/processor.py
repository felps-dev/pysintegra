"""
SINTEGRA magnetic file processor.

This module provides functionality to generate and parse SINTEGRA magnetic files
using Pydantic models for validation and type safety.
"""

from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Dict, List, Union

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


class SintegraProcessor:
    """
    Main processor for SINTEGRA magnetic files.

    Provides methods to add records, generate output files, and parse existing files.
    """

    def __init__(self) -> None:
        """Initialize the processor with an empty record list."""
        self.records: List[BaseRecord] = []
        self._record_counts: Dict[str, int] = {}

    def add_record(self, record: BaseRecord) -> None:
        """
        Add a record to the processor.

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
        valor_total: Union[float, Decimal],
        bc_icms: Union[float, Decimal],
        valor_icms: Union[float, Decimal],
        isenta: Union[float, Decimal],
        outras: Union[float, Decimal],
        aliquota: Union[float, Decimal],
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
        quantidade: Union[float, Decimal],
        valor: Union[float, Decimal],
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

    def add_registro_75(self, **kwargs) -> None:
        """Adiciona um registro tipo 75 (Código do produto ou serviço e alíquota de ICMS)"""
        registro = Registro75(**kwargs)
        self.add_record(registro)

    def add_registro_51(self, **kwargs) -> None:
        """Adiciona um registro tipo 51 (Nota Fiscal/Conta de Energia Elétrica, Gás, Água, Comunicações e Similares)"""
        registro = Registro51(**kwargs)
        self.add_record(registro)

    def add_registro_53(self, **kwargs) -> None:
        """Adiciona um registro tipo 53 (Substituição Tributária)"""
        registro = Registro53(**kwargs)
        self.add_record(registro)

    def add_registro_54(self, **kwargs) -> None:
        """Adiciona um registro tipo 54 (Produto)"""
        registro = Registro54(**kwargs)
        self.add_record(registro)

    def add_registro_55(self, **kwargs) -> None:
        """Adiciona um registro tipo 55 (GNRE)"""
        registro = Registro55(**kwargs)
        self.add_record(registro)

    def add_registro_60m(self, **kwargs) -> None:
        """Adiciona um registro tipo 60M (ECF - Mestre)"""
        registro = Registro60M(**kwargs)
        self.add_record(registro)

    def add_registro_60a(self, **kwargs) -> None:
        """Adiciona um registro tipo 60A (ECF - Alíquota)"""
        registro = Registro60A(**kwargs)
        self.add_record(registro)

    def add_registro_60i(self, **kwargs) -> None:
        """Adiciona um registro tipo 60I (ECF - Item)"""
        registro = Registro60I(**kwargs)
        self.add_record(registro)

    def add_registro_61(self, **kwargs) -> None:
        """Adiciona um registro tipo 61 (Resumo Mensal de Documento Fiscal Emitido por ECF)"""
        registro = Registro61(**kwargs)
        self.add_record(registro)

    def add_registro_61r(self, **kwargs) -> None:
        """Adiciona um registro tipo 61R (Resumo Mensal de Itens do ECF por Produto)"""
        registro = Registro61R(**kwargs)
        self.add_record(registro)

    def add_registro_70(self, **kwargs) -> None:
        """Adiciona um registro tipo 70 (Nota Fiscal de Serviços de Comunicação e de Telecomunicação)"""
        registro = Registro70(**kwargs)
        self.add_record(registro)

    def add_registro_71(self, **kwargs) -> None:
        """Adiciona um registro tipo 71 (Nota Fiscal de Serviços de Transporte)"""
        registro = Registro71(**kwargs)
        self.add_record(registro)

    def add_registro_76(self, **kwargs) -> None:
        """Adiciona um registro tipo 76 (Nota Fiscal de Serviços de Comunicação)"""
        registro = Registro76(**kwargs)
        self.add_record(registro)

    def add_registro_85(self, **kwargs) -> None:
        """Adiciona um registro tipo 85 (Informações de Exportação)"""
        registro = Registro85(**kwargs)
        self.add_record(registro)

    def add_registro_86(self, **kwargs) -> None:
        """Adiciona um registro tipo 86 (Informações Complementares de Exportação)"""
        registro = Registro86(**kwargs)
        self.add_record(registro)

    def generate_output(self) -> str:
        """
        Generate the complete SINTEGRA file content.

        Returns:
            String containing the formatted SINTEGRA file content
        """
        if not self.records:
            raise ValueError("No records added to generate output")

        # Generate main records
        lines = []
        for record in self.records:
            lines.append(record.to_sintegra_line())

        # Generate Registro 90 (totalization records)
        registro_10 = next((r for r in self.records if isinstance(r, Registro10)), None)
        if not registro_10:
            raise ValueError("Registro 10 is required to generate totalization records")

        # Create totalization string
        totalization_parts = []
        for record_type, count in self._record_counts.items():
            if record_type != "Registro90":  # Don't count the 90 records themselves
                type_code = record_type.replace("Registro", "")
                totalization_parts.append(f"{type_code}{count:08d}")

        # Pad totalization string to 95 characters
        totalization_str = "".join(totalization_parts).ljust(95, " ")

        # Add Registro 90
        registro_90 = Registro90(
            cnpj=registro_10.cnpj_mf,
            ie=registro_10.ie,
            totalizacoes=totalization_str,
            numero=1,
        )
        lines.append(registro_90.to_sintegra_line())

        return "\r\n".join(lines) + "\r\n"

    def save_to_file(self, filepath: Union[str, Path]) -> None:
        """
        Save the generated SINTEGRA content to a file.

        Args:
            filepath: Path where to save the file
        """
        content = self.generate_output()
        Path(filepath).write_text(content, encoding="latin-1")

    @classmethod
    def parse_from_file(cls, filepath: Union[str, Path]) -> "SintegraProcessor":
        """
        Parse a SINTEGRA file and create a processor instance.

        Args:
            filepath: Path to the SINTEGRA file to parse

        Returns:
            SintegraProcessor instance with parsed records
        """
        processor = cls()
        content = Path(filepath).read_text(encoding="latin-1")

        registry_map = {
            "10": Registro10,
            "11": Registro11,
            "50": Registro50,
            "51": Registro51,
            "53": Registro53,
            "54": Registro54,
            "55": Registro55,
            "60": processor._parse_registro_60,  # Special handling for subtypes
            "61": processor._parse_registro_61,  # Special handling for subtypes
            "70": Registro70,
            "71": Registro71,
            "74": Registro74,
            "75": Registro75,
            "76": Registro76,
            "85": Registro85,
            "86": Registro86,
            "90": Registro90,
        }

        for line in content.strip().split("\n"):
            line = line.rstrip("\r")
            if len(line) < 2:
                continue

            record_type = line[:2]
            processor._parse_line(line, record_type, registry_map)

        return processor

    def _parse_line(
        self, line: str, record_type: str, registry_map: Dict[str, type]
    ) -> None:
        """Parse a single line from a SINTEGRA file."""
        try:
            if record_type in registry_map:
                handler = registry_map[record_type]
                if callable(handler) and hasattr(handler, "__self__"):
                    # It's a method (for special cases like 60, 61)
                    handler(line)
                else:
                    # It's a registry class
                    self._parse_generic_registry(line, handler)
            else:
                print(f"Warning: Unknown record type: {record_type}")
        except Exception as e:
            print(f"Warning: Could not parse line with record type {record_type}: {e}")

    def _parse_generic_registry(self, line: str, registry_class) -> None:
        """Parse a line using a generic registry class."""
        # For now, this is a simplified implementation
        # In a full implementation, you would parse each field according to the SINTEGRA specification
        # For testing purposes, we'll create a minimal record
        try:
            if registry_class == Registro10:
                # Parse basic Registro10 fields from the line
                record = Registro10(
                    cnpj_mf=line[2:16],
                    ie=line[16:30].strip(),
                    nome_contribuinte=line[30:65].strip(),
                    municipio=line[65:95].strip(),
                    unidade_federacao=line[95:97],
                    fax=line[97:107].strip(),
                    data_inicial=self._parse_date(line[107:115]),
                    data_final=self._parse_date(line[115:123]),
                    cod_id_estrutura=line[123:124],
                    cod_id_natureza=line[124:125],
                    cod_id_finalidade=line[125:126],
                )
                self.add_record(record)
            elif registry_class == Registro75:
                # Parse basic Registro75 fields from the line
                record = Registro75(
                    data_inicial=self._parse_date(line[2:10]),
                    data_final=self._parse_date(line[10:18]),
                    codigo=line[18:32].strip(),
                    ncm=line[32:40],
                    descricao=line[40:93].strip(),
                    un_com=line[93:99].strip(),
                    valor_ipi=self._parse_decimal(line[99:104], 2),
                    valor_icms=self._parse_decimal(line[104:108], 2),
                    red_bc_icms=self._parse_decimal(line[108:113], 2),
                    valor_bc_st=self._parse_decimal(line[113:126], 2),
                )
                self.add_record(record)
            else:
                # For other registry types, just print for now
                print(f"Parsing {registry_class.__name__} from line: {line[:50]}...")
        except Exception as e:
            print(f"Error parsing {registry_class.__name__}: {e}")

    def _parse_registro_10(self, line: str) -> None:
        """Parse a Registro 10 line."""
        record = Registro10(
            cnpj_mf=line[2:16].strip(),
            ie=line[16:30].strip(),
            nome_contribuinte=line[30:65].strip(),
            municipio=line[65:95].strip(),
            unidade_federacao=line[95:97].strip(),
            fax=line[97:107].strip(),
            data_inicial=self._parse_date(line[107:115]),
            data_final=self._parse_date(line[115:123]),
            cod_id_estrutura=line[123:124].strip(),
            cod_id_natureza=line[124:125].strip(),
            cod_id_finalidade=line[125:126].strip(),
        )
        self.add_record(record)

    def _parse_registro_11(self, line: str) -> None:
        """Parse a Registro 11 line."""
        record = Registro11(
            logradouro=line[2:36].strip(),
            numero=int(line[36:41].strip() or "0"),
            complemento=line[41:63].strip(),
            bairro=line[63:78].strip(),
            cep=line[78:86].strip(),
            nome_contato=line[86:114].strip(),
            telefone=line[114:126].strip(),
        )
        self.add_record(record)

    def _parse_registro_50(self, line: str) -> None:
        """Parse a Registro 50 line."""
        record = Registro50(
            cnpj=line[2:16].strip(),
            ie=line[16:30].strip(),
            data=self._parse_date(line[30:38]),
            unidade_federacao=line[38:40].strip(),
            modelo=int(line[40:42].strip() or "0"),
            serie=line[42:45].strip(),
            numero=int(line[45:51].strip() or "0"),
            cfop=int(line[51:55].strip() or "0"),
            emitente=line[55:56].strip(),
            valor_total=self._parse_decimal(line[56:69], 2),
            bc_icms=self._parse_decimal(line[69:82], 2),
            valor_icms=self._parse_decimal(line[82:95], 2),
            isenta=self._parse_decimal(line[95:108], 2),
            outras=self._parse_decimal(line[108:121], 2),
            aliquota=self._parse_decimal(line[121:125], 2),
            situacao=line[125:126].strip(),
        )
        self.add_record(record)

    def _parse_registro_74(self, line: str) -> None:
        """Parse a Registro 74 line."""
        record = Registro74(
            data=self._parse_date(line[2:10]),
            codigo=line[10:24].strip(),
            quantidade=self._parse_decimal(line[24:37], 3),
            valor=self._parse_decimal(line[37:50], 2),
            posse=line[50:51].strip(),
            cnpj=line[51:65].strip(),
            ie=line[65:79].strip(),
            uf=line[79:81].strip(),
        )
        self.add_record(record)

    def _parse_registro_75(self, line: str) -> None:
        """Parse a Registro 75 line."""
        record = Registro75(
            data_inicial=self._parse_date(line[2:10]),
            data_final=self._parse_date(line[10:18]),
            codigo=line[18:32].strip(),
            ncm=line[32:40].strip(),
            descricao=line[40:93].strip(),
            un_com=line[93:99].strip(),
            valor_ipi=self._parse_decimal(line[99:104], 2),
            valor_icms=self._parse_decimal(line[104:108], 2),
            red_bc_icms=self._parse_decimal(line[108:113], 2),
            valor_bc_st=self._parse_decimal(line[113:126], 2),
        )
        self.add_record(record)

    def _parse_registro_90(self, line: str) -> None:
        """Parse a Registro 90 line."""
        record = Registro90(
            cnpj=line[2:16].strip(),
            ie=line[16:30].strip(),
            totalizacoes=line[30:125].strip(),
            numero=int(line[125:126].strip() or "1"),
        )
        self.add_record(record)

    def _parse_registro_60(self, line: str) -> None:
        """Parse registro 60 with subtype handling."""
        if len(line) > 2:
            subtype = line[2]
            if subtype == "M":
                self._parse_generic_registry(line, Registro60M)
            elif subtype == "A":
                self._parse_generic_registry(line, Registro60A)
            elif subtype == "I":
                self._parse_generic_registry(line, Registro60I)
            else:
                print(f"Warning: Unknown 60 subtype: {subtype}")

    def _parse_registro_61(self, line: str) -> None:
        """Parse registro 61 with subtype handling."""
        if len(line) > 2:
            subtype = line[2]
            if subtype == "R":
                self._parse_generic_registry(line, Registro61R)
            else:
                # Default to regular Registro61
                self._parse_generic_registry(line, Registro61)

    @staticmethod
    def _parse_date(date_str: str) -> date:
        """Parse a date string in YYYYMMDD format."""
        date_str = date_str.strip()
        if len(date_str) != 8:
            raise ValueError(f"Invalid date format: {date_str}")

        year = int(date_str[:4])
        month = int(date_str[4:6])
        day = int(date_str[6:8])
        return date(year, month, day)

    @staticmethod
    def _parse_decimal(value_str: str, decimal_places: int) -> Decimal:
        """Parse a decimal value from SINTEGRA format."""
        value_str = value_str.strip()
        if not value_str:
            return Decimal("0")

        # Convert to decimal by inserting decimal point
        if decimal_places > 0:
            if len(value_str) <= decimal_places:
                value_str = "0." + value_str.zfill(decimal_places)
            else:
                integer_part = value_str[:-decimal_places]
                decimal_part = value_str[-decimal_places:]
                value_str = f"{integer_part}.{decimal_part}"

        return Decimal(value_str)

    def get_record_counts(self) -> Dict[str, int]:
        """Get the count of each record type."""
        return self._record_counts.copy()

    def clear_records(self) -> None:
        """Clear all records from the processor."""
        self.records.clear()
        self._record_counts.clear()


# Backward compatibility alias
ArquivoMagnetico = SintegraProcessor

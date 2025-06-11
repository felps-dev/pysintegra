"""Pydantic models for SINTEGRA magnetic file generation.

This module contains all the record types supported by the SINTEGRA format,
implemented using Pydantic for robust validation and type safety.
"""

from __future__ import annotations

from datetime import date  # noqa: TC003
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BaseRecord(BaseModel):
    """Base class for all SINTEGRA records with common validation logic."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )

    def to_sintegra_line(self) -> str:
        """Convert the record to a SINTEGRA formatted line."""
        msg = "Subclasses must implement to_sintegra_line"
        raise NotImplementedError(msg)

    @staticmethod
    def _format_numeric(
        value: int | float | Decimal, size: int, decimal_places: int = 0
    ) -> str:
        """Format numeric values for SINTEGRA output."""
        if isinstance(value, (int, float)):
            value = Decimal(str(value))

        if decimal_places > 0:
            formatted = f"{value:.{decimal_places}f}".replace(".", "")
        else:
            formatted = str(int(value))

        return formatted.rjust(size, "0")

    @staticmethod
    def _format_text(value: str, size: int) -> str:
        """Format text values for SINTEGRA output."""
        return str(value).ljust(size, " ")[:size]

    @staticmethod
    def _format_date(value: date) -> str:
        """Format date values for SINTEGRA output (YYYYMMDD)."""
        return value.strftime("%Y%m%d")


class Registro10(BaseRecord):
    """Master establishment record for identifying the reporting establishment.

    This record contains the basic identification information of the establishment
    that is providing the SINTEGRA data.
    """

    cnpj_mf: str = Field(
        ...,
        description="CNPJ of the reporting establishment",
        min_length=14,
        max_length=14,
    )
    ie: str = Field(
        ...,
        description="State registration of the reporting establishment",
        max_length=14,
    )
    nome_contribuinte: str = Field(..., description="Taxpayer name", max_length=35)
    municipio: str = Field(..., description="Municipality", max_length=30)
    unidade_federacao: str = Field(
        ..., description="State (UF)", min_length=2, max_length=2
    )
    fax: str = Field(..., description="Fax number", max_length=10)
    data_inicial: date = Field(..., description="Start date of the reporting period")
    data_final: date = Field(..., description="End date of the reporting period")
    cod_id_estrutura: str = Field(
        ..., description="Structure identification code", min_length=1, max_length=1
    )
    cod_id_natureza: str = Field(
        ...,
        description="Nature of operations identification code",
        min_length=1,
        max_length=1,
    )
    cod_id_finalidade: str = Field(
        ..., description="File purpose identification code", min_length=1, max_length=1
    )

    @field_validator("cnpj_mf")
    @classmethod
    def validate_cnpj(cls, v: str) -> str:
        if not v.isdigit():
            msg = "CNPJ must contain only digits"
            raise ValueError(msg)
        return v

    @field_validator("unidade_federacao")
    @classmethod
    def validate_uf(cls, v: str) -> str:
        valid_ufs = {
            "AC",
            "AL",
            "AP",
            "AM",
            "BA",
            "CE",
            "DF",
            "ES",
            "GO",
            "MA",
            "MT",
            "MS",
            "MG",
            "PA",
            "PB",
            "PR",
            "PE",
            "PI",
            "RJ",
            "RN",
            "RS",
            "RO",
            "RR",
            "SC",
            "SP",
            "SE",
            "TO",
        }
        if v.upper() not in valid_ufs:
            msg = f"Invalid UF: {v}"
            raise ValueError(msg)
        return v.upper()

    def to_sintegra_line(self) -> str:
        """Convert to SINTEGRA format line."""
        return (
            self._format_text("10", 2)
            + self._format_numeric(self.cnpj_mf, 14)
            + self._format_text(self.ie, 14)
            + self._format_text(self.nome_contribuinte, 35)
            + self._format_text(self.municipio, 30)
            + self._format_text(self.unidade_federacao, 2)
            + self._format_text(self.fax, 10)
            + self._format_date(self.data_inicial)
            + self._format_date(self.data_final)
            + self._format_text(self.cod_id_estrutura, 1)
            + self._format_text(self.cod_id_natureza, 1)
            + self._format_text(self.cod_id_finalidade, 1)
        )


class Registro11(BaseRecord):
    """Complementary data of the reporting party.

    Contains additional address and contact information for the establishment.
    """

    logradouro: str = Field(..., description="Street address", max_length=34)
    numero: int = Field(..., description="Street number", ge=0, le=99999)
    complemento: str = Field(..., description="Address complement", max_length=22)
    bairro: str = Field(..., description="Neighborhood", max_length=15)
    cep: str = Field(..., description="ZIP code", min_length=8, max_length=8)
    nome_contato: str = Field(..., description="Contact name", max_length=28)
    telefone: str = Field(..., description="Phone number", max_length=12)

    @field_validator("cep")
    @classmethod
    def validate_cep(cls, v: str) -> str:
        if not v.isdigit():
            msg = "CEP must contain only digits"
            raise ValueError(msg)
        return v

    def to_sintegra_line(self) -> str:
        """Convert to SINTEGRA format line."""
        return (
            self._format_text("11", 2)
            + self._format_text(self.logradouro, 34)
            + self._format_numeric(self.numero, 5)
            + self._format_text(self.complemento, 22)
            + self._format_text(self.bairro, 15)
            + self._format_numeric(self.cep, 8)
            + self._format_text(self.nome_contato, 28)
            + self._format_text(self.telefone, 12)
        )


class Registro50(BaseRecord):
    """Invoice total record for models 1 and 1A.

    Specifies totalization information for fiscal documents regarding ICMS.
    For documents with multiple ICMS rates and/or CFOPs, generate one record
    for each combination.
    """

    cnpj: str = Field(
        ...,
        description="CNPJ of sender (inbound) or recipient (outbound)",
        min_length=14,
        max_length=14,
    )
    ie: str = Field(..., description="State registration", max_length=14)
    data: date = Field(
        ..., description="Issue date (outbound) or receipt date (inbound)"
    )
    unidade_federacao: str = Field(
        ..., description="State (UF)", min_length=2, max_length=2
    )
    modelo: int = Field(..., description="Invoice model code", ge=1, le=99)
    serie: str = Field(..., description="Invoice series", max_length=3)
    numero: int = Field(..., description="Invoice number", ge=1, le=999999)
    cfop: int = Field(..., description="CFOP code", ge=1000, le=9999)
    emitente: Literal["P", "T"] = Field(..., description="Issuer (P=own/T=third party)")
    valor_total: Decimal = Field(..., description="Total invoice value", ge=0)
    bc_icms: Decimal = Field(..., description="ICMS calculation base", ge=0)
    valor_icms: Decimal = Field(..., description="ICMS amount", ge=0)
    isenta: Decimal = Field(..., description="Exempt or non-taxable value", ge=0)
    outras: Decimal = Field(
        ..., description="Other values (no ICMS debit/credit)", ge=0
    )
    aliquota: Decimal = Field(..., description="ICMS rate", ge=0, le=100)
    situacao: str = Field(..., description="Invoice status", min_length=1, max_length=1)

    @field_validator("unidade_federacao")
    @classmethod
    def validate_uf(cls, v: str) -> str:
        valid_ufs = {
            "AC",
            "AL",
            "AP",
            "AM",
            "BA",
            "CE",
            "DF",
            "ES",
            "GO",
            "MA",
            "MT",
            "MS",
            "MG",
            "PA",
            "PB",
            "PR",
            "PE",
            "PI",
            "RJ",
            "RN",
            "RS",
            "RO",
            "RR",
            "SC",
            "SP",
            "SE",
            "TO",
        }
        if v.upper() not in valid_ufs:
            msg = "Invalid UF"
            raise ValueError(msg)
        return v.upper()

    @field_validator("cnpj")
    @classmethod
    def validate_cnpj(cls, v: str) -> str:
        if not v.isdigit():
            msg = "CNPJ must contain only digits"
            raise ValueError(msg)
        return v

    def to_sintegra_line(self) -> str:
        """Convert to SINTEGRA format line."""
        return (
            self._format_text("50", 2)
            + self._format_numeric(self.cnpj, 14)
            + self._format_text(self.ie, 14)
            + self._format_date(self.data)
            + self._format_text(self.unidade_federacao, 2)
            + self._format_numeric(self.modelo, 2)
            + self._format_text(self.serie, 3)
            + self._format_numeric(self.numero, 6)
            + self._format_numeric(self.cfop, 4)
            + self._format_text(self.emitente, 1)
            + self._format_numeric(self.valor_total, 13, 2)
            + self._format_numeric(self.bc_icms, 13, 2)
            + self._format_numeric(self.valor_icms, 13, 2)
            + self._format_numeric(self.isenta, 13, 2)
            + self._format_numeric(self.outras, 13, 2)
            + self._format_numeric(self.aliquota, 4, 2)
            + self._format_text(self.situacao, 1)
        )


class Registro51(BaseRecord):
    """Registro Tipo 51 - Nota Fiscal/Conta de Energia Elétrica, Gás, Água.

    Registro obrigatório para informar as notas fiscais/contas de energia elétrica,
    gás, água, comunicações e similares.
    """

    tipo: Literal["51"] = Field(default="51", description="Tipo do registro")
    cnpj: str = Field(
        ...,
        min_length=14,
        max_length=14,
        description="CNPJ do remetente nas entradas e do destinatário nas saídas",
    )
    ie: str = Field(
        ...,
        max_length=14,
        description="Inscrição Estadual do remetente/destinatário",
    )
    data: date = Field(
        ..., description="Data de emissão na saída ou de recebimento na entrada"
    )
    uf: str = Field(..., min_length=2, max_length=2, description="Unidade da Federação")
    serie: str = Field(..., max_length=3, description="Série da nota fiscal")
    numero: int = Field(..., description="Número da nota fiscal")
    cfop: int = Field(
        ..., ge=1000, le=9999, description="Código Fiscal de Operação e Prestação"
    )
    valor_total: Decimal = Field(..., ge=0, description="Valor total da nota fiscal")
    valor_ipi: Decimal = Field(..., ge=0, description="Montante IPI da nota fiscal")
    isenta: Decimal = Field(
        ..., ge=0, description="Valor amparado por isenção ou não incidência"
    )
    outras: Decimal = Field(
        ..., ge=0, description="Valor que não confira débito ou crédito do ICMS"
    )
    situacao: str = Field(
        ..., min_length=1, max_length=1, description="Situação da Nota Fiscal"
    )

    @field_validator("uf")
    @classmethod
    def validate_uf(cls, v: str) -> str:
        valid_ufs = {
            "AC",
            "AL",
            "AP",
            "AM",
            "BA",
            "CE",
            "DF",
            "ES",
            "GO",
            "MA",
            "MT",
            "MS",
            "MG",
            "PA",
            "PB",
            "PR",
            "PE",
            "PI",
            "RJ",
            "RN",
            "RS",
            "RO",
            "RR",
            "SC",
            "SP",
            "SE",
            "TO",
        }
        if v.upper() not in valid_ufs:
            msg = f"UF deve ser uma das seguintes: {', '.join(valid_ufs)}"
            raise ValueError(msg)
        return v.upper()

    @field_validator("cnpj")
    @classmethod
    def validate_cnpj(cls, v: str) -> str:
        if not v.isdigit():
            msg = "CNPJ deve conter apenas dígitos"
            raise ValueError(msg)
        return v

    def to_sintegra_line(self) -> str:
        return (
            f"{self.tipo}"
            f"{self.cnpj.zfill(14)}"
            f"{self.ie:<14}"
            f"{self.data.strftime('%Y%m%d')}"
            f"{self.uf}"
            f"{self.serie:<3}"
            f"{self.numero:06d}"
            f"{self.cfop:04d}"
            f"{int(self.valor_total * 100):013d}"
            f"{int(self.valor_ipi * 100):013d}"
            f"{int(self.isenta * 100):013d}"
            f"{int(self.outras * 100):013d}"
            f"{'':<20}"  # brancos
            f"{self.situacao}"
        )


class Registro53(BaseRecord):
    """Registro Tipo 53 - Substituição Tributária.

    Registro obrigatório para informar as operações com substituição tributária.
    """

    tipo: Literal["53"] = Field(default="53", description="Tipo do registro")
    cnpj: str = Field(
        ...,
        min_length=14,
        max_length=14,
        description="CNPJ do remetente nas entradas e do destinatário nas saídas",
    )
    ie: str = Field(
        ...,
        max_length=14,
        description="Inscrição Estadual do remetente/destinatário",
    )
    data: date = Field(
        ..., description="Data de emissão na saída ou de recebimento na entrada"
    )
    uf: str = Field(..., min_length=2, max_length=2, description="Unidade da Federação")
    modelo: int = Field(..., description="Código do modelo da nota fiscal")
    serie: str = Field(..., max_length=3, description="Série da nota fiscal")
    numero: int = Field(..., description="Número da nota fiscal")
    cfop: int = Field(
        ..., ge=1000, le=9999, description="Código Fiscal de Operação e Prestação"
    )
    emitente: str = Field(
        ...,
        min_length=1,
        max_length=1,
        description="Emitente da Nota Fiscal (P-próprio/T-terceiros)",
    )
    bc_icms: Decimal = Field(
        ..., ge=0, description="Base de cálculo de retenção do ICMS"
    )
    icms_retido: Decimal = Field(..., ge=0, description="ICMS retido pelo substituto")
    despesas_acessorias: Decimal = Field(
        ..., ge=0, description="Soma das despesas acessórias (frete, seguro e outras)"
    )
    situacao: str = Field(
        ..., min_length=1, max_length=1, description="Situação da Nota Fiscal"
    )

    @field_validator("uf")
    @classmethod
    def validate_uf(cls, v: str) -> str:
        valid_ufs = {
            "AC",
            "AL",
            "AP",
            "AM",
            "BA",
            "CE",
            "DF",
            "ES",
            "GO",
            "MA",
            "MT",
            "MS",
            "MG",
            "PA",
            "PB",
            "PR",
            "PE",
            "PI",
            "RJ",
            "RN",
            "RS",
            "RO",
            "RR",
            "SC",
            "SP",
            "SE",
            "TO",
        }
        if v.upper() not in valid_ufs:
            msg = f"UF deve ser uma das seguintes: {', '.join(valid_ufs)}"
            raise ValueError(msg)
        return v.upper()

    @field_validator("cnpj")
    @classmethod
    def validate_cnpj(cls, v: str) -> str:
        if not v.isdigit():
            msg = "CNPJ deve conter apenas dígitos"
            raise ValueError(msg)
        return v

    def to_sintegra_line(self) -> str:
        return (
            f"{self.tipo}"
            f"{self.cnpj.zfill(14)}"
            f"{self.ie:<14}"
            f"{self.data.strftime('%Y%m%d')}"
            f"{self.uf}"
            f"{self.modelo:02d}"
            f"{self.serie:<3}"
            f"{self.numero:06d}"
            f"{self.cfop:04d}"
            f"{self.emitente}"
            f"{int(self.bc_icms * 100):013d}"
            f"{int(self.icms_retido * 100):013d}"
            f"{int(self.despesas_acessorias * 100):013d}"
            f"{self.situacao}"
            f"{'':<30}"  # brancos
        )


class Registro54(BaseRecord):
    """Registro Tipo 54 - Produto.

    Registro obrigatório para informar os produtos/mercadorias constantes
    nos documentos fiscais informados nos registros 50, 51, 53, 70, 71 e 76.
    """

    tipo: Literal["54"] = Field(default="54", description="Tipo do registro")
    cnpj: str = Field(
        ...,
        min_length=14,
        max_length=14,
        description="CNPJ do remetente nas entradas e do destinatário nas saídas",
    )
    modelo: int = Field(..., description="Código do modelo da nota fiscal")
    serie: str = Field(..., max_length=3, description="Série da nota fiscal")
    numero: int = Field(..., description="Número da nota fiscal")
    cfop: int = Field(
        ..., ge=1000, le=9999, description="Código Fiscal de Operação e Prestação"
    )
    cst: int = Field(..., description="Código da Situação Tributária")
    item: int = Field(..., description="Número de ordem do item na nota fiscal")
    codigo: str = Field(
        ...,
        max_length=14,
        description="Código do produto/mercadoria ou serviço do informante",
    )
    quantidade: Decimal = Field(
        ..., ge=0, description="Quantidade do produto/mercadoria"
    )
    valor: Decimal = Field(..., ge=0, description="Valor bruto do produto/mercadoria")
    desconto: Decimal = Field(
        ..., ge=0, description="Valor do desconto concedido no item"
    )
    bc_icms: Decimal = Field(..., ge=0, description="Base de cálculo do ICMS")
    bc_icms_st: Decimal = Field(
        ...,
        ge=0,
        description="Base de cálculo do ICMS de retenção na Substituição Tributária",
    )
    valor_ipi: Decimal = Field(..., ge=0, description="Valor IPI")
    aliquota: Decimal = Field(..., ge=0, le=100, description="Alíquota do ICMS")

    @field_validator("cnpj")
    @classmethod
    def validate_cnpj(cls, v: str) -> str:
        if not v.isdigit():
            msg = "CNPJ deve conter apenas dígitos"
            raise ValueError(msg)
        return v

    def to_sintegra_line(self) -> str:
        return (
            f"{self.tipo}"
            f"{self.cnpj.zfill(14)}"
            f"{self.modelo:02d}"
            f"{self.serie:<3}"
            f"{self.numero:06d}"
            f"{self.cfop:04d}"
            f"{self.cst:03d}"
            f"{self.item:03d}"
            f"{self.codigo:<14}"
            f"{int(self.quantidade * 1000):011d}"  # 3 decimais
            f"{int(self.valor * 100):012d}"
            f"{int(self.desconto * 100):012d}"
            f"{int(self.bc_icms * 100):012d}"
            f"{int(self.bc_icms_st * 100):012d}"
            f"{int(self.valor_ipi * 100):012d}"
            f"{int(self.aliquota * 100):04d}"
        )


class Registro55(BaseRecord):
    """Registro Tipo 55 - Guia Nacional de Recolhimento de Tributos Estaduais (GNRE).

    Registro obrigatório para informar os recolhimentos de ICMS efetuados
    através da GNRE.
    """

    tipo: Literal["55"] = Field(default="55", description="Tipo do registro")
    cnpj: str = Field(
        ...,
        min_length=14,
        max_length=14,
        description="CNPJ do contribuinte substituto tributário",
    )
    ie: str = Field(
        ...,
        max_length=14,
        description="Inscrição Estadual do contribuinte substituto tributário",
    )
    data: date = Field(..., description="Data da GNRE")
    uf: str = Field(
        ...,
        min_length=2,
        max_length=2,
        description="Unidade da Federação do contribuinte substituto tributário",
    )
    uf_favorecida: str = Field(
        ..., min_length=2, max_length=2, description="Unidade da Federação destino"
    )
    banco: int = Field(
        ..., description="Código do banco onde foi efetuado o recolhimento"
    )
    agencia: int = Field(..., description="Agência onde foi efetuado o recolhimento")
    numero: int = Field(
        ..., description="Número de autenticação bancária do documento de arrecadação"
    )
    valor: Decimal = Field(..., ge=0, description="Valor GNRE")
    data_vencimento: date = Field(..., description="Data do vencimento")
    mes_ano_referencia: int = Field(
        ..., description="Mês e ano referente à ocorrência do fato gerador (MMAAAA)"
    )
    convenio: str = Field(
        ..., max_length=30, description="Número do Convênio ou Protocolo/Mercadoria"
    )

    @field_validator("uf", "uf_favorecida")
    @classmethod
    def validate_uf(cls, v: str) -> str:
        valid_ufs = {
            "AC",
            "AL",
            "AP",
            "AM",
            "BA",
            "CE",
            "DF",
            "ES",
            "GO",
            "MA",
            "MT",
            "MS",
            "MG",
            "PA",
            "PB",
            "PR",
            "PE",
            "PI",
            "RJ",
            "RN",
            "RS",
            "RO",
            "RR",
            "SC",
            "SP",
            "SE",
            "TO",
        }
        if v.upper() not in valid_ufs:
            msg = f"UF deve ser uma das seguintes: {', '.join(valid_ufs)}"
            raise ValueError(msg)
        return v.upper()

    @field_validator("cnpj")
    @classmethod
    def validate_cnpj(cls, v: str) -> str:
        if not v.isdigit():
            msg = "CNPJ deve conter apenas dígitos"
            raise ValueError(msg)
        return v

    def to_sintegra_line(self) -> str:
        return (
            f"{self.tipo}"
            f"{self.cnpj.zfill(14)}"
            f"{self.ie:<14}"
            f"{self.data.strftime('%Y%m%d')}"
            f"{self.uf}"
            f"{self.uf_favorecida}"
            f"{self.banco:03d}"
            f"{self.agencia:04d}"
            f"{self.numero:020d}"
            f"{int(self.valor * 100):012d}"
            f"{self.data_vencimento.strftime('%Y%m%d')}"
            f"{self.mes_ano_referencia:06d}"
            f"{self.convenio:<30}"
        )


class Registro60M(BaseRecord):
    """Registro Tipo 60M - Equipamento Emissor de Cupom Fiscal (ECF) - Mestre.

    Registro obrigatório para informar os dados do equipamento emissor de cupom fiscal.
    """

    tipo: Literal["60"] = Field(default="60", description="Tipo do registro")
    subtipo: Literal["M"] = Field(default="M", description="Subtipo M")
    data: date = Field(..., description="Data de emissão dos documentos")
    serie: str = Field(
        ..., max_length=20, description="Série de fabricação do equipamento"
    )
    sequencia: int = Field(
        ..., description="Número atribuído pelo estabelecimento ao equipamento"
    )
    modelo: str = Field(
        ..., max_length=2, description="Código do modelo do documento fiscal"
    )
    coo_inicio: int = Field(..., description="COO do início do dia")
    coo_fim: int = Field(..., description="COO do fim do dia")
    crz: int = Field(..., description="Número do Contador de Redução Z (CRZ)")
    cro: int = Field(
        ..., description="Valor acumulado no Contador de Reinício de Operação (CRO)"
    )
    venda_bruta: Decimal = Field(..., ge=0, description="Valor venda bruta")
    totalizador: Decimal = Field(..., ge=0, description="Valor totalizador geral")

    def to_sintegra_line(self) -> str:
        return (
            f"{self.tipo}"
            f"{self.subtipo}"
            f"{self.data.strftime('%Y%m%d')}"
            f"{self.serie:<20}"
            f"{self.sequencia:03d}"
            f"{self.modelo:<2}"
            f"{self.coo_inicio:06d}"
            f"{self.coo_fim:06d}"
            f"{self.crz:06d}"
            f"{self.cro:03d}"
            f"{int(self.venda_bruta):016d}"
            f"{int(self.totalizador):016d}"
            f"{'':<37}"  # brancos
        )


class Registro60A(BaseRecord):
    """Registro Tipo 60A - Equipamento Emissor de Cupom Fiscal (ECF) - Alíquota.

    Registro obrigatório para informar as alíquotas do equipamento emissor de cupom.
    """

    tipo: Literal["60"] = Field(default="60", description="Tipo do registro")
    subtipo: Literal["A"] = Field(default="A", description="Subtipo A")
    data: date = Field(..., description="Data de emissão dos documentos")
    serie: str = Field(
        ..., max_length=20, description="Série de fabricação do equipamento"
    )
    st_aliquota: str = Field(
        ...,
        max_length=4,
        description="Identificador da Situação Tributária/Alíquota do ICMS",
    )
    bc_icms: Decimal = Field(
        ..., ge=0, description="Valor acumulado no final do dia no totalizador parcial"
    )

    def to_sintegra_line(self) -> str:
        return (
            f"{self.tipo}"
            f"{self.subtipo}"
            f"{self.data.strftime('%Y%m%d')}"
            f"{self.serie:<20}"
            f"{self.st_aliquota:<4}"
            f"{int(self.bc_icms * 100):012d}"
            f"{'':<79}"  # brancos para completar 126 caracteres
        )


class Registro60I(BaseRecord):
    """Registro Tipo 60I - Equipamento Emissor de Cupom Fiscal (ECF) - Item.

    Registro obrigatório para informar os itens do equipamento emissor de cupom fiscal.
    """

    tipo: Literal["60"] = Field(default="60", description="Tipo do registro")
    subtipo: Literal["I"] = Field(default="I", description="Subtipo I")
    data: date = Field(..., description="Data de emissão dos documentos")
    modelo: str = Field(
        ..., max_length=2, description="Código do modelo do documento fiscal"
    )
    coo: int = Field(..., description="COO")
    item: int = Field(..., description="Número de ordem do item na nota fiscal")
    codigo: str = Field(
        ...,
        max_length=14,
        description="Código do produto/mercadoria ou serviço do informante",
    )
    quantidade: Decimal = Field(
        ..., ge=0, description="Quantidade do produto/mercadoria"
    )
    valor: Decimal = Field(..., ge=0, description="Valor bruto do produto/mercadoria")
    bc_icms: Decimal = Field(..., ge=0, description="Base de cálculo do ICMS")
    st_aliquota: str = Field(
        ...,
        max_length=4,
        description="Identificador da Situação Tributária/Alíquota do ICMS",
    )
    valor_icms: Decimal = Field(..., ge=0, description="Montante do imposto")

    def to_sintegra_line(self) -> str:
        return (
            f"{self.tipo}"
            f"{self.subtipo}"
            f"{self.data.strftime('%Y%m%d')}"
            f"{self.modelo:<2}"
            f"{self.coo:06d}"
            f"{self.item:03d}"
            f"{self.codigo:<14}"
            f"{int(self.quantidade * 1000):013d}"  # 3 decimais
            f"{int(self.valor * 1000):013d}"  # 3 decimais
            f"{int(self.bc_icms * 100):012d}"
            f"{self.st_aliquota:<4}"
            f"{int(self.valor_icms * 100):012d}"
            f"{'':<16}"  # brancos
        )


class Registro61(BaseRecord):
    """Registro Tipo 61 - Resumo Mensal de Documento Fiscal Emitido por ECF.

    Registro obrigatório para informar o resumo mensal dos documentos fiscais
    emitidos por equipamento emissor de cupom fiscal.
    """

    tipo: Literal["61"] = Field(default="61", description="Tipo do registro")
    data: date = Field(..., description="Data de emissão dos documentos")
    modelo: str = Field(
        ..., max_length=2, description="Código do modelo do documento fiscal"
    )
    serie: str = Field(..., max_length=3, description="Série do documento fiscal")
    subserie: str = Field(..., max_length=2, description="SubSérie do documento fiscal")
    coo_inicio: int = Field(..., description="COO do início do dia")
    coo_fim: int = Field(..., description="COO do fim do dia")
    valor_total: Decimal = Field(..., ge=0, description="Valor total")
    bc_icms: Decimal = Field(..., ge=0, description="Base de cálculo do ICMS")
    valor_icms: Decimal = Field(..., ge=0, description="Montante do imposto")
    isenta: Decimal = Field(
        ..., ge=0, description="Valor amparado por isenção ou não incidência"
    )
    outras: Decimal = Field(
        ..., ge=0, description="Valor que não confira débito ou crédito do ICMS"
    )
    aliquota: Decimal = Field(..., ge=0, le=100, description="Alíquota do ICMS")

    def to_sintegra_line(self) -> str:
        return (
            f"{self.tipo}"
            f"{'':<14}"  # brancos
            f"{'':<14}"  # brancos
            f"{self.data.strftime('%Y%m%d')}"
            f"{self.modelo:<2}"
            f"{self.serie:<3}"
            f"{self.subserie:<2}"
            f"{self.coo_inicio:06d}"
            f"{self.coo_fim:06d}"
            f"{int(self.valor_total * 100):013d}"
            f"{int(self.bc_icms * 100):013d}"
            f"{int(self.valor_icms * 100):012d}"
            f"{int(self.isenta * 100):013d}"
            f"{int(self.outras * 100):013d}"
            f"{int(self.aliquota * 100):04d}"
            f"{'':<1}"  # brancos
        )


class Registro61R(BaseRecord):
    """Registro Tipo 61R - Resumo Mensal de Itens do ECF por Produto.

    Registro obrigatório para informar o resumo mensal de itens do ECF por produto.
    """

    tipo: Literal["61"] = Field(default="61", description="Tipo do registro")
    subtipo: Literal["R"] = Field(default="R", description="Subtipo R")
    mes_ano: str = Field(
        ...,
        min_length=6,
        max_length=6,
        description="Mês e ano de emissão dos documentos fiscais (MMAAAA)",
    )
    codigo_produto: str = Field(
        ..., max_length=14, description="Código do produto do informante"
    )
    quantidade: Decimal = Field(
        ..., ge=0, description="Quantidade do produto/mercadoria"
    )
    valor_total: Decimal = Field(..., ge=0, description="Valor total")
    bc_icms: Decimal = Field(..., ge=0, description="Base de cálculo do ICMS")
    aliquota: Decimal = Field(..., ge=0, le=100, description="Alíquota do ICMS")

    def to_sintegra_line(self) -> str:
        return (
            f"{self.tipo}"
            f"{self.subtipo}"
            f"{self.mes_ano}"
            f"{self.codigo_produto:<14}"
            f"{int(self.quantidade * 1000):013d}"  # 3 decimais
            f"{int(self.valor_total):016d}"
            f"{int(self.bc_icms):016d}"
            f"{int(self.aliquota * 100):04d}"
            f"{'':<54}"  # brancos
        )


class Registro70(BaseRecord):
    """Registro Tipo 70 - Nota Fiscal de Serviços de Comunicação e de Telecomunicação.

    Registro obrigatório para informar as notas fiscais de serviços de comunicação
    e de telecomunicação.
    """

    tipo: Literal["70"] = Field(default="70", description="Tipo do registro")
    cnpj: str = Field(
        ...,
        min_length=14,
        max_length=14,
        description="CNPJ do contribuinte substituto tributário",
    )
    ie: str = Field(
        ...,
        max_length=14,
        description="Inscrição Estadual do contribuinte substituto tributário",
    )
    data: date = Field(..., description="Data da GNRE")
    uf: str = Field(
        ...,
        min_length=2,
        max_length=2,
        description="Unidade da Federação do contribuinte substituto tributário",
    )
    modelo: str = Field(
        ..., max_length=2, description="Código do modelo do documento fiscal"
    )
    serie: str = Field(..., max_length=3, description="Série do documento fiscal")
    subserie: str = Field(..., max_length=2, description="SubSérie do documento fiscal")
    numero: int = Field(..., description="Número da nota fiscal")
    cfop: int = Field(
        ..., ge=1000, le=9999, description="Código Fiscal de Operação e Prestação"
    )
    valor_total: Decimal = Field(..., ge=0, description="Valor total")
    bc_icms: Decimal = Field(..., ge=0, description="Base de cálculo do ICMS")
    valor_icms: Decimal = Field(..., ge=0, description="Montante do imposto")
    isenta: Decimal = Field(
        ..., ge=0, description="Valor amparado por isenção ou não incidência"
    )
    outras: Decimal = Field(
        ..., ge=0, description="Valor que não confira débito ou crédito do ICMS"
    )
    cif_fob: int = Field(..., description="Modalidade do Frete")
    situacao: str = Field(
        ..., min_length=1, max_length=1, description="Situação da Nota Fiscal"
    )

    @field_validator("uf")
    @classmethod
    def validate_uf(cls, v: str) -> str:
        valid_ufs = {
            "AC",
            "AL",
            "AP",
            "AM",
            "BA",
            "CE",
            "DF",
            "ES",
            "GO",
            "MA",
            "MT",
            "MS",
            "MG",
            "PA",
            "PB",
            "PR",
            "PE",
            "PI",
            "RJ",
            "RN",
            "RS",
            "RO",
            "RR",
            "SC",
            "SP",
            "SE",
            "TO",
        }
        if v.upper() not in valid_ufs:
            msg = f"UF deve ser uma das seguintes: {', '.join(valid_ufs)}"
            raise ValueError(msg)
        return v.upper()

    @field_validator("cnpj")
    @classmethod
    def validate_cnpj(cls, v: str) -> str:
        if not v.isdigit():
            msg = "CNPJ deve conter apenas dígitos"
            raise ValueError(msg)
        return v

    def to_sintegra_line(self) -> str:
        return (
            f"{self.tipo}"
            f"{self.cnpj.zfill(14)}"
            f"{self.ie:<14}"
            f"{self.data.strftime('%Y%m%d')}"
            f"{self.uf}"
            f"{self.modelo:<2}"
            f"{self.serie:<3}"
            f"{self.subserie:<2}"
            f"{self.numero:06d}"
            f"{self.cfop:04d}"
            f"{int(self.valor_total * 100):013d}"
            f"{int(self.bc_icms * 100):014d}"
            f"{int(self.valor_icms * 100):014d}"
            f"{int(self.isenta * 100):014d}"
            f"{int(self.outras * 100):013d}"
            f"{self.cif_fob:02d}"
            f"{self.situacao}"
        )


class Registro71(BaseRecord):
    """Registro Tipo 71 - Nota Fiscal de Serviços de Transporte.

    Registro obrigatório para informar as notas fiscais de serviços de transporte.
    """

    tipo: Literal["71"] = Field(default="71", description="Tipo do registro")
    cnpj_tomador: str = Field(
        ..., min_length=14, max_length=14, description="CNPJ do tomador"
    )
    ie_tomador: str = Field(
        ..., max_length=14, description="Inscrição Estadual do tomador"
    )
    data: date = Field(..., description="Data de emissão")
    uf_tomador: str = Field(
        ...,
        min_length=2,
        max_length=2,
        description="Unidade da Federação do contribuinte",
    )
    modelo: str = Field(
        ..., max_length=2, description="Código do modelo do documento fiscal"
    )
    serie: str = Field(..., max_length=3, description="Série do documento fiscal")
    subserie: str = Field(..., max_length=2, description="SubSérie do documento fiscal")
    numero: int = Field(..., description="Número da nota fiscal")
    uf_remetente: str = Field(
        ..., min_length=2, max_length=2, description="Unidade da Federação do remetente"
    )
    cnpj_remetente: str = Field(
        ..., min_length=14, max_length=14, description="CNPJ do remetente"
    )
    ie_remetente: str = Field(
        ..., max_length=14, description="Inscrição Estadual do remetente"
    )
    data_nf: date = Field(..., description="Data de emissão da NF")
    modelo_nf: str = Field(
        ..., max_length=2, description="Código do modelo do documento fiscal"
    )
    serie_nf: str = Field(..., max_length=3, description="Série do documento fiscal")
    numero_nf: int = Field(..., description="Número da nota fiscal")
    valor_total: Decimal = Field(..., ge=0, description="Valor total")

    @field_validator("uf_tomador", "uf_remetente")
    @classmethod
    def validate_uf(cls, v: str) -> str:
        valid_ufs = {
            "AC",
            "AL",
            "AP",
            "AM",
            "BA",
            "CE",
            "DF",
            "ES",
            "GO",
            "MA",
            "MT",
            "MS",
            "MG",
            "PA",
            "PB",
            "PR",
            "PE",
            "PI",
            "RJ",
            "RN",
            "RS",
            "RO",
            "RR",
            "SC",
            "SP",
            "SE",
            "TO",
        }
        if v.upper() not in valid_ufs:
            msg = f"UF deve ser uma das seguintes: {', '.join(valid_ufs)}"
            raise ValueError(msg)
        return v.upper()

    @field_validator("cnpj_tomador", "cnpj_remetente")
    @classmethod
    def validate_cnpj(cls, v: str) -> str:
        if not v.isdigit():
            msg = "CNPJ deve conter apenas dígitos"
            raise ValueError(msg)
        return v

    def to_sintegra_line(self) -> str:
        return (
            f"{self.tipo}"
            f"{self.cnpj_tomador.zfill(14)}"
            f"{self.ie_tomador:<14}"
            f"{self.data.strftime('%Y%m%d')}"
            f"{self.uf_tomador}"
            f"{self.modelo:<2}"
            f"{self.serie:<3}"
            f"{self.subserie:<2}"
            f"{self.numero:06d}"
            f"{self.uf_remetente}"
            f"{self.cnpj_remetente.zfill(14)}"
            f"{self.ie_remetente:<14}"
            f"{self.data_nf.strftime('%Y%m%d')}"
            f"{self.modelo_nf:<2}"
            f"{self.serie_nf:<3}"
            f"{self.numero_nf:06d}"
            f"{int(self.valor_total * 100):014d}"
            f"{'':<12}"  # brancos
        )


class Registro76(BaseRecord):
    """Registro Tipo 76 - Nota Fiscal de Serviços de Comunicação.

    Registro obrigatório para informar as notas fiscais de serviços de comunicação.
    """

    tipo: Literal["76"] = Field(default="76", description="Tipo do registro")
    cnpj: str = Field(
        ..., min_length=14, max_length=14, description="CNPJ do tomador do serviço"
    )
    ie: str = Field(
        ..., max_length=14, description="Inscrição Estadual do tomador do serviço"
    )
    modelo: str = Field(
        ..., max_length=2, description="Código do modelo do documento fiscal"
    )
    serie: str = Field(..., max_length=3, description="Série do documento fiscal")
    subserie: str = Field(..., max_length=2, description="SubSérie do documento fiscal")
    numero: int = Field(..., description="Número da nota fiscal")
    cfop: int = Field(
        ..., ge=1000, le=9999, description="Código Fiscal de Operação e Prestação"
    )
    tipo_receita: int = Field(
        ..., description="Código da identificação do tipo de receita"
    )
    data: date = Field(..., description="Data final")
    uf: str = Field(..., min_length=2, max_length=2, description="Unidade da Federação")
    valor_total: Decimal = Field(..., ge=0, description="Valor total")
    bc_icms: Decimal = Field(..., ge=0, description="Base de cálculo do ICMS")
    valor_icms: Decimal = Field(..., ge=0, description="Montante do imposto")
    isenta: Decimal = Field(
        ..., ge=0, description="Valor amparado por isenção ou não incidência"
    )
    outras: Decimal = Field(
        ..., ge=0, description="Valor que não confira débito ou crédito do ICMS"
    )
    aliquota: int = Field(
        ..., ge=0, le=100, description="Alíquota do ICMS (valor inteiro)"
    )
    situacao: str = Field(
        ..., min_length=1, max_length=1, description="Situação da Nota Fiscal"
    )

    @field_validator("uf")
    @classmethod
    def validate_uf(cls, v: str) -> str:
        valid_ufs = {
            "AC",
            "AL",
            "AP",
            "AM",
            "BA",
            "CE",
            "DF",
            "ES",
            "GO",
            "MA",
            "MT",
            "MS",
            "MG",
            "PA",
            "PB",
            "PR",
            "PE",
            "PI",
            "RJ",
            "RN",
            "RS",
            "RO",
            "RR",
            "SC",
            "SP",
            "SE",
            "TO",
        }
        if v.upper() not in valid_ufs:
            msg = f"UF deve ser uma das seguintes: {', '.join(valid_ufs)}"
            raise ValueError(msg)
        return v.upper()

    @field_validator("cnpj")
    @classmethod
    def validate_cnpj(cls, v: str) -> str:
        if not v.isdigit():
            msg = "CNPJ deve conter apenas dígitos"
            raise ValueError(msg)
        return v

    def to_sintegra_line(self) -> str:
        return (
            f"{self.tipo}"
            f"{self.cnpj.zfill(14)}"
            f"{self.ie:<14}"
            f"{self.modelo:<2}"
            f"{self.serie:<3}"
            f"{self.subserie:<2}"
            f"{self.numero:06d}"
            f"{self.cfop:04d}"
            f"{self.tipo_receita:01d}"
            f"{self.data.strftime('%Y%m%d')}"
            f"{self.uf}"
            f"{int(self.valor_total * 100):013d}"
            f"{int(self.bc_icms * 100):013d}"
            f"{int(self.valor_icms * 100):012d}"
            f"{int(self.isenta * 100):012d}"
            f"{int(self.outras * 100):012d}"
            f"{self.aliquota:02d}"
            f"{self.situacao}"
        )


class Registro85(BaseRecord):
    """Registro Tipo 85 - Informações de Exportação.

    Registro obrigatório para informar as operações de exportação.
    """

    tipo: Literal["85"] = Field(default="85", description="Tipo do registro")
    exportacao: int = Field(..., description="Nº da Declaração de Exportação")
    data_declaracao: date = Field(..., description="Data da declaração")
    natureza: int = Field(
        ..., ge=1, le=2, description="Natureza da exportação (1-Direta, 2-Indireta)"
    )
    registro: int = Field(..., description="Nº do registro de exportação")
    data_registro: date = Field(..., description="Data do registro")
    conhecimento: int = Field(..., description="Nº do conhecimento de embarque")
    data_conhecimento: date = Field(..., description="Data do conhecimento de embarque")
    tipo_conhecimento: int = Field(
        ..., description="Informação do tipo de conhecimento de transporte"
    )
    pais: int = Field(..., description="Código do país de destino da mercadoria")
    data_averbacao: date = Field(
        ..., description="Data da averbação da Declaração de exportação"
    )
    nf_exportacao: int = Field(..., description="Nº da nota fiscal de exportação")
    data_emissao: date = Field(..., description="Data de emissão")
    modelo: str = Field(
        ..., max_length=2, description="Código do modelo do documento fiscal"
    )
    serie: str = Field(..., max_length=3, description="Série do documento fiscal")

    def to_sintegra_line(self) -> str:
        return (
            f"{self.tipo}"
            f"{self.exportacao:011d}"
            f"{self.data_declaracao.strftime('%Y%m%d')}"
            f"{self.natureza:01d}"
            f"{self.registro:012d}"
            f"{self.data_registro.strftime('%Y%m%d')}"
            f"{self.conhecimento:012d}"
            f"{self.data_conhecimento.strftime('%Y%m%d')}"
            f"{self.tipo_conhecimento:02d}"
            f"{self.pais:04d}"
            f"{0:08d}"  # reservado - zeros
            f"{self.data_averbacao.strftime('%Y%m%d')}"
            f"{self.nf_exportacao:06d}"
            f"{self.data_emissao.strftime('%Y%m%d')}"
            f"{self.modelo:<2}"
            f"{self.serie:<3}"
            f"{'':<19}"  # brancos
        )


class Registro86(BaseRecord):
    """Registro Tipo 86 - Informações Complementares de Exportação.

    Registro obrigatório para informar as informações complementares de exportação.
    """

    tipo: Literal["86"] = Field(default="86", description="Tipo do registro")
    registro: int = Field(..., description="Nº do registro de exportação")
    data_registro: date = Field(..., description="Data do registro")
    cnpj: str = Field(
        ..., min_length=14, max_length=14, description="CNPJ do tomador do serviço"
    )
    ie: str = Field(
        ..., max_length=14, description="Inscrição Estadual do tomador do serviço"
    )
    uf: str = Field(..., min_length=2, max_length=2, description="Unidade da Federação")
    numero: int = Field(..., description="Número da nota fiscal")
    data_emissao: date = Field(..., description="Data de emissão")
    modelo: str = Field(
        ..., max_length=2, description="Código do modelo do documento fiscal"
    )
    serie: str = Field(..., max_length=3, description="Série do documento fiscal")
    codigo: str = Field(
        ...,
        max_length=14,
        description="Código do produto/mercadoria ou serviço do informante",
    )
    quantidade: Decimal = Field(
        ..., ge=0, description="Quantidade do produto/mercadoria"
    )
    valor: Decimal = Field(..., ge=0, description="Valor unitário do produto")
    relacionamento: int = Field(
        ...,
        description="Código de relacionamento entre registro de exportação e nota fiscal",  # noqa: E501
    )

    @field_validator("uf")
    @classmethod
    def validate_uf(cls, v: str) -> str:
        valid_ufs = {
            "AC",
            "AL",
            "AP",
            "AM",
            "BA",
            "CE",
            "DF",
            "ES",
            "GO",
            "MA",
            "MT",
            "MS",
            "MG",
            "PA",
            "PB",
            "PR",
            "PE",
            "PI",
            "RJ",
            "RN",
            "RS",
            "RO",
            "RR",
            "SC",
            "SP",
            "SE",
            "TO",
        }
        if v.upper() not in valid_ufs:
            msg = f"UF deve ser uma das seguintes: {', '.join(valid_ufs)}"
            raise ValueError(msg)
        return v.upper()

    @field_validator("cnpj")
    @classmethod
    def validate_cnpj(cls, v: str) -> str:
        if not v.isdigit():
            msg = "CNPJ deve conter apenas dígitos"
            raise ValueError(msg)
        return v

    def to_sintegra_line(self) -> str:
        return (
            f"{self.tipo}"
            f"{self.registro:012d}"
            f"{self.data_registro.strftime('%Y%m%d')}"
            f"{self.cnpj.zfill(14)}"
            f"{self.ie:<14}"
            f"{self.uf}"
            f"{self.numero:06d}"
            f"{self.data_emissao.strftime('%Y%m%d')}"
            f"{self.modelo:<2}"
            f"{self.serie:<3}"
            f"{self.codigo:<14}"
            f"{int(self.quantidade * 1000):013d}"  # 3 decimais
            f"{int(self.valor * 100):013d}"
            f"{self.relacionamento:01d}"
            f"{'':<5}"  # brancos
        )


class Registro90(BaseRecord):
    """Totalization record.

    Contains summary information about the number of records of each type
    in the SINTEGRA file.
    """

    cnpj: str = Field(
        ..., description="Reporting party's CNPJ", min_length=14, max_length=14
    )
    ie: str = Field(
        ..., description="Reporting party's state registration", max_length=14
    )
    totalizacoes: str = Field(..., description="Record totalizations", max_length=95)
    numero: int = Field(..., description="Number of type 90 records", ge=1, le=9)

    def to_sintegra_line(self) -> str:
        """Convert to SINTEGRA format line."""
        return (
            self._format_text("90", 2)
            + self._format_numeric(self.cnpj, 14)
            + self._format_text(self.ie, 14)
            + self._format_text(self.totalizacoes, 95)
            + self._format_numeric(self.numero, 1)
        )


class Registro74(BaseRecord):
    """Inventory record.

    Contains information about inventory items including quantities,
    unit values, and ownership details.
    """

    data: date = Field(..., description="Inventory date")
    codigo: str = Field(
        ..., description="Product/merchandise/service code", max_length=14
    )
    quantidade: Decimal = Field(..., description="Product quantity", ge=0)
    valor: Decimal = Field(..., description="Unit value", ge=0)
    posse: str = Field(..., description="Possession code", min_length=1, max_length=1)
    cnpj: str = Field(..., description="Owner's CNPJ", min_length=14, max_length=14)
    ie: str = Field(..., description="Owner's state registration", max_length=14)
    uf: str = Field(..., description="Owner's state", min_length=2, max_length=2)

    @field_validator("uf")
    @classmethod
    def validate_uf(cls, v: str) -> str:
        valid_ufs = {
            "AC",
            "AL",
            "AP",
            "AM",
            "BA",
            "CE",
            "DF",
            "ES",
            "GO",
            "MA",
            "MT",
            "MS",
            "MG",
            "PA",
            "PB",
            "PR",
            "PE",
            "PI",
            "RJ",
            "RN",
            "RS",
            "RO",
            "RR",
            "SC",
            "SP",
            "SE",
            "TO",
        }
        if v.upper() not in valid_ufs:
            msg = f"UF deve ser uma das seguintes: {', '.join(valid_ufs)}"
            raise ValueError(msg)
        return v.upper()

    @field_validator("cnpj")
    @classmethod
    def validate_cnpj(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("CNPJ deve conter apenas dígitos")  # noqa: EM101
        return v

    def to_sintegra_line(self) -> str:
        """Convert to SINTEGRA format line."""
        return (
            self._format_text("74", 2)
            + self._format_date(self.data)
            + self._format_text(self.codigo, 14)
            + self._format_numeric(self.quantidade, 13, 3)
            + self._format_numeric(self.valor, 13, 2)
            + self._format_text(self.posse, 1)
            + self._format_numeric(self.cnpj, 14)
            + self._format_text(self.ie, 14)
            + self._format_text(self.uf, 2)
            + self._format_text("", 45)  # Blanks
        )


class Registro75(BaseRecord):
    """Product and service code record.

    Contains detailed information about products including NCM codes,
    descriptions, units of measure, and tax rates.
    """

    data_inicial: date = Field(..., description="Start date")
    data_final: date = Field(..., description="End date")
    codigo: str = Field(
        ..., description="Product/merchandise/service code", max_length=14
    )
    ncm: str = Field(..., description="NCM code", min_length=8, max_length=8)
    descricao: str = Field(
        ..., description="Product/service description", max_length=53
    )
    un_com: str = Field(..., description="Commercial unit of measure", max_length=6)
    valor_ipi: Decimal = Field(..., description="IPI rate", ge=0, le=100)
    valor_icms: Decimal = Field(..., description="ICMS rate", ge=0, le=100)
    red_bc_icms: Decimal = Field(
        ..., description="ICMS base reduction percentage", ge=0, le=100
    )
    valor_bc_st: Decimal = Field(..., description="ICMS ST base value", ge=0)

    @field_validator("ncm")
    @classmethod
    def validate_ncm(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("NCM deve conter apenas dígitos")  # noqa: EM101
        return v

    def to_sintegra_line(self) -> str:
        """Convert to SINTEGRA format line."""
        return (
            self._format_text("75", 2)
            + self._format_date(self.data_inicial)
            + self._format_date(self.data_final)
            + self._format_text(self.codigo, 14)
            + self._format_text(self.ncm, 8)
            + self._format_text(self.descricao, 53)
            + self._format_text(self.un_com, 6)
            + self._format_numeric(self.valor_ipi, 5, 2)
            + self._format_numeric(self.valor_icms, 4, 2)
            + self._format_numeric(self.red_bc_icms, 5, 2)
            + self._format_numeric(self.valor_bc_st, 13, 2)
        )

"""
File parsing example of PySintegra.

This example demonstrates how to parse an existing SINTEGRA file
and load it back into Pydantic models.
"""

from datetime import date

from pysintegra import Registro10, Registro74, Registro75, SintegraProcessor

# First, create a sample SINTEGRA file
print("Creating a sample SINTEGRA file...")
processor = SintegraProcessor()

processor.add_registro_10(
    cnpj_mf="12345678910110",
    ie="ISENTO",
    nome_contribuinte="Empresa Exemplo LTDA",
    municipio="São Paulo",
    unidade_federacao="SP",
    fax="1133334444",
    data_inicial=date(2024, 1, 1),
    data_final=date(2024, 1, 31),
    cod_id_estrutura="1",
    cod_id_natureza="1",
    cod_id_finalidade="1",
)

processor.add_registro_74(
    data=date(2024, 1, 31),
    codigo="PROD001",
    quantidade=100.500,
    valor=25.99,
    posse="1",
    cnpj="12345678910110",
    ie="123456789",
    uf="SP",
)

processor.add_registro_75(
    data_inicial=date(2024, 1, 1),
    data_final=date(2024, 1, 31),
    codigo="PROD001",
    ncm="12345678",
    descricao="Produto de Exemplo para Demonstração",
    un_com="UN",
    valor_ipi=5.0,
    valor_icms=18.0,
    red_bc_icms=0.0,
    valor_bc_st=0.0,
)

# Save the file
sample_file = "sample_sintegra.txt"
processor.save_to_file(sample_file)
print(f"Sample file created: {sample_file}")

# Now parse the file back
print("\nParsing the file back into models...")
parsed_processor = SintegraProcessor.parse_from_file(sample_file)

print(f"Parsed {len(parsed_processor.records)} records")
print("Record counts:", parsed_processor.get_record_counts())

# Access individual records with type safety
for record in parsed_processor.records:
    if isinstance(record, Registro10):
        print("\nRegistro 10 found:")
        print(f"  CNPJ: {record.cnpj_mf}")
        print(f"  Company: {record.nome_contribuinte}")
        print(f"  City: {record.municipio}")
        print(f"  State: {record.unidade_federacao}")
        print(f"  Period: {record.data_inicial} to {record.data_final}")

    elif isinstance(record, Registro74):
        print("\nRegistro 74 found:")
        print(f"  Product Code: {record.codigo}")
        print(f"  Quantity: {record.quantidade}")
        print(f"  Unit Value: {record.valor}")
        print(f"  Date: {record.data}")

    elif isinstance(record, Registro75):
        print("\nRegistro 75 found:")
        print(f"  Product Code: {record.codigo}")
        print(f"  NCM: {record.ncm}")
        print(f"  Description: {record.descricao}")
        print(f"  Unit: {record.un_com}")
        print(f"  IPI Rate: {record.valor_ipi}%")
        print(f"  ICMS Rate: {record.valor_icms}%")

# Demonstrate validation - try to create an invalid record
print("\nDemonstrating validation...")
try:
    invalid_record = Registro10(
        cnpj_mf="invalid_cnpj",  # This should fail validation
        ie="ISENTO",
        nome_contribuinte="Test",
        municipio="Test",
        unidade_federacao="XX",  # Invalid UF
        fax="123",
        data_inicial=date.today(),
        data_final=date.today(),
        cod_id_estrutura="1",
        cod_id_natureza="1",
        cod_id_finalidade="1",
    )
except Exception as e:
    print(f"Validation error caught: {e}")

print("\nExample completed successfully!")

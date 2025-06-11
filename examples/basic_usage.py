"""
Basic usage example of PySintegra.

This example demonstrates how to create a simple SINTEGRA file with
the new Pydantic-based models.
"""

from datetime import date

from pysintegra import SintegraProcessor

# Create a new SINTEGRA processor
processor = SintegraProcessor()

# Add Registro 10 (establishment master record)
processor.add_registro_10(
    cnpj_mf="12345678910110",
    ie="ISENTO",
    nome_contribuinte="Nome do Contribuinte / Razao Social",
    municipio="Rio de Janeiro",
    unidade_federacao="RJ",
    fax="ISENTO",
    data_inicial=date.today(),
    data_final=date.today(),
    cod_id_estrutura="1",
    cod_id_natureza="1",
    cod_id_finalidade="1",
)

# Add Registro 74 (inventory record)
processor.add_registro_74(
    data=date.today(),
    codigo="00000000000000",
    quantidade=2.00,
    valor=2.00,
    posse="1",
    cnpj="00000000000000",
    ie="              ",
    uf="RJ",
)

# Add Registro 75 (product and service code record)
processor.add_registro_75(
    data_inicial=date.today(),
    data_final=date.today(),
    codigo="0000000000012",
    ncm="00000000",
    descricao="Produto Teste",
    un_com="UN",
    valor_ipi=0.0,
    valor_icms=0.0,
    red_bc_icms=0.0,
    valor_bc_st=0.0,
)

# Generate and print the SINTEGRA file content
print("Generated SINTEGRA file:")
print(processor.generate_output())

# Save to file
processor.save_to_file("output.txt")
print("File saved as 'output.txt'")

# Show record counts
print("Record counts:", processor.get_record_counts())

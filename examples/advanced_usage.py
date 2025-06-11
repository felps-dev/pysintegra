"""
Advanced usage example of PySintegra.

This example demonstrates advanced features like direct model usage,
validation, and working with multiple record types.
"""

from datetime import date
from decimal import Decimal

from pysintegra import (
    Registro10,
    Registro11,
    Registro50,
    Registro74,
    Registro75,
    SintegraProcessor,
)

print("=== Advanced PySintegra Usage Example ===\n")

# Example 1: Direct model usage with validation
print("1. Creating records directly with Pydantic models:")

try:
    # Create a Registro 10 directly
    registro_10 = Registro10(
        cnpj_mf="11222333000181",
        ie="123456789",
        nome_contribuinte="Empresa Avançada LTDA",
        municipio="Brasília",
        unidade_federacao="DF",
        fax="6133334444",
        data_inicial=date(2024, 1, 1),
        data_final=date(2024, 12, 31),
        cod_id_estrutura="1",
        cod_id_natureza="3",
        cod_id_finalidade="1",
    )
    print(f"✓ Registro 10 created: {registro_10.nome_contribuinte}")

    # Create a Registro 11 with address details
    registro_11 = Registro11(
        logradouro="Av. Paulista, 1000",
        numero=1000,
        complemento="Sala 101",
        bairro="Bela Vista",
        cep="01310100",
        nome_contato="João Silva",
        telefone="11999887766",
    )
    print(f"✓ Registro 11 created: {registro_11.logradouro}")

except Exception as e:
    print(f"✗ Error creating records: {e}")

# Example 2: Working with financial records (Registro 50)
print("\n2. Creating invoice records with precise decimal handling:")

registro_50 = Registro50(
    cnpj="11222333000181",
    ie="123456789",
    data=date(2024, 6, 15),
    unidade_federacao="SP",
    modelo=1,
    serie="001",
    numero=12345,
    cfop=5102,
    emitente="P",
    valor_total=Decimal("1250.75"),
    bc_icms=Decimal("1000.00"),
    valor_icms=Decimal("180.00"),
    isenta=Decimal("0.00"),
    outras=Decimal("70.75"),
    aliquota=Decimal("18.00"),
    situacao="N",
)
print(f"✓ Invoice record created: R$ {registro_50.valor_total}")

# Example 3: Batch processing with validation
print("\n3. Batch processing multiple products:")

products = [
    {
        "codigo": "PROD001",
        "ncm": "12345678",
        "descricao": "Notebook Dell Inspiron 15",
        "un_com": "UN",
        "valor_ipi": Decimal("5.0"),
        "valor_icms": Decimal("18.0"),
    },
    {
        "codigo": "PROD002",
        "ncm": "87654321",
        "descricao": "Mouse Óptico USB",
        "un_com": "UN",
        "valor_ipi": Decimal("10.0"),
        "valor_icms": Decimal("12.0"),
    },
    {
        "codigo": "PROD003",
        "ncm": "11223344",
        "descricao": "Teclado Mecânico RGB",
        "un_com": "UN",
        "valor_ipi": Decimal("15.0"),
        "valor_icms": Decimal("18.0"),
    },
]

processor = SintegraProcessor()

# Add the establishment record
processor.add_record(registro_10)
processor.add_record(registro_11)
processor.add_record(registro_50)

# Add product records
for product in products:
    registro_75 = Registro75(
        data_inicial=date(2024, 1, 1),
        data_final=date(2024, 12, 31),
        codigo=product["codigo"],
        ncm=product["ncm"],
        descricao=product["descricao"],
        un_com=product["un_com"],
        valor_ipi=product["valor_ipi"],
        valor_icms=product["valor_icms"],
        red_bc_icms=Decimal("0.0"),
        valor_bc_st=Decimal("0.0"),
    )
    processor.add_record(registro_75)
    print(f"✓ Product added: {product['descricao']}")

# Add inventory records for each product
for i, product in enumerate(products, 1):
    registro_74 = Registro74(
        data=date(2024, 12, 31),
        codigo=product["codigo"],
        quantidade=Decimal(f"{i * 10}.500"),  # Different quantities
        valor=Decimal(f"{i * 100}.99"),  # Different values
        posse="1",
        cnpj="11222333000181",
        ie="123456789",
        uf="DF",
    )
    processor.add_record(registro_74)

print(f"\n✓ Total records created: {len(processor.records)}")

# Example 4: Generate and analyze output
print("\n4. Generating SINTEGRA file:")

output = processor.generate_output()
lines = output.strip().split("\r\n")
print(f"✓ Generated {len(lines)} lines")

# Show record type distribution
record_counts = processor.get_record_counts()
print("\nRecord distribution:")
for record_type, count in record_counts.items():
    print(f"  {record_type}: {count}")

# Example 5: Validation demonstration
print("\n5. Demonstrating validation features:")

validation_tests = [
    {
        "name": "Invalid CNPJ format",
        "test": lambda: Registro10(
            cnpj_mf="invalid",
            ie="123456789",
            nome_contribuinte="Test",
            municipio="Test",
            unidade_federacao="SP",
            fax="123",
            data_inicial=date.today(),
            data_final=date.today(),
            cod_id_estrutura="1",
            cod_id_natureza="1",
            cod_id_finalidade="1",
        ),
    },
    {
        "name": "Invalid UF",
        "test": lambda: Registro10(
            cnpj_mf="12345678901234",
            ie="123456789",
            nome_contribuinte="Test",
            municipio="Test",
            unidade_federacao="XX",  # Invalid UF
            fax="123",
            data_inicial=date.today(),
            data_final=date.today(),
            cod_id_estrutura="1",
            cod_id_natureza="1",
            cod_id_finalidade="1",
        ),
    },
    {
        "name": "Invalid CFOP range",
        "test": lambda: Registro50(
            cnpj="12345678901234",
            ie="123456789",
            data=date.today(),
            unidade_federacao="SP",
            modelo=1,
            serie="001",
            numero=1,
            cfop=999,  # Invalid CFOP (should be 1000-9999)
            emitente="P",
            valor_total=Decimal("100.00"),
            bc_icms=Decimal("100.00"),
            valor_icms=Decimal("18.00"),
            isenta=Decimal("0.00"),
            outras=Decimal("0.00"),
            aliquota=Decimal("18.00"),
            situacao="N",
        ),
    },
]

for test in validation_tests:
    try:
        test["test"]()
        print(f"✗ {test['name']}: Should have failed validation")
    except Exception as e:
        print(f"✓ {test['name']}: Correctly caught - {str(e)[:50]}...")

# Save the final file
output_file = "advanced_example.txt"
processor.save_to_file(output_file)
print(f"\n✓ Complete SINTEGRA file saved as: {output_file}")

print("\n=== Advanced example completed successfully! ===")

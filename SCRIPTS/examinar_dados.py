import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Ler o arquivo
df = pd.read_excel('Palestra Desenvolvimento de SI (respostas).xlsx')

print("=" * 80)
print("PRIMEIRAS LINHAS")
print("=" * 80)
print(df.head(10))

print("\n" + "=" * 80)
print("INFORMAÇÕES")
print("=" * 80)
print(f"Linhas: {len(df)}")
print(f"Colunas: {len(df.columns)}")

print("\n" + "=" * 80)
print("NOMES DAS COLUNAS")
print("=" * 80)
for i, col in enumerate(df.columns):
    print(f"{i+1}. {col}")

print("\n" + "=" * 80)
print("TIPOS DE DADOS")
print("=" * 80)
print(df.dtypes)

print("\n" + "=" * 80)
print("RESUMO")
print("=" * 80)
print(df.describe(include='all'))

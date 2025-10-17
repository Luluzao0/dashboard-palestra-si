import pandas as pd
import numpy as np

df = pd.read_excel('Palestra Desenvolvimento de SI (respostas).xlsx')

print('='*100)
print('DIAGNÓSTICO COMPLETO DOS DADOS')
print('='*100)

print('\n1. DIMENSÕES')
print(f'Linhas: {len(df)}, Colunas: {len(df.columns)}')

print('\n2. NOMES DAS COLUNAS')
for i, col in enumerate(df.columns, 1):
    print(f'{i:2d}. {col}')

print('\n3. TIPOS DE DADOS')
print(df.dtypes)

print('\n4. VALORES NULOS')
print(df.isnull().sum())

print('\n5. ESTATÍSTICAS BÁSICAS')
print(df.describe())

print('\n6. AMOSTRA DE DADOS')
print(df.head(5).to_string())

print('\n7. VALORES ÚNICOS POR COLUNA')
for col in df.columns:
    unicos = df[col].nunique()
    print(f'{col}: {unicos} valores únicos')
    if unicos <= 10:
        print(f'   Valores: {df[col].unique().tolist()}')

print('\n8. VERIFICAÇÃO DE CONSISTÊNCIA')
# Verificar se valores numéricos estão corretos
numeric_cols = df.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    min_val = df[col].min()
    max_val = df[col].max()
    print(f'{col}: min={min_val}, max={max_val}')
    if min_val < 0 or max_val > 10:
        print(f'  ⚠️ AVISO: Valores fora do intervalo 0-10!')

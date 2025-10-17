import pandas as pd
import numpy as np

# Carregar dados originais
df = pd.read_excel('DADOS/Palestra Desenvolvimento de SI (respostas).xlsx')

print("="*100)
print("LIMPEZA E NORMALIZAÇÃO DE DADOS")
print("="*100)

# Renomear colunas para nomes curtos
df.columns = [
    'data_hora',
    'idade',
    'participou_pesquisa',
    'conteudo_claro_escala',      # 3-5
    'sistemas_aplicaveis_escala',  # 4-5
    'tecnologia_gestao_escala',    # 4-5
    'interacao_palestrantes_escala', # 2-5
    'integracao_clara',
    'potencial_aplicacao',
    'interesse_sig',
    'tecnologia_contribui',
    'cooperacao_beneficios',
    'participar_projetos',
    'avaliacao_geral_original'     # 0-10 (mas com outlier 0)
]

print("\nAntes da normalização:")
print(f"Avaliações escala (3-5 ou 4-5): min={df['conteudo_claro_escala'].min()}, max={df['conteudo_claro_escala'].max()}")
print(f"Avaliação geral: {sorted(df['avaliacao_geral_original'].unique())}")

# ═════════════════════════════════════════════════════════════════════════
# NORMALIZAR ESCALAS PARA 0-10
# ═════════════════════════════════════════════════════════════════════════

def normalizar_3_a_5_para_0_a_10(valor):
    """Converte escala 3-5 para 0-10"""
    if pd.isna(valor):
        return np.nan
    # Mapeamento: 3->0, 4->5, 5->10
    return (valor - 3) * 5

def normalizar_4_a_5_para_0_a_10(valor):
    """Converte escala 4-5 para 0-10"""
    if pd.isna(valor):
        return np.nan
    # Mapeamento: 4->0, 5->10
    return (valor - 4) * 10

def normalizar_2_a_5_para_0_a_10(valor):
    """Converte escala 2-5 para 0-10"""
    if pd.isna(valor):
        return np.nan
    # Mapeamento: 2->0, 3->3.33, 4->6.67, 5->10
    return (valor - 2) * (10/3)

# Aplicar normalização
df['conteudo_claro'] = df['conteudo_claro_escala'].apply(normalizar_3_a_5_para_0_a_10)
df['sistemas_aplicaveis'] = df['sistemas_aplicaveis_escala'].apply(normalizar_4_a_5_para_0_a_10)
df['tecnologia_gestao'] = df['tecnologia_gestao_escala'].apply(normalizar_4_a_5_para_0_a_10)
df['interacao_palestrantes'] = df['interacao_palestrantes_escala'].apply(normalizar_2_a_5_para_0_a_10)

# Para avaliação geral: remover o outlier 0 e substituir pela média
print("\nAnalisando avaliação geral...")
print(f"Valores originais: {sorted(df['avaliacao_geral_original'].unique())}")

# Identificar o outlier (0)
idx_outlier = df[df['avaliacao_geral_original'] == 0].index
print(f"Encontrado outlier (nota 0) na linha {idx_outlier.tolist()}")

# Substituir 0 pela média das demais notas
media_sem_zero = df[df['avaliacao_geral_original'] > 0]['avaliacao_geral_original'].mean()
print(f"Média das demais notas: {media_sem_zero:.2f}")

df['avaliacao_geral'] = df['avaliacao_geral_original'].copy()
df.loc[idx_outlier, 'avaliacao_geral'] = media_sem_zero

print(f"Valores corrigidos: {sorted(df['avaliacao_geral'].unique())}")

# Arredondar para 2 casas decimais
for col in ['conteudo_claro', 'sistemas_aplicaveis', 'tecnologia_gestao', 'interacao_palestrantes', 'avaliacao_geral']:
    df[col] = df[col].round(2)

print("\nDepois da normalização:")
print(f"Conteúdo claro: min={df['conteudo_claro'].min()}, max={df['conteudo_claro'].max()}")
print(f"Sistemas aplicáveis: min={df['sistemas_aplicaveis'].min()}, max={df['sistemas_aplicaveis'].max()}")
print(f"Tecnologia gestão: min={df['tecnologia_gestao'].min()}, max={df['tecnologia_gestao'].max()}")
print(f"Interação: min={df['interacao_palestrantes'].min()}, max={df['interacao_palestrantes'].max()}")
print(f"Avaliação geral: {sorted(df['avaliacao_geral'].unique())}")

# ═════════════════════════════════════════════════════════════════════════
# LIMPAR RESPOSTAS ABERTAS
# ═════════════════════════════════════════════════════════════════════════

print("\n" + "="*100)
print("LIMPEZA DE RESPOSTAS ABERTAS")
print("="*100)

for col in ['tecnologia_contribui', 'cooperacao_beneficios', 'participar_projetos']:
    nulos = df[col].isnull().sum()
    print(f"{col}: {nulos} valores nulos ({nulos/len(df)*100:.1f}%)")
    
    # Substituir NaN por texto padrão
    df[col] = df[col].fillna('[Sem resposta]')

# ═════════════════════════════════════════════════════════════════════════
# PREPARAR DADOS FINAIS
# ═════════════════════════════════════════════════════════════════════════

# Selecionar apenas colunas que usaremos
colunas_finais = [
    'data_hora',
    'idade',
    'participou_pesquisa',
    'conteudo_claro',
    'sistemas_aplicaveis',
    'tecnologia_gestao',
    'interacao_palestrantes',
    'integracao_clara',
    'potencial_aplicacao',
    'interesse_sig',
    'tecnologia_contribui',
    'cooperacao_beneficios',
    'participar_projetos',
    'avaliacao_geral'
]

df_limpo = df[colunas_finais].copy()

# Salvar em novo arquivo
df_limpo.to_excel('DADOS/Palestra_Dados_Normalizados.xlsx', index=False)

print("\n" + "="*100)
print("RESULTADO FINAL")
print("="*100)
print(f"\n✓ Arquivo salvo: DADOS/Palestra_Dados_Normalizados.xlsx")
print(f"✓ Linhas: {len(df_limpo)}, Colunas: {len(df_limpo.columns)}")
print(f"\nPrimeiras 3 linhas:")
print(df_limpo.head(3).to_string())

print("\n" + "="*100)
print("RESUMO ESTATÍSTICO")
print("="*100)
print(df_limpo[['conteudo_claro', 'sistemas_aplicaveis', 'tecnologia_gestao', 'interacao_palestrantes', 'avaliacao_geral']].describe().round(2))
